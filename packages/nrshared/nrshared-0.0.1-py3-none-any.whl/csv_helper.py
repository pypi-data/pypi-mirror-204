
class CsvHelper:
    """ Helper class for converting to CSV """
    def __init__(self, list_param):
        self.__list = list_param

    async def convert_list_to_csv(self):
        """ Convert list parameter to comma separated string """
        __csv = None
        if isinstance(self.__list, list):
            if all(isinstance(x, int) for x in self.__list):
                __csv = ",".join([str(i) for i in self.__list])
            else:
                raise Exception("Invalid parameters sent")            
        return __csv or None