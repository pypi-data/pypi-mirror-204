from cd2t.types import *
from cd2t.schema import Schema, SchemaError
from cd2t.results import FindingsList
from cd2t.References import ReferenceFinding
from cd2t.RunTimeEnv import RunTimeEnv
import copy


BUILTIN_DATA_TYPES = {
    'any': BaseDataType,
    'bool': Bool,
    'enum': Enum,
    'float': Float,
    'idlist': IDList,
    'integer': Integer,
    'list': List,
    'multitype': Multitype,
    'none': NoneDataType,
    'object': Object,
    'schema': SchemaDataType,
    'string': String
}

class DataParser():
    """ Mother class for all data processing classes """

    def __init__(self, namespace: str='') -> None:
        self.RTE = RunTimeEnv(namespace=namespace, data_types=BUILTIN_DATA_TYPES)
        self.current_schema = None
    
    @property
    def namespace(self):
        return self.RTE.namespace
        
    def change_namespace(self, namespace :str) -> None:
        self.RTE.change_namespace(namespace=namespace)
    
    def _get_schema_object(self, schema: Schema) -> Schema:
        """ Return a schema object. Either given schema if valid or last loaded schema

        Args:
            schema: Schema object
        
        Return:
            A valid Schema object

        Raises:
            SchemaError:
                - If given schema is not a Schema object
                - If given schema object is not valid and no schema has been loaded before
        """
        if not isinstance(schema, Schema):
            raise SchemaError('Given schema is not a valid schema object')
        if schema.root_data_type is None:
            if self.current_schema is None:
                raise SchemaError('need a schema or ' +\
                                        'Validator object loads a schema first')
            return self.current_schema
        return schema

    def load_data_type(self, type_name :str, type_class :any) -> None:
        self.RTE.load_data_type(type_name=type_name, type_class=type_class)
    
    def load_schema(self, schema :dict) -> Schema:
        """ Verify schema definition, converts it to a Schema object and stores it.

        Args:
            schema: dictionary - containing schema definition
        
        Return:
            A valid Schema object

        Raises:
            SchemaError: If given schema is not a dictionary or not a valid schema definition
        """
        def verify_schema_format(schema_dic :dict, sub=False, sub_name=''):
            try:
                if not isinstance(schema_dic, dict):
                    raise SchemaError('needs to be an dictionary')
                if 'root' not in schema_dic.keys():
                    raise SchemaError("has no key 'root'")
                root_schema = schema_dic.get('root', None)
                if not isinstance(root_schema, dict):
                    if self.RTE.allow_shortcuts:
                        if not isinstance(root_schema, str):
                            raise SchemaError('root needs to be an dictionary or a string')
                        root_type_name = root_schema
                        root_schema = dict()
                    else:
                        raise SchemaError("root is not a dictionary")
                else:
                    root_type_name = root_schema.get('type', None)
                if len(root_schema) and 'type' not in root_schema.keys():
                    raise SchemaError("option 'type' in root schema missing")
            except SchemaError as se:
                if sub:
                    raise SchemaError("Subschema '%s' %s" % (sub_name, str(se)))
                raise SchemaError("Schema %s" % str(se))
            if root_type_name is None:
                root_class = BaseDataType
            else:
                try:
                    root_class = self.RTE.get_data_type_class(root_type_name)
                except SchemaError as se:
                    raise SchemaError("Schema root type '%s' not found" % str(root_type_name))
            return root_class, root_schema
        
        schema = copy.copy(schema)

        self.RTE.allow_shortcuts = schema.get('allow_data_type_shortcuts', False)

        sub_schemas = dict()
        if 'subschemas' in schema.keys():
            sub_schemas = schema['subschemas']
            if not isinstance(sub_schemas, dict):
                raise SchemaError("Schema subschemas is no mapping")
            for sub_name in sub_schemas.keys():
                sub_schema = sub_schemas[sub_name]
                if isinstance(sub_schema, Schema):
                    # This subschema was already verified/translated (recursively)
                    continue
                sub_type_class, sub_type_schema = verify_schema_format(sub_schema, sub=True, sub_name=sub_name)
                sub_type = sub_type_class().build_schema(
                                schema=sub_type_schema, path='<' + sub_name +'>',
                                subschemas=sub_schemas, subpath=[sub_name],
                                RTE=self.RTE
                            )
                sub_schema_obj = Schema()
                sub_schema_obj.set_root_data_type(sub_type)
                sub_schemas[sub_name] = sub_schema_obj
                
        root_type_class, root_type_schema = verify_schema_format(schema)
        root_type = root_type_class().build_schema(
                schema=root_type_schema, path='',
                subschemas=sub_schemas, subpath=[],
                RTE=self.RTE
            )
        schema_obj = Schema()
        schema_obj.set_root_data_type(root_type)
        self.current_schema = schema_obj
        return schema_obj
    
    def get_reference_findings(self) -> list[ReferenceFinding]:
        """ Get references findings after data validation(s)

        Returns:
            list - containing all findings as ReferenceFinding objects
        """
        return self.RTE.references.get_producer_consumer_issues()


class Autogenerator(DataParser):
    """
        Autogenerator can:
        - load/verify schema definitions
        - build references on multiple data sets
        - autogenerate data in data sets according to schema definition(s) and references
    """
    def build_references(self, data :any, schema=Schema()) -> None:
        """ Build/Populate references from data with schema definitions

        Args:
            data: any - Any data from which references should be analyzed

            schema: Schema object
                If not given or Schema object is not valid, last loaded schema is used 
        """
        schema = self._get_schema_object(schema)
        root_data_type = schema.root_data_type
        root_data_type.build_references(data=data, path='', RTE=self.RTE)

    def autogenerate_data(self, data :any, schema=Schema()) -> any:
        """ Autogenerate missing data according to schema and references

        Args:
            data: any - Any data where missing data should be added

            schema: Schema object
                If not given or Schema object is not valid, last loaded schema is used 
        
        Returns:
            tuple:
                - any - Given 'data' with autogerenated data added
                - FindingsList object - containing all findings as Finding objects
        """
        schema = self._get_schema_object(schema)
        root_data_type = schema.root_data_type
        new_data, FL = root_data_type.autogenerate_data(data=data, path='', RTE=self.RTE)
        FL.set_namespace(self.RTE.namespace)
        return new_data, FL
    
    
class Validator(DataParser):
    """
        Validator can:
        - load/verify schema definitions
        - validate data according to schema definition(s) and analyzed references
    """
    def validate_data(self, data :any, schema=Schema()) -> FindingsList:
        """ Validate data according to schema and references

        Args:
            data: any - Any data which should be validated

            schema: Schema object
                If not given or Schema object is not valid, last loaded schema is used 
        
        Returns:
            FindingsList object - containing all findings as Finding objects
        """
        schema = self._get_schema_object(schema)
        root_data_type = schema.root_data_type
        FL = root_data_type.validate_data(data=data, path='', RTE=self.RTE)
        FL.set_namespace(self.RTE.namespace)
        return FL
    