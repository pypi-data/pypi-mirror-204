from typing import Optional


class DatabaseDSN(str):
    @classmethod
    def parse_connection_args(
        cls,
        dsn: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        dbname: Optional[str] = None,
    ):
        """
        dsn template:
            postgres://{user}:{password}@{host}:{port}/{dbname}
        """

        _dsn = ""
        if dsn:
            _dsn = dsn
        else:
            assert user is not None, "no user provided"
            assert host is not None, "no host provided"
            assert dbname is not None, "no dbname provided"
            _dsn = f"postgres://"
            if user:
                _dsn += user
            if password:
                _dsn += f":{password}"
            _dsn += "@"
            if host:
                _dsn += host
            if port is not None:
                _dsn += f":{port}"
            if dbname:
                _dsn += f"/{dbname}"
        return cls(_dsn)
