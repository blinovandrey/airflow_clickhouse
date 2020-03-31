import logging
import os
from datetime import datetime

from airflow.models import DAG, Variable

from src.operators.clickhouse_operator import ClickHouseOperator

logger = logging.getLogger(__name__)


dag = DAG(
    dag_id='main',
    catchup=False,
    start_date=datetime(2020, 3, 31),
    schedule_interval='0 1 * * *',
)


def read_data():
    with open(Variable.get('EVENTS_JSON_PATH')) as f:
        for line in f:
            yield dict(data=line)


def get_clickhouse_host():
    return Variable.get('CLICKHOUSE_HOST')


def get_raw_data_to_events_sql():
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           'sql_scripts/raw_data_to_events.sql'), 'r') as f:
        sql = f.read()
    return sql


load_raw_data = ClickHouseOperator(
    dag=dag,
    task_id='load_raw_data',
    clickhouse_host=get_clickhouse_host(),
    sql="INSERT INTO raw_data VALUES",
    data_generator_fn=read_data
)


raw_data_to_events = ClickHouseOperator(
    dag=dag,
    task_id='raw_data_to_events',
    clickhouse_host=get_clickhouse_host(),
    sql=get_raw_data_to_events_sql()
)

load_raw_data >> raw_data_to_events
