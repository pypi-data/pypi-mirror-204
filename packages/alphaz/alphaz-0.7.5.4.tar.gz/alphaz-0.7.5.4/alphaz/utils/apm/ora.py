from elasticapm.instrumentation.packages.dbapi2 import (
    ConnectionProxy,
    CursorProxy,
    DbApi2Instrumentation,
    extract_signature,
)
from elasticapm.instrumentation import register
from elasticapm.utils import default_ports


class OracleCursorProxy(CursorProxy):
    provider_name = "oracle"

    def extract_signature(self, sql):
        return extract_signature(sql)

    @property
    def _self_database(self) -> str:
        # for unknown reasons, the connection is available as the `_connection` attribute on Python 3.6,
        # and as `_cnx` on later Python versions
        return self.connection.dsn.split("SID=")[1].split(")")[0]
        # connection = getattr(self, "_cnx") or getattr(self, "_connection")
        # return connection.database if connection else ""


class OracleConnectionProxy(ConnectionProxy):
    cursor_proxy = OracleCursorProxy


class OracleInstrumentation(DbApi2Instrumentation):
    name = "oracle"

    instrument_list = [("cx_Oracle", "connect")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        destination_info = {
            "address": kwargs["dsn"].split("HOST=")[1].split(")")[0],
            "port": int(kwargs["dsn"].split("PORT=")[1].split(")")[0]),
        }
        return OracleConnectionProxy(
            wrapped(*args, **kwargs), destination_info=destination_info
        )


register.register("alphaz.utils.apm.ora.OracleInstrumentation")
