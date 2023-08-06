import asyncpg
from asyncpg.pool import Pool
from asyncpg.connection import Connection
from typing import Any
from typing import Union
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseConfig
from asyncpgdb.types.dsn import DatabaseDSN
from asyncpgdb.types.sql.stmt import SQLStmt
from .maps import SomeSchema


class ConnectionPool(BaseModel):
    class Config(BaseConfig):
        arbitrary_types_allowed = True

    dsn: DatabaseDSN
    min_size: int
    max_size: int
    is_connected: bool
    is_initialized: bool
    pool: Optional[Pool]
    connection: Optional[Connection]

    @classmethod
    def init(
        cls,
        dsn: DatabaseDSN,
        min_size: int = 5,
        max_size: int = 10,
        pool: Optional[Pool] = None,
        connection: Optional[Connection] = None,
        is_initialized: bool = False,
        is_connected: bool = False,
    ):

        return cls(
            dsn=dsn,
            min_size=min_size,
            max_size=max_size,
            is_initialized=is_initialized,
            pool=pool,
            connection=connection,
            is_connected=is_connected,
        )

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
        except:
            result = "error"
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
            result = f"execute_raw.error:\n\n{str(error)}\n\n"
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
        await self.close()
        return data

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
        await self.close()
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
            print("UPSERT VARS:", vars)

            await self.connect()

            try:

                result = await self.connection.executemany(
                    query, args=vars, timeout=timeout
                )
                result = "success"

            except:
                result = "error"
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
