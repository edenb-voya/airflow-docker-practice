import time

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow import DAG

from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'airflow'
}

def increment_by_1(counter):
    print("Count {counter}!".format(counter=counter))

    return counter + 1

def multilpy_by_100(counter):
    print("Count {counter}!".format(counter=counter))

    return counter * 100


with DAG(
    dag_id = 'cross_task_communication',
    description = 'Cross-task communication with XCom',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@daily',
    tags = ['xcom', 'python']
) as dag:
    taskA = PythonOperator(
        task_id = 'increment_by_1',
        python_callable = increment_by_1,
        op_kwargs={'counter': 100}
    )

    taskB = PythonOperator(
        task_id = 'multiply_by_100',
        python_callable = greet_hello_with_city,
        op_kwargs={'counter': 9}
    )

taskA >> taskB