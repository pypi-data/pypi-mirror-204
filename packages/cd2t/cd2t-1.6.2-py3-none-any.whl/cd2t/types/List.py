from cd2t.types.base import BaseDataType
from cd2t.results import FindingsList, ValidationFinding, WrongValueFinding
from cd2t.schema import SchemaError
from cd2t.RunTimeEnv import RunTimeEnv
import copy

class List(BaseDataType):
    type = 'list'
    path_symbol = '[]'
    matching_classes = [list]
    options = [
        # option_name, required, class
        ('minimum', False, int, None),
        ('maximum', False, int, None),
        ('allow_duplicates', False, bool, True),
        ('elements', True, [dict, str], dict()),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.minimum = None
        self.maximum = None
        self.allow_duplicates = True
        self.elements = dict()
        self.element_data_type = None
    
    def build_schema(self, schema :dict, path :str, subschemas :dict, subpath :list, RTE :RunTimeEnv):
        self.__init__()
        path = path + self.path_symbol
        self.load_schema_options(schema, path)

        self.element_data_type = self._get_data_type('elements', path + 'elements', RTE)
        # Save recursively detected data type (i.e. from 'schema' --> subschema)
        self.element_data_type = self.element_data_type.build_schema(
            schema=self.elements, path=path,
            subschemas=subschemas, subpath=subpath,
            RTE=RTE)
        return self
    
    def build_sub_references(self, data :any, path :str, RTE :RunTimeEnv):
        i = 0
        for element in data:
            self.element_data_type.build_references(element, "%s[%d]" % (path, i), RTE)
            i += 1
    
    def autogenerate_data(self, data :any, path :str, RTE :RunTimeEnv):
        FL = FindingsList()
        if not self.data_matches_type(data):
            return data, FL
        for i in range(len(data)):
            _data, _FL = self.element_data_type.autogenerate_data(data[i], "%s[%d]" % (path, i), RTE)
            data[i] = _data
            FL += _FL
        return data, FL

    def verify_data(self, data :any, path :str, RTE :RunTimeEnv) -> FindingsList:
        FL = FindingsList()
        if self.minimum and len(data) < self.minimum:
            FL.append(WrongValueFinding(
                        path=path,
                        message='Length of list is lower than %d' % self.minimum))
        elif self.maximum and len(data) > self.maximum:
            FL.append(WrongValueFinding(
                        path=path,
                        message='Length of list is greater than %d' % self.maximum))
        i = 0
        for element in data:
            FL += self.element_data_type.validate_data(element, "%s[%d]" % (path, i), RTE)
            i += 1
        
        if not self.allow_duplicates:
            remaining_data = copy.copy(data)
            i = 0 
            for element in data:
                remaining_data = remaining_data[1:]
                if element in remaining_data:
                    relative_position = remaining_data.index(element) + 1
                    FL.append(ValidationFinding(
                        path="%s[%d]" % (path, i),
                        message='Element is same as on position %d' % (i + relative_position)))
                i += 1
        return FL
