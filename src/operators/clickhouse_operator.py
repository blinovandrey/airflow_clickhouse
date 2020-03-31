from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from clickhouse_driver import Client


class ClickHouseOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 clickhouse_host,
                 sql,
                 data_generator_fn=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.clickhouse_host = clickhouse_host
        self.sql = sql
        self.data_generator_fn = data_generator_fn

    def get_client(self) -> Client:
        return Client(self.clickhouse_host)

    def execute(self, context):
        client = self.get_client()
        if self.data_generator_fn:
            result = client.execute(self.sql, (line for line in self.data_generator_fn()))
        else:
            result = client.execute(self.sql)
        return result
