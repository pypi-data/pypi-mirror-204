from typing import Optional
from typing import Type
from typing import Union
from dataclasses import dataclass, field
from asyncpgdb.types.maps import SomeSchema
from asyncpgdb.types.maps import SomeModel


@dataclass(frozen=False, order=True)
class SQLStmt(str):

    dtype: Type[Union[SomeSchema, SomeModel]] = field()
    stmt: str = field()

    def __init__(
        self,
        __stmt: str,
        __dtype: Optional[Union[Type[SomeSchema], Type[SomeModel]]] = None,
    ):
        self.stmt = __stmt
        self.dtype = __dtype

    def compile(self):
        return self.stmt

    def __prepare__(self):
        return self.compile().removesuffix(";")

    def limit(self, n: Optional[int] = None):
        if n:
            stmt = self.__prepare__()
            stmt += f" LIMIT {n};"
            stmt = SQLStmt(stmt, self.dtype)
        else:
            stmt = self
        return stmt

    def where(self, whereclause: Optional[str] = None):
        if whereclause:
            whereclause = whereclause.lstrip().removeprefix("WHERE ").removesuffix(";")
            if whereclause:
                stmt = self.__prepare__()
                stmt += f" WHERE {whereclause};"
                stmt = SQLStmt(stmt, self.dtype)
            else:
                stmt = self
        else:
            stmt = self
        return stmt

    def serializer(self, as_dicts: bool = True):
        if self.dtype:
            if as_dicts:
                result = self.dtype.row2dict_serializer()
            else:
                result = self.dtype.row2schema_serializer()
        else:
            result = None
        return result

    def format_vars(
        self, vars: Union[list[dict], list[SomeSchema]], include_null: bool = True
    ):
        if self.dtype:

            result = self.dtype.format_upsert_vars(vars=vars, include_null=include_null)
        else:
            print("UNABLE TO FORMAT VARS: UNKNOWN DTYPE:")
            result = vars
        return result


def select(
    __dtype: Union[Type[SomeSchema], Type[SomeModel]],
    tablename: Optional[str] = None,
    whereclause: Optional[str] = None,
    limit: Optional[int] = None,
):
    tablename = __dtype.tablename(tablename=tablename)
    fields = ", ".join(__dtype.__fields__)
    stmt = f"SELECT {fields} FROM {tablename}"
    if whereclause:
        stmt += f" WHERE {whereclause}"
    if limit:
        stmt += f" LIMIT {limit}"
    stmt += ";"
    return stmt


def upsert(
    __dtype: Union[Type[SomeSchema], Type[SomeModel]], tablename: Optional[str] = None
):
    tablename = __dtype.tablename(tablename=tablename)
    pk = __dtype.primary_key()
    if pk is None:
        raise BaseException(f"No primary key exists for {str(__dtype)}")
    pk = str(pk.name)
    fieldnames = [field for field in __dtype.__fields__]

    insert_args = []
    on_conflict_args = []

    for (i, fieldname) in enumerate(fieldnames):
        insert_arg = f"${i+1}"
        if fieldname != pk:
            on_conflict_arg = f"{fieldname} = excluded.{fieldname}"
            on_conflict_args.append(on_conflict_arg)
        insert_args.append(insert_arg)
    insert_args = ",\n".join(insert_args)
    on_conflict_args = ",\n".join(on_conflict_args)
    fieldnames = ",".join(fieldnames)
    return f"INSERT INTO {tablename} ({fieldnames}) VALUES ({insert_args}) ON CONFLICT ({pk}) DO UPDATE SET {on_conflict_args}\n;"


def insert(
    __dtype: Union[Type[SomeSchema], Type[SomeModel]], tablename: Optional[str] = None
):
    return upsert(__dtype, tablename=tablename)


class Select(SQLStmt):
    def __init__(
        self,
        __dtype: Union[Type[SomeSchema], Type[SomeModel]],
        tablename: Optional[str] = None,
    ):

        self.stmt = select(__dtype, tablename=tablename)
        self.dtype = __dtype


class Upsert(SQLStmt):
    def __init__(
        self,
        __dtype: Union[Type[SomeSchema], Type[SomeModel]],
        tablename: Optional[str] = None,
    ):
        self.stmt = upsert(__dtype, tablename=tablename)
        self.dtype = __dtype


class Insert(SQLStmt):
    def __init__(
        self,
        __dtype: Union[Type[SomeSchema], Type[SomeModel]],
        tablename: Optional[str] = None,
    ):
        self.stmt = insert(__dtype, tablename=tablename)
        self.dtype = __dtype
