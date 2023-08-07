"""JSON HELPER CLASS """
import ast
class JsonHelper:
    """ Helper class for converting dictionary to JSON """
    def __init__(self, dictionary):
        self.__json_string = str(dictionary)

    def convert_to_json(self):
        """
        function to convert dictionary to json
        """
        self.__json_string = (\
                              self.__json_string[1:-1]
                              .replace(" '[", "[")
                              .replace("]', ", "],")
                              .replace("]'", "]")
                              .replace("'", '"')
                             )
        return self.__json_string

    async def filter_none_keys(self, __keys):
        """ function to filter None value keys
        """
        __json_dictionary = self.convert_to_json()
        __json_dictionary = ast.literal_eval(__json_dictionary)
        __filter_none_keys = {k: v for k, v in __json_dictionary.items()
                              if v is not None}
        __json_dictionary.clear()
        __json_dictionary.update(__filter_none_keys)
        __json_dictionary_keys = list(__json_dictionary.keys())
        if sorted(__json_dictionary_keys) == sorted(__keys):
            __all_required_keys = True
        else:
            __all_required_keys = False

        __json_data = str(__json_dictionary)
        __json_data = __json_data.replace("'", '"')
        return(__json_data, __all_required_keys)
