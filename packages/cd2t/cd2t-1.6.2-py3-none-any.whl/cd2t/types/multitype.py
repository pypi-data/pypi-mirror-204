from cd2t.types.base import BaseDataType
from cd2t.results import DataTypeMismatch, FindingsList
from cd2t.schema import SchemaError
from cd2t.RunTimeEnv import RunTimeEnv


class Multitype(BaseDataType):
    type = 'multitype'
    path_symbol = '?'
    options = [
        # option_name, required, class
        ('types', True, list, None),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.types = None
        self.type_objects = list()
        self.tmp_type = None
        self.matching_classes = []
        self.data_type_mismatch_message = "None of the data types matches"
    
    def build_schema(self, schema :dict, path :str, subschemas :dict, subpath :list, RTE :RunTimeEnv):
        self.__init__()
        path = path + self.path_symbol
        self.load_schema_options(schema, path)
        i = 0
        for _type in self.types:
            _path = "%stypes[%d]" % (path, i)
            if isinstance(_type, dict) and not len(_type):
                raise SchemaError('Empty dictionary is not allowed', _path)
            self.tmp_type = _type
            data_type = self._get_data_type('tmp_type', _path, RTE)
            if data_type.type == self.type:
                raise SchemaError("Multitype in Multitype not supported", _path)
            data_type = data_type.build_schema(
                schema=self.tmp_type, path=path,
                subschemas=subschemas, subpath=subpath,
                RTE=RTE)
            self.type_objects.append(data_type)
            self.matching_classes.extend(data_type.matching_classes)
            i += 1
        return self

    def build_sub_references(self, data :any, path :str, RTE :RunTimeEnv) -> list:
        for type_object in self.type_objects:
            if type_object.data_matches_type(data):
                type_object.build_references(data=data, path=path, RTE=RTE)
    
    def autogenerate_data(self, data :any, path :str, RTE :RunTimeEnv):
        FL = FindingsList()
        if data is None:
            return data, FL
        # Try to find ...
        for type_object in self.type_objects:
            if type_object.data_matches_type:
                FL += type_object.autogenerate_data(data=data, path=path, RTE=RTE)
        return data, FL

    def validate_data(self, data :any, path :str, RTE=RunTimeEnv) -> list:
        FL = FindingsList()
        FL_without_direct_findings = False
        for type_object in self.type_objects:
            _FL = type_object.validate_data(data=data, path=path, RTE=RTE)
            if _FL:
                if not FL_without_direct_findings and \
                        len(_FL[0].path) > len(path) + 2:
                    # Path in first finding is not from direct specified data type
                    # -> is comming from sub data types. So first level is 100% fine.
                    FL = _FL
                    FL_without_direct_findings = True
                elif not FL and not isinstance(_FL[0], DataTypeMismatch):
                    FL = _FL
            else:
                return _FL
        if not FL:
            FL.append(DataTypeMismatch(path=path, message='None of the data types matches'))
        return FL

