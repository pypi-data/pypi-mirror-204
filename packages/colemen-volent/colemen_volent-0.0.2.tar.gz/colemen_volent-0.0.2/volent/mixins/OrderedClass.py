# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from typing import Iterable, OrderedDict, Union
from collections import OrderedDict
import colemen_utils as c


class OrderedClass(type):
    @classmethod
    def __prepare__(mcs, name, bases): 
        return OrderedDict()




    def __setattr__(self, name, value):
        super().__setattr__(name, value)

        if not name in self._order:
            self._order.append(name)



        return value

    def ordered_attrs(self, with_order=False):
        return [(k,getattr(self, k)) for k in self._order if k != '_order' or with_order]


    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result._order = []
        return result

    # def __new__(cls, name, bases, classdict):
    #     # print(f"classdict:{classdict}")
    #     result = type.__new__(cls, name, bases, dict(classdict))
    #     result.__odict__ = OrderedDict()
    #     result.__odict__ = list(classdict.keys())
    # #     print(f"result.__init__.__dict__:{result.__init__.}")
    # #     # result.__columns__ = []
    # #     print("-"*80)
    # #     print(result.__dict__)
    # #     print("-"*80)

    # #     # value = []
    # #     # from volent.Column import Column as _column
    # #     # for prop in list(classdict.keys()):
    # #     #     name = prop

    # #     #     val = classdict[prop]
    # #     #     # print(f"{prop} - prop type: {type(val)}")
    # #     #     if isinstance(val,(_column)):
    # #     #         c.con.log(f"OrderedClass.located Column: {name}","green")
    # #     #         val.name = name
    # #     #         val.model = result
    # #     #         if val.is_primary is True:
    # #     #             result.primary_column = val
    # #     #         value.append(val)
                
    # #     #         setattr(result,name,val)

            
    # #         # if isinstance(prop,(list)):
    # #         #     # print(f"prop is a list")
    # #         #     vals = classdict[prop]
    # #         #     for val in vals:
    # #         #         print(f"val:{val}")
    # #         #         if val.name == name:
    # #         #     # val = classdict[prop]
    # #         #     # print(f"{name} - val: {value}")
    # #         #             if isinstance(val,(_column)):
    # #         #                 c.con.log(f"OrderedClass.located Column: {name}","green")
    # #         #                 val.name = name
    # #         #                 val.model = result
    # #         #                 if val.is_primary is True:
    # #         #                     result.primary_column = val
    # #         #                 value.append(val)
    # #         #                 setattr(result,name,val)

        
    # #     # if len(value) == 0:
    # #     #     value = None
        
    # #     # result.title.value = "boobers"
    # #     # result._columns = value
    # #     # result.boobs = "tiddies"
    # #     return result
    
    
    
    # # def __new__(cls, *args, **kwargs):
    # #     instance = type.__new__(cls)
    # #     instance.__odict__ = OrderedDict()
    # #     return instance

    # def __setattr__(self, key, value):
    #     if key != '__odict__':
    #         self.__odict__[key] = value
    #     object.__setattr__(self, key, value)

    # def keys(self):
    #     return self.__odict__.keys()

    # def iteritems(self):
    #     return self.__odict__.iteritems()


