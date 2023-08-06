import asyncpg
from asyncpg.pool import Pool
from asyncpg.connection import Connection
from typing import Any
from typing import Union
from typing import Optional
import dataclasses as dc
from pydantic import BaseConfig
from asyncpgdb.types.dsn import DatabaseDSN
from asyncpgdb.types.sql.stmt import SQLStmt
from .maps import SomeSchema


@dc.dataclass(frozen=False, order=True)
class ConnectionPool:

    dsn: DatabaseDSN = dc.field()
    min_size: int = dc.field()
    max_size: int = dc.field()
    is_connected: bool = dc.field()
    is_initialized: bool = dc.field()
    pool: Optional[Pool] = dc.field(default=None)
    connection: Optional[Connection] = dc.field(default=None)

    @classmethod
    def __init__(
        self,
        dsn: DatabaseDSN,
        min_size: int = 5,
        max_size: int = 10,
        pool: Optional[Pool] = None,
        connection: Optional[Connection] = None,
        is_initialized: bool = False,
        is_connected: bool = False,
    ):

        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.is_initialized = is_initialized
        self.pool = pool
        self.connection = connection
        self.is_connected = is_connected

    async def init_pool(self):
        if not self.is_initialized:
            dsn = self.dsn
            min_size = self.min_size
            max_size = self.max_size
            self.pool = await asyncpg.create_pool(
                dsn=dsn, min_size=min_size, max_size=max_size
            )
            self.is_initialized = True

    async def connect(self):
        if not self.is_connected:
            await self.init_pool()
            self.connection: Connection = await self.pool.acquire()
            self.is_connected = True

    async def close(self):
        if self.is_connected:
            if not self.connection.is_closed():
                await self.connection.close()
            self.is_connected = False
            await self.pool.release(self.connection)

    def compile_stmt(self, __stmt: Union[SQLStmt, str]):
        _stmt = __stmt.compile() if isinstance(__stmt, SQLStmt) else str(__stmt)

        return _stmt

    async def execute(
        self,
        stmt: SQLStmt,
        vars: Optional[Union[list[dict], list[SomeSchema]]] = None,
        timeout: Optional[float] = None,
    ):
        query = self.compile_stmt(stmt)

        await self.connect()
        try:
            if vars:
                result = await self.connection.execute(query, *vars, timeout=timeout)
            else:
                result = await self.connection.execute(query, timeout=timeout)
        except BaseException as error:
            result = f"error: {str(error)}"
        finally:
            await self.close()
        return result

    async def executemany_raw(
        self,
        stmt: str,
        vars: Optional[Union[list[dict], list[SomeSchema]]] = None,
        timeout: Optional[float] = None,
    ):
        query = self.compile_stmt(stmt)
        await self.connect()
        try:
            if vars:
                result = await self.connection.executemany(
                    query, args=vars, timeout=timeout
                )
            else:
                result = await self.connection.executemany(query, timeout=timeout)
        except BaseException as error:
            result = f"executemany_raw.error:\n\n{str(error)}\n\n"
        finally:
            await self.close()
        return result

    async def execute_raw(
        self,
        stmt: str,
        vars: Optional[Union[list[dict], list[SomeSchema]]] = None,
        timeout: Optional[float] = None,
    ):
        query = self.compile_stmt(stmt)
        await self.connect()
        try:
            if vars:
                result = await self.connection.execute(query, *vars, timeout=timeout)
            else:
                result = await self.connection.execute(query, timeout=timeout)
        except BaseException as error:
            result = f"execute_raw.error:\n\n{str(error)}\n\n"
        finally:
            await self.close()
        return result

    async def fetchall(
        self,
        stmt: SQLStmt,
        as_dicts: bool = True,
        whereclause: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        query = self.compile_stmt(stmt.where(whereclause=whereclause).limit(n=limit))

        await self.connect()
        try:
            data = await self.connection.fetch(query, timeout=timeout)
        except:
            data = []
        finally:
            await self.close()
        if data:
            format_row = stmt.serializer(as_dicts=as_dicts)
            format_data = lambda __data: list(map(format_row, __data))
            data = format_data(data)
        return data

    async def iterrows(
        self,
        stmt: SQLStmt,
        as_dicts: bool = True,
        whereclause: Optional[str] = None,
        limit: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        query = self.compile_stmt(stmt.where(whereclause=whereclause).limit(n=limit))

        await self.connect()
        try:
            format_row = stmt.serializer(as_dicts=as_dicts)
            transaction = self.connection.transaction(readonly=True)
            await transaction.start()
            cursor = self.connection.cursor(query)
            async for row in cursor:
                yield format_row(row)

        except BaseException as error:
            result = f"iterrows.error:\n\n{str(error)}\n\n"
            print(result)
        finally:
            await self.close()

    async def fetchone(
        self,
        stmt: SQLStmt,
        as_dicts: bool = True,
        whereclause: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        query = stmt.where(whereclause=whereclause).limit(n=limit)
        query = self.compile_stmt(query)
        await self.connect()
        try:
            data = await self.connection.fetchrow(query=query)
        except:
            data = None
        finally:
            await self.close()
        if data:
            format_row = stmt.serializer(as_dicts=as_dicts)
            format_data = format_row
            data = format_data(data)
        return data

    async def upsert(
        self,
        stmt: SQLStmt,
        vars: Optional[Union[list[dict], list[SomeSchema]]] = None,
        timeout: Optional[float] = None,
    ):

        query = self.compile_stmt(stmt)
        if vars:
            vars = stmt.format_vars(vars=vars)

            await self.connect()

            try:

                result = await self.connection.executemany(
                    query, args=vars, timeout=timeout
                )
                result = "success"

            except BaseException as error:
                result = f"upsert.error: {str(error)}"
            finally:
                await self.close()
        else:
            result = "error: no vars to upsert"
        return result

    async def insert(
        self,
        stmt: SQLStmt,
        vars: Optional[Union[list[dict], list[SomeSchema]]] = None,
        timeout: Optional[float] = None,
    ):

        result = await self.upsert(stmt=stmt, vars=vars, timeout=timeout)
        return result


def __singleton_protocol__(cls):
    instance = [None]

    def __inner__(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return __inner__


@__singleton_protocol__
class SingletonConnectionPool(ConnectionPool):
    pass
