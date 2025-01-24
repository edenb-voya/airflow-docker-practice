from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow import DAG 

from airflow.operators.bash import BashOperator

default_args = {
    'owner' : 'airflow'
}

date_seven_days_ago = datetime.now() - timedelta(days=7)
iso_format_date = date_seven_days_ago.isoformat()

dag = DAG(
    dag_id = 'hello_world',
    description = 'Our first "Hello World" DAG!',
    default_args = default_args,
    start_date = iso_format_date,
    schedule_interval = None
)

task = BashOperator(
    task_id = 'hello_world_task',
    bash_command = 'echo Hello world!',
    dag = dag
)

task 