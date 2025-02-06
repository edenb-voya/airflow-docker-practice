from airflow.models import Variable
from datetime import datetime, timedelta

import pandas as pd
import json
import csv

from airflow.operators.postgres_operator import PostgresOperator

from airflow.utils.dates import days_ago
from airflow.decorators import dag, task

default_args = {
    'owner': 'airflow'
}

@dag(
    dag_id='data_transformation_storage_pipeline',
    description='Data transformation and storage pipeline',
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval='@once',
    tags=['postgresql', 'python', 'taskflow_api', 'xcoms']
)
def data_transformation_storage_pipeline():

    @task
    def read_dataset():
        df = pd.read_csv('/opt/airflow/datasets/car_data.csv')

        return df.to_json()
    
    @task
    def create_table():
        postgres_operator = PostgresOperator(
            task_id='create_table',
            postgres_conn_id='postgres_conn',
            sql="""CREATE TABLE IF NOT EXISTS car_data (
                    id SERIAL PRIMARY KEY,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL,
                    body_style TEXT NOT NULL,
                    seat INT NOT NULL,
                    price INT NOT NULL);"""
        )

        postgres_operator.execute(context=None)

    @task
    def insert_selected_data(**kwargs):
        ti = kwargs['ti']

        json_data = ti.xcom_pull(task_ids='read_dataset')

        df = pd.read_json(json_data)

        df = df[['Brand', 'Model', 'Bodystyle', 'Seats', 'PriceEuro']]

        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        insert_query = """
            INSERT INTO car_data (brand, model, body_style, seat, price)
            VALUES (?, ?, ?, ?, ?)
        """

        parameters = df.to_dict(orient='records')

        for record in parameters:
            postgres_operator = PostgresOperator(
                task_id='insert_data',
                postgres_conn_id='postgres_conn',
                sql=insert_query,
                parameters=tuple(record.values()),
            )

            postgres_operator.execute(context=None)
    
    read_dataset() >> create_table() >> insert_selected_data()

data_transformation_storage_pipeline()