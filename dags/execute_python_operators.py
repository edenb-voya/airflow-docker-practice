import time

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago

from airflow import DAG

from airflow.operators.python import PythonOperator

default_args = {
    'owner' : 'airflow'
}

def greet_hello(name):
    print("Hello, {name}!".format(name=name))

def greet_hello_with_city(name, city):
    print("Hello, {name} from {city}".format(name=name, city=city))


with DAG(
    dag_id = 'execute_python_operators',
    description = 'Python operators in DAGs',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@daily',
    tags = ['simple', 'python']
) as dag:
    taskA = PythonOperator(
        task_id = 'taskA',
        python_callable = task_a
    )

    taskB = PythonOperator(
        task_id = 'taskB',
        python_callable = task_b
    )

    taskC = PythonOperator(
        task_id = 'taskC',
        python_callable = task_c
    )

    taskD = PythonOperator(
        task_id = 'taskD',
        python_callable = task_d
    )

taskA >> [taskB, taskC]
[taskB, taskC] >> taskD