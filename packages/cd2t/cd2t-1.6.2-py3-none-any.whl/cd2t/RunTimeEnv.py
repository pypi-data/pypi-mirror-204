from cd2t.types.datatype import DataType
from cd2t.References import References
from cd2t.schema import SchemaError


class RunTimeEnv():
    """ Stores all information during loading schemas and data validations. """
    def __init__(self,
                namespace: str=None,
                data_types: dict=None,
                allow_shortcuts: bool=False
                ) -> None:
        """
        Args:
            namespace: string - Initial namespace

            data_types: dictionary
                with data type name as key and data type class as value

            allow_shortcuts: bool - Allow data type shortcuts in schemas
        """
        self.allow_shortcuts = allow_shortcuts
        self.references = References()
        self.namespace = ''
        if namespace is not None:
            self.change_namespace(namespace)
        self.data_types = dict()
        if data_types:
            self.load_data_types(data_types)
        try:
            from ruamel.yaml import CommentedMap, CommentedSeq
            self.ruamel_yaml_available = True
            self.CommentedMap = CommentedMap
            self.CommentedSeq = CommentedSeq
        except ImportError:
            self.ruamel_yaml_available = False


        
    def change_namespace(self, namespace :str) -> None:
        """
        Args:
            namespace: string - New namespace
        """
        if not isinstance(namespace, str):
            raise ValueError('namespace has to be a string')
        self.references.change_namespace(namespace)
        self.namespace = namespace

    def load_data_type(self, type_name :str, type_class :DataType) -> None:
        """ Load/Add a data type to the run time environment

        Args:
            type_name: string - Data type name

            type_class: class - A sub-class to DataType

        Raises:
            ValueError:
                - If type_name already registered in run time environment
                - If type_class is not a sub-class to DataType
        """
        if type_name in self.data_types.keys():
            raise ValueError("Data type '%s' already loaded" % type_name)
        if not issubclass(type_class, DataType):
            raise ValueError("Loading %s failed - not %s" % (type_class, DataType))
        self.data_types[type_name] = type_class

    def load_data_types(self, data_types :dict) -> None:
        """ Load/Add a multiple data types to the run time environment

        Args:
            data_types: dictionary
                with data type name as key and data type class as value
        
        Raises:
            ValueError: If data_types is not a dictionary
        """
        if not isinstance(data_types, dict) :
            raise ValueError("'data_types' must be a dictionary")
        for type_name, type_class in data_types.items():
            self.load_data_type(type_name, type_class)
    
    def get_data_type_class(self, data_type_name: str) -> DataType:
        """ Returns data type class for given data type name

        Args:
            data_type_name: string
        
        Raises:
            SchemaError: If data type name is not found in run tinme environment

        Returns:
            Corresponding DataType sub-class for given data type name
        """
        if data_type_name not in self.data_types:
            raise SchemaError("Data type '%s' not found" % str(data_type_name))
        return self.data_types[data_type_name]
