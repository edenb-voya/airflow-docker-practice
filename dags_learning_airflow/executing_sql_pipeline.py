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
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER NOT NULL,
                    city VARCHAR(50),
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

    delete_values = PostgresOperator(
        task_id = 'delete_values',
        sql = r"""
            DELETE FROM users WHERE is_active = FALSE;
        """,
        postgres_conn_id = 'postgres_conn',
        dag = dag
    )

    update_values = PostgresOperator(
        task_id = 'update_values',
        sql = r"""
            UPDATE users SET city = 'Seattle';
        """,
        postgres_conn_id = 'postgres_conn',
        dag = dag
    )

    display_result = PostgresOperator(
        task_id = 'display_result',
        sql = r"""SELECT * FROM users;""",
        postgres_conn_id = 'postgres_conn',
        dag = dag,
        do_xcom_push = True
    )

create_table >> [insert_values_1, insert_values_2] >> delete_values >> update_values >> display_result