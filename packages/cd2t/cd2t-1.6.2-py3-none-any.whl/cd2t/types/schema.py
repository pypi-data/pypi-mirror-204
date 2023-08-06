from cd2t.types.base import BaseDataType
from cd2t.schema import SchemaError, Schema
from cd2t.RunTimeEnv import RunTimeEnv
import copy

class SchemaDataType(BaseDataType):
    type = 'schema'
    path_symbol = '<>'
    options = [
        # option_name, required, class
        ('subschema', True, str, ''),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.subschema = ''
        self.sub_root_schema = None
    
    def build_schema(self, schema :dict, path :str, subschemas :dict, subpath :list, RTE :RunTimeEnv):
        self.__init__()
        _path = path
        path = path + self.path_symbol
        self.load_schema_options(schema, path)
        _sub_schema = subschemas.get(self.subschema, None)
        if _sub_schema is None:
            raise SchemaError("Could not found subschema '%s'" % self.subschema, path)
        new_path = _path + '<' + self.subschema + '>'
        if self.subschema in subpath:
            raise SchemaError("Subschema loop detected %s"
                                    % " -> ".join(subpath + [self.subschema]), new_path)
        new_subpath = copy.copy(subpath)
        new_subpath.append(self.subschema)
        if isinstance(_sub_schema, Schema):
            # Subschema was already build.
            return _sub_schema.root_data_type
        sub_root_schema = _sub_schema.get('root', None)
        if sub_root_schema is None:
            raise SchemaError("Key missing", new_path + 'root')
        self.sub_root_schema = sub_root_schema
        sub_data_obj = self._get_data_type('sub_root_schema', new_path + 'root', RTE)
        sub_data_obj = sub_data_obj.build_schema(
                                schema=self.sub_root_schema, path=new_path,
                                subschemas=subschemas, subpath=new_subpath,
                                RTE=RTE)
        sub_schema_obj = Schema()
        sub_schema_obj.set_root_data_type(sub_data_obj)
        subschemas[self.subschema] = sub_schema_obj
        return sub_data_obj
    