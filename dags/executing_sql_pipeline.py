from airflow import DAG

from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import date, datetime, timedelta
from airflow.utils.dates import days_ago

default_args = {
    'owner' : 'airflow'
}

with DAG(
    dag_id = 'executing_sql_pipeline',
    description = 'Pipeline using SQL operators',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['pipeline', 'sql']
) as dag:
    create_table = PostgresOperator(
        task_id = 'create_table',
        sql = r"""
            CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER NOT NULL,
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        postgres_conn_id = 'postgres_conn',
        dag = dag
    )

    insert_values_1 = PostgresOperator(
        task_id = 'insert_values_1',
        sql = r"""
            INSERT INTO users (name, age, is_active) VALUES
                ('Julie', 30, false),
                ('Peter', 55, true),
                ('Emily', 37, false),
                ('Katrina', 54, false),
                ('Joseph', 27, true);
        """,
        postgres_conn_id = 'postgres_conn',
        dag=dag
    )

    insert_values_2 = PostgresOperator(
        task_id = 'insert_values_2',
        sql = r"""
            INSERT INTO users (name, age) VALUES
                ('Harry', 49),
                ('Nancy', 52),
                ('Elvis', 26),
                ('Mia', 20);
        """,
        postgres_conn_id = 'postgres_conn',
        dag=dag
    )

create_table