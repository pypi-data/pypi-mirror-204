from elasticapm.instrumentation.packages.dbapi2 import (
    ConnectionProxy,
    CursorProxy,
    DbApi2Instrumentation,
    extract_signature,
)
from elasticapm.instrumentation import register


class OracleCursorProxy(CursorProxy):
    provider_name = "oracle"

    def extract_signature(self, sql):
        return extract_signature(sql)


class OracleConnectionProxy(ConnectionProxy):
    cursor_proxy = OracleCursorProxy


class OracleInstrumentation(DbApi2Instrumentation):
    name = "oracle"

    instrument_list = [("cx_Oracle", "connect")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        return OracleConnectionProxy(wrapped(*args, **kwargs))


register.register("ora.OracleInstrumentation")
