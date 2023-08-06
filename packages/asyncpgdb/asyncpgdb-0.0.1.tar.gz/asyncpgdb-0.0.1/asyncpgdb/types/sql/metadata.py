from sqlmodel.main import MetaData
from sqlmodel.main import Column


class PrimaryKeySQL(str):
    @classmethod
    def parse_column(cls, column: Column):
        return cls(f"PRIMARY KEY ({column.name})")


class CreateColumnSQL(str):
    @classmethod
    def parse_column(cls, column: Column):
        return cls(f"{column.name} {str(column.type)} NOT NULL")


class CreateTableSQL(str):
    @classmethod
    def parse_table(cls, table):
        columns = []
        primary_key = None
        for column in table.columns:
            columns.append(CreateColumnSQL.parse_column(column))
            if column.primary_key and not primary_key:
                primary_key = column

        columns = ",\n".join(columns)

        if primary_key is not None:
            column = PrimaryKeySQL.parse_column(primary_key)
            columns += f",\n{column}"
        while ",," in columns:
            columns = columns.replace(",,", ",")
        return cls(f"CREATE TABLE IF NOT EXISTS {table.name} (\n{columns}\n);")


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
