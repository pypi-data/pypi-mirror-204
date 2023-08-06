from typing import Optional
from sqlmodel.main import MetaData
from sqlmodel.main import Column


class PrimaryKeySQL(str):
    @classmethod
    def parse_column(cls, column: Column):
        return cls(f"PRIMARY KEY ({column.name})")


class CreateColumnSQL(str):
    @classmethod
    def parse_column(
        cls,
        column: Column,
        non_null: bool = True,
        serial: bool = False,
        primary_key: bool = False,
    ):
        result = f"{column.name}"
        if serial:
            result += f" SERIAL"
        if primary_key:
            result += f" PRIMARY KEY"
        else:
            result += f" {str(column.type)}"

        if non_null:
            result += " NOT NULL"
        return cls(result)


from sqlmodel import Column


class CreateTableSQL(str):
    @classmethod
    def parse_table(cls, table):
        columns = []

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
                column=column, non_null=non_null, serial=serial, primary_key=primary_key
            )
            columns.append(column_sql)

        columns = ",\n".join(columns)

        while ",," in columns:
            columns = columns.replace(",,", ",")
        result = cls(f"CREATE TABLE IF NOT EXISTS {table.name} (\n{columns}\n);")
        print("RESULT:", result)
        return result


class DropTableSQL(str):
    @classmethod
    def parse_table(cls, table):
        return cls(f"DROP TABLE IF EXISTS {table.name};")


class CreateDatabaseSQL(str):
    @classmethod
    def parse_metadata(cls, metadata: MetaData):
        return cls("\n".join(map(CreateTableSQL.parse_table, metadata.tables.values())))

    def compile(self):
        return str(self, encoding="utf-8")


class DropDatabaseSQL(str):
    @classmethod
    def parse_metadata(cls, metadata: MetaData):
        return cls("\n".join(map(DropTableSQL.parse_table, metadata.tables.values())))

    def compile(self):
        return str(self, encoding="utf-8")
