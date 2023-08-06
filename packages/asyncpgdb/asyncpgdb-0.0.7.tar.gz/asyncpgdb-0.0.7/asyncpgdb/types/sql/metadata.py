from sqlmodel.main import MetaData
from sqlmodel.main import Column


class CreateColumnSQL(str):
    @classmethod
    def parse_column(
        cls,
        column: Column,
        non_null: bool = True,
        serial: bool = False,
        primary_key: bool = False,
        echo: bool = False,
    ):
        column_name = column.name
        stmt = f"{column_name}"
        if serial:
            stmt += f" SERIAL"
        if primary_key:
            stmt += f" PRIMARY KEY"
        else:
            stmt += f" {str(column.type)}"

        if non_null:
            stmt += " NOT NULL"
        if echo:
            print(f"asyncpgdb.types.sql.metadata.CreateColumnSQL:: {column_name}")
        return cls(stmt)


from sqlmodel import Column


class CreateTableSQL(str):
    @classmethod
    def parse_table(cls, table, echo: bool = False):
        columns = []
        table_name = table.name

        for column in table.columns:
            column: Column = column
            non_null = True
            serial = False
            primary_key = False
            if column.primary_key:
                if str(column.type).strip().lower().startswith("int"):
                    primary_key = True
                    non_null = False
                    serial = True
            column_sql = CreateColumnSQL.parse_column(
                column=column,
                non_null=non_null,
                serial=serial,
                primary_key=primary_key,
                echo=echo,
            )
            columns.append(column_sql)

        columns = ",\n".join(columns)

        while ",," in columns:
            columns = columns.replace(",,", ",")
        stmt = f"CREATE TABLE IF NOT EXISTS {table_name} (\n{columns}\n);"
        if echo:
            print(f"asyncpgdb.types.sql.metadata.CreateTableSQL:: {table_name}")
        result = cls(stmt)

        return result


class DropTableSQL(str):
    @classmethod
    def parse_table(cls, table, echo: bool = False):
        table_name = table.name
        stmt = f"DROP TABLE IF EXISTS {table_name};"
        if echo:
            print(f"asyncpgdb.types.sql.metadata.DropTableSQL:: {table_name}")

        return cls(stmt)


class CreateDatabaseSQL(str):
    @classmethod
    def parse_metadata(cls, metadata: MetaData, echo: bool = False):
        parse_table = lambda table: CreateTableSQL.parse_table(table=table, echo=echo)
        stmt = "\n".join(map(parse_table, metadata.tables.values()))
        if echo:
            print(f"asyncpgdb.types.sql.metadata.CreateDatabaseSQL:: {stmt}")
        return cls(stmt)

    def compile(self):
        return str(self).encode(encoding="utf-8").decode(encoding="utf-8")


class DropDatabaseSQL(str):
    @classmethod
    def parse_metadata(cls, metadata: MetaData, echo: bool = False):
        parse_table = lambda table: DropTableSQL.parse_table(table=table, echo=echo)
        stmt = "\n".join(map(parse_table, metadata.tables.values()))
        if echo:
            print(f"asyncpgdb.types.sql.metadata.DropDatabaseSQL:: {stmt}")
        return cls(stmt)

    def compile(self):
        return str(self).encode(encoding="utf-8").decode(encoding="utf-8")
