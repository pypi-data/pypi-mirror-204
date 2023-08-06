from cd2t.types.datatype import DataType
from cd2t.utils import *
from cd2t.results import *
from cd2t.schema import *
from cd2t.References import ReferenceFinding, OPT, ReferenceElement
from cd2t.RunTimeEnv import RunTimeEnv


class BaseDataType(DataType):
    type = 'any'
    path_symbol = '*'
    matching_classes = []
    options = [
        # option_name, required?, class, init_value
    ]
    support_reference = False

    def __init__(self) -> None:
        self.ref_OPT = OPT.NONE
        self.ref_key = ''
        self.data_type_mismatch_message = "Value is not '%s'" % self.type
        return
    
    def data_matches_type(self, data :any) -> bool:
        if self.type == 'any':
            return True
        for cls in self.matching_classes:
            if isinstance(data, cls):
                return True
        return False
    
    def build_schema(self, schema :dict, path :str, subschemas :dict, subpath :list, RTE :RunTimeEnv):
        self.__init__()
        path = path + self.path_symbol
        self.load_reference_option(schema, path)
        self.load_schema_options(schema, path)
        self.verify_options(path=path)
        return self
    
    def _get_data_type(self, option :str, path :str, RTE :RunTimeEnv) -> DataType:
        schema = self.__dict__[option]
        if isinstance(schema, dict):
            if len(schema) == 0:
                return BaseDataType()
            if not 'type' in schema.keys():
                raise SchemaError("Needs to have a key 'type'", path)
            data_type_name = schema['type']
        elif RTE.allow_shortcuts and isinstance(schema, str):
            data_type_name = schema
            self.__dict__[option] = dict()
        else:
            raise SchemaError("Wrong value type", path)
        
        try:
            data_type = RTE.get_data_type_class(data_type_name)()
        except SchemaError:
            raise SchemaError("Data type '%s' not found" % data_type_name, path)
        return data_type

    
    def load_reference_option(self, schema :dict, path :str):
        if not self.support_reference or 'reference' not in schema.keys():
            return
        options = schema.pop('reference', None)
        if options is None or not isinstance(options, dict):
            raise SchemaError("Must be a dictionary.", path + 'reference')
        
        if 'key' not in options.keys():
            raise SchemaError("Key missing", path + 'reference/key')
        self.ref_key = options.pop('key')
        if not isinstance(self.ref_key, str):
            raise SchemaError("Must be a string", path+ 'reference/key')
        
        mode = options.pop('mode', 'unique')
        u_scope = options.pop('unique_scope', 'global')
        p_scope = options.pop('producer_scope', 'global')
        c_scope = options.pop('consumer_scope', 'global')
        orphan = options.pop('allow_orphan_producer', True)
        if mode == 'unique':
            self.ref_OPT = OPT.UNIQUE | OPT.PRODUCER
        elif mode == 'producer':
            self.ref_OPT = OPT.PRODUCER
        elif mode == 'consumer':
            self.ref_OPT = OPT.CONSUMER
        else:
            raise SchemaError("Unsupported mode", path + 'reference/mode')
        if OPT.UNIQUE in self.ref_OPT:
            if u_scope == 'global':
                self.ref_OPT = self.ref_OPT | OPT.UNIQUE_GLOBAL
            elif u_scope != 'namespace':
                raise SchemaError("Must be either 'global' or 'namespace'", path + 'reference/unique_scope')
        if OPT.PRODUCER in self.ref_OPT:
            if p_scope == 'global':
                self.ref_OPT = self.ref_OPT | OPT.PRODUCER_GLOBAL
            elif p_scope != 'namespace':
                raise SchemaError("Must be either 'global' or 'namespace'", path + 'reference/producer_scope')
            if orphan:
                self.ref_OPT = self.ref_OPT | OPT.ALLOW_ORPHAN_PRODUCER
        if OPT.CONSUMER in self.ref_OPT:
            if c_scope == 'global':
                self.ref_OPT = self.ref_OPT | OPT.CONSUMER_GLOBAL
            elif c_scope != 'namespace':
                raise SchemaError("Must be either 'global' or 'namespace'", path + 'reference/consumer_scope')
        if not isinstance(orphan, bool):
            raise SchemaError("Must be bool", path + 'reference/allow_orphan_producer')
        if len(options):
            raise SchemaError("Unknown option keys '%s'" % ','.join(options.keys()), path + 'reference')
    
    def verify_options(self, path :str):
        return
    
    def load_schema_options(self, schema :dict, path :str) -> None:
        schema.pop('type', None)
        for option, required, cls, init_value in self.options:
            if option in schema.keys():
                value = schema[option]
                if isinstance(cls, list):
                    found = False
                    for _cls in cls:
                        if isinstance(value, _cls):
                            found = True
                            break
                    if not found:
                        raise SchemaError("Wrong value type", path + option)
                elif not isinstance(value, cls):
                    raise SchemaError("Wrong value type", path + option)
                exec("self." + option + " = value")
                schema.pop(option, None)
            elif required:
                raise SchemaError("Key missing", path + option)
        if len(schema):
            raise SchemaError("Unknown option keys '%s'" % ', '.join(schema.keys()), path)
        return

    def validate_data(self, data :any, path :str, RTE :RunTimeEnv) -> FindingsList:
        FL = FindingsList()
        if not self.data_matches_type(data):
            FL.append(DataTypeMismatch(path=path, message=self.data_type_mismatch_message))
            return FL
        FL += self.verify_reference(data, path, RTE)
        FL += self.verify_data(data, path, RTE)
        return FL

    def verify_data(self, data :any, path :str, RTE :RunTimeEnv) -> FindingsList:
        return FindingsList()
    
    def build_sub_references(self, data :any, path :str, RTE :RunTimeEnv) -> None:
        return
    
    def build_references(self, data :any, path :str, RTE :RunTimeEnv) -> None:
        if self.data_matches_type(data):
            self.verify_reference(data=data, path=path, RTE=RTE)
            self.build_sub_references(data=data, path=path, RTE=RTE)
    
    def autogenerate_data(self, data :any, path :str, RTE :RunTimeEnv):
        return data, FindingsList()
    
    def get_reference_data(self, data :any, path :str) -> any:
        return data, FindingsList()
    
    def get_reference_element(self, path :str, ref_data :any) -> any:
        return ReferenceElement(self.ref_key, path, ref_data, self.ref_OPT)
    
    def verify_reference(self, data :any, path :str, RTE :RunTimeEnv) -> FindingsList:
        FL = FindingsList()
        if not self.support_reference or OPT.NONE in self.ref_OPT:
            return FL
        ref_data, _FL = self.get_reference_data(data, path)
        FL += _FL
        ref_element = self.get_reference_element(path, ref_data)
        if OPT.UNIQUE in self.ref_OPT:
            other = RTE.references.same_unique(ref_element)
            if other is not None:
                if other.namespace != RTE.references.namespace:
                    _path = "%s > %s" % (other.namespace, other.path)
                else:
                    _path = other.path
                FL.append(ReferenceFinding(
                    path=path,message="Unique value already used at '%s'" % _path,
                    reference=ref_element))
                return FL
        # If unique or just for producer/consumer mapping, add element to references
        RTE.references.add_element(ref_element)
        return FL
