from cd2t.types.base import BaseDataType
from cd2t.utils import string_matches_regex_list, regex_matches_in_string_list
from cd2t.results import ValidationFinding, FindingsList
from cd2t.schema import SchemaError
from cd2t.RunTimeEnv import RunTimeEnv


class Object(BaseDataType):
    type = 'object'
    path_symbol = '{}'
    matching_classes = [dict]
    support_reference = True
    options = [
        # option_name, required, class, init_value
        ('attributes', False, dict, None),
        ('required_attributes', False, list, list),
        ('dependencies', False, dict, dict()),
        ('reference_attributes', False, list, None),
        ('ignore_undefined_attributes', False, bool, False),
        ('allow_regex_attributes', False, bool, False),
        ('autogenerate', False, bool, True)
    ]

    def __init__(self) -> None:
        super().__init__()
        self.attributes = None
        self.attributes_objects = dict()
        self.tmp_a_schema = None
        self.required_attributes = list()
        self.dependencies = dict()
        self.reference_attributes = None
        self.ignore_undefined_attributes = False
        self.allow_regex_attributes = False
        self.autogenerate = True
        return
    
    def build_schema(self, schema :dict, path :str, subschemas :dict, subpath :list, RTE :RunTimeEnv):
        self.__init__()
        path = path + self.path_symbol
        self.load_reference_option(schema, path)
        self.load_schema_options(schema, path)
        if self.attributes is None:
            # No other options should be set:
            for option, required, cls, init_value in self.options:
                if exec("self." + option + " != init_value"):
                    raise SchemaError("Option 'attribute' is omitted, no other option is expected.")
            return self
        if self.reference_attributes is None:
            if self.ref_key and self.allow_regex_attributes:
                raise SchemaError("Reference attributes must be defined if reference is enabled and regex is allowed", path)
            self.reference_attributes = self.attributes
        for req_attr in self.required_attributes:
            if not self._attribute_in_list(req_attr, list(self.attributes.keys()), self.allow_regex_attributes):
                raise SchemaError("Required attribute '%s' not in attributes" % req_attr, path)
        for ref_attr in self.reference_attributes:
            if ref_attr not in self.attributes.keys():
                raise SchemaError("Reference attribute '%s' not in attributes" % ref_attr, path)
        for dep_attr, dep_info in self.dependencies.items():
            if dep_attr not in self.attributes.keys():
                raise SchemaError("Depency attribute '%s' not in attributes" % dep_attr, path)
            if not isinstance(dep_info, dict):
                raise SchemaError("Dependency for '%s' is not a dictionary" % dep_attr, path)
            for req_attr in dep_info.get('requires', []):
                if not self._attribute_in_list(req_attr, list(self.attributes.keys()), self.allow_regex_attributes):
                    raise SchemaError("Required attribute '%s' " % req_attr +\
                                      "for dependency '%s' not in attributes" % dep_attr, path)
            for ex_attr in dep_info.get('excludes', []):
                if not self._attribute_in_list(ex_attr, list(self.attributes.keys()), self.allow_regex_attributes):
                    raise SchemaError("Excluded attribute '%s' " % ex_attr +\
                                      "for dependency '%s' not in attributes" % dep_attr, path)
        #
        for a_name, a_schema in self.attributes.items():
            a_path = path + a_name
            self.tmp_a_schema = a_schema
            data_type = self._get_data_type('tmp_a_schema', a_path, RTE)
            # Save recursively detected data type (i.e. from 'schema' --> subschema)
            self.attributes_objects[a_name] = data_type.build_schema(self.tmp_a_schema, a_path, subschemas, subpath, RTE)
        return self
    
    def build_references(self, data :any, path :str, RTE :RunTimeEnv):
        for a_name, a_data in data.items():
            data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
            if data_type is None:
                continue
            a_path = path + self.path_symbol + a_name
            data_type.build_references(a_data, a_path, RTE)
    
    def autogenerate_data(self, data :any, path :str, RTE :RunTimeEnv):
        FL = FindingsList()
        if data is None or not self.data_matches_type(data):
            return data, FL
        if not self.allow_regex_attributes and self.autogenerate:
            if RTE.ruamel_yaml_available and isinstance(data, RTE.CommentedMap):
                new_data = data
                insert = True
            else:
                new_data = dict()
                insert = False
            i = 0
            for a_name, data_type in self.attributes_objects.items():
                a_path = path + self.path_symbol + a_name
                _FL = FindingsList()
                if a_name not in data.keys():
                    _data, _FL = data_type.autogenerate_data(data=None, path=a_path, RTE=RTE)
                    if _FL:
                        if insert:
                            new_data.insert(pos=i, key=a_name, value=_data, comment='autogenerated')
                        else:
                            new_data[a_name] = _data
                        i += 1
                else:
                    _data, _FL = data_type.autogenerate_data(data[a_name], a_path, RTE)
                    new_data[a_name] = _data
                    i += 1
                FL += _FL
            data = new_data
        else:
            for a_name, a_data in data.items():
                data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
                if data_type is None:
                    continue
                a_path = path + self.path_symbol + a_name
                _data, _FL = data_type.autogenerate_data(a_data, a_path, RTE)
                if _FL:
                    data[a_name] = _data
                    FL += _FL
        return data, FL
    
    @staticmethod
    def _attribute_in_list(attribute :str, attributes :list, regex_allowed=False) -> bool:
        if regex_allowed:
            return  regex_matches_in_string_list(attribute, attributes)
        elif attribute in attributes:
            return attribute
        return None
    
    def _get_attribute_object(self, name :str, regex_allowed=False) -> bool:
        if regex_allowed:
            name = string_matches_regex_list(string=name,
                                                   regex_list=list(self.attributes_objects.keys()),
                                                   full_match=True)
        return self.attributes_objects.get(name, None)

    def verify_data(self, data :any, path :str, RTE :RunTimeEnv) -> FindingsList:
        FL = FindingsList()
        if self.attributes is None:
            return FL
        path = path + self.path_symbol
        for a_name, a_data in data.items():
            data_type = self._get_attribute_object(a_name, self.allow_regex_attributes)
            if data_type is None:
                if self.ignore_undefined_attributes:
                    continue
                FL.append(ValidationFinding(path=path, message="Invalid attribute '%s'" % a_name))
                continue
            a_path = path + a_name
            FL += data_type.validate_data(data=a_data, path=a_path, RTE=RTE)
        for req_attr in self.required_attributes:
            found_in_data_keys = False
            if self.allow_regex_attributes:
                if regex_matches_in_string_list(
                                                regex=req_attr,
                                                strings=list(data.keys()),
                                                full_match=True):
                    found_in_data_keys = True
            elif req_attr in data.keys():
                found_in_data_keys = True
            if not found_in_data_keys:
                FL.append(ValidationFinding(
                    path = path + req_attr,
                    message = "Required attribute missing"))
        for attr_name, dep_info in self.dependencies.items():
            if not attr_name in data.keys():
                continue
            a_path = path + attr_name
            for req_attr in dep_info.get('requires', list()):
                if self.allow_regex_attributes:
                    if not regex_matches_in_string_list(
                                                            regex=req_attr,
                                                            strings=list(data.keys()),
                                                            full_match=True):
                        FL.append(ValidationFinding(
                            path = a_path,
                            message = "No attribute matches regex requirements"))
                elif req_attr not in data.keys():
                    FL.append(ValidationFinding(
                        path = a_path,
                        message = "Required attribute '%s' missing" % req_attr))
            for ex_attr in dep_info.get('excludes', list()):
                match = None
                if self.allow_regex_attributes:
                    match = regex_matches_in_string_list(
                                                            regex=ex_attr,
                                                            strings=list(data.keys()),
                                                            full_match=True)
                    if match:
                        found_in_data_keys = True
                elif ex_attr in data.keys():
                    match = ex_attr
                if match:
                    FL.append(ValidationFinding(
                        path = a_path,
                        message = "Excluded attribute '%s' found" % match))
        return FL
    
    def get_reference_data(self, data: any, path :str) -> any:
        ref_data = list()
        results = list()
        for ref_attr in self.reference_attributes:
            if ref_attr not in data.keys():
                results.append(ValidationFinding(path = path+'{}',
                                           message = "Reference attribute '%s' missing" % ref_attr))
            ref_data.append(data[ref_attr])
        return ref_data, results
