# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import



class EntityName(type):

    @property
    def name(self):
        '''
            Get this EntityName's name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-11-2023 14:32:58
            `@memberOf`: EntityName
            `@property`: name
        '''
        value = self._name
        if value is None:
            if hasattr(self,"__table_name__"):
                value = getattr(self,"__table_name__")
            self._name = value
        return value