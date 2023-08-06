from pydantic import validate_arguments
from typing import Optional

class FromDictList:
    @validate_arguments
    def __init__(self, list_: list[dict]):
        self.__list = list_

    @validate_arguments
    def get_with_key_value(self, key, value) -> Optional[dict]:
        for x in  self.__list:

            if x[key] == value:
                return x

    @validate_arguments
    def get_with_key(self, key) -> Optional[dict]:
        for x in  self.__list:

            if key in x.keys():
                return x
    
    @validate_arguments
    def filter_with_key_values(self, key, values: list) -> list[dict]:
        dicts = []

        for value in values:
            for x in self.__list:
                if x[key] == value:
                    dicts.append(x)

        return dicts

    @validate_arguments
    def filter_with_keys(self, keys: list) -> list[dict]:
        dicts = []

        for key in keys:
            for x in self.__list:
                if key in x.keys():
                    dicts.append(x)

        return dicts

    @validate_arguments
    def filter_with_key_value(self, key, value) -> list[dict]:
        dicts = [ x for x in  self.__list if x[key] == value ]
        return dicts

    @validate_arguments
    def filter_with_key(self, key) -> list[dict]:
        dicts = [ x for x in  self.__list if key in x.keys() ]
        return dicts
    
    @validate_arguments
    def for_each_dict_pop_keys(self, keys: list) -> list[dict]:
        new_list = []

        for x in self.__list:
            for key in keys:
                x.pop(key)

            new_list.append(x)

        return new_list

    @validate_arguments
    def merge_dicts(self) -> dict:
        new_dict = {}

        for x in self.__list:
            for key in x.keys():
                if not key in new_dict.keys():
                    new_dict[key] = x[key]

                else:
                    raise Exception(f"Duplicate key: {key}")

        return new_dict

    @validate_arguments
    def categorize_dicts_by_key_value(self, key) -> dict[str, list]:
        dict_: dict[str, list] = {}

        for x in self.__list:
            new_key = x[key]
            
            if new_key in dict_:
                dict_[new_key].append(x)

            else:
                dict_[new_key] = []
                dict_[new_key].append(x)

        return dict_

__all__ = [ "FromDictList" ]