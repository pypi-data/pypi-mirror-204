from typing import TYPE_CHECKING,TypeVar as _TypeVar


# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

_main_type = None
model_type = None
database_type = None
column_type = None
type_base_type = None
query_type = None

relationship_type = None
schema_type = None
field_type = None
unique_constraint_type = None



if TYPE_CHECKING:

    from volent.Volent import Volent as _m
    _main_type = _TypeVar('_main_type', bound=_m)

    from volent.Column import Column as _OXC0
    column_type = _TypeVar('column_type', bound=_OXC0)

    from volent.Model import Model as _HFem
    model_type = _TypeVar('model_type', bound=_HFem)

    from volent.Database import Database as _e8Ig
    database_type = _TypeVar('database_type', bound=_e8Ig)


    from volent.data_types.TypeBase import TypeBase as _NZwn
    type_base_type = _TypeVar('type_base_type', bound=_NZwn)

    from volent.Relationship import Relationship as _gt25
    relationship_type = _TypeVar('relationship_type', bound=_gt25)


    from volent.Schema import Schema as _gmhq
    schema_type = _TypeVar('schema_type', bound=_gmhq)

    from volent.Field import Field as _zoTC
    field_type = _TypeVar('field_type', bound=_zoTC)

    from volent.UniqueConstraint import UniqueConstraint as _xbst
    unique_constraint_type = _TypeVar('unique_constraint_type', bound=_xbst)


    from volent.query.Query import Query as _PsBw
    query_type = _TypeVar('query_type', bound=_PsBw)


class NoDefault:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Undefined:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    # def __repr__(self) -> str:
    #     return f"<{self.__class__.__name__} : {self.value}>"
no_default = NoDefault("__NO_DEFAULT_PROVIDED__")
undefined = Undefined("__UNDEFINED_VALUE__")






