from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.models import Variable

import pandas as pd
import json
import csv

from airflow.providers.postgres.operators.postgres import PostgresOperator

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
    def read_car_data():
        df = pd.read_csv('/opt/airflow/datasets/car_data.csv')

        return df.to_json()
    
    @task
    def read_car_categories_data():
        df = pd.read_csv('/opt/airflow/datasets/car_categories.csv')

        return df.to_json()

    @task
    def create_table_car_data():
        postgres_operator = PostgresOperator(
            task_id='create_table_car_data',
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
    def create_table_car_categories_data():
        postgres_operator = PostgresOperator(
            task_id='create_table_car_categories_data',
            postgres_conn_id='postgres_conn',
            sql="""CREATE TABLE IF NOT EXISTS car_categories (
                    id SERIAL PRIMARY KEY,
                    brand TEXT NOT NULL,
                    category TEXT NOT NULL);"""
        )
        postgres_operator.execute(context=None)

    @task
    def insert_car_data(**kwargs):
        ti = kwargs['ti']

        json_data = ti.xcom_pull(task_ids='read_car_data')

        df = pd.read_json(json_data)

        df = df[['Brand', 'Model', 'BodyStyle', 'Seats', 'PriceEuro']]

        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        insert_query = """
            INSERT INTO car_data (brand, model, body_style, seat, price)
            VALUES (%s, %s, %s, %s, %s)
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

    @task
    def insert_car_categories_data(**kwargs):
        ti = kwargs['ti']

        json_data = ti.xcom_pull(task_ids='read_car_categories_data')

        df = df[['Brand', 'Category']]

        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        insert_query = """
            INSERT INTO car_categories (brand, category)
            VALUES (%s, %s)
        """

        parameters = df.to_dict(orient='records')

        for record in parameters:
            postgres_operator = PostgresOperator(
                task_id="insert_car_categories",
                postgres_conn_id="postgres_conn",
                sql=insert_query,
                parameters=tuple(record.values()),
            )
    
            postgres_operator.execute(context=None)

    @task
    def join():
        postgres_operator = PostgresOperator(
            task_id="join_table",
            postgres_conn_id="postgres_conn",
            sql="""CREATE TABLE IF NOT EXISTS car_details AS
                    SELECT car_data.brand,
                           car_data.model,
                           car_data.price,
                           car_categories.category
                    FROM car_data JOIN car_categories
                    ON car_data.brand = car_categories.brand;
                """,
        )   

        postgres_operator.execute(context=None)
    
    join_task = join()
        
    read_car_data() >> create_table_car_data() >> \
        insert_car_data() >> join_task
    
    read_car_categories_data() >> create_table_car_categories_data() >> \
        insert_car_categories_data() >> join_task

data_transformation_storage_pipeline()