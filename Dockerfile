# Official Apache Airflow base image
FROM apache/airflow:2.7.1-python3.10

# Install system dependencies (if any additional are required)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV AIRFLOW_VERSION=2.7.1
ENV PYTHON_VERSION=3.10
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# Airflow will use the CeleryExecutor for distributed task execution
ENV AIRFLOW__CORE__EXECUTOR=CeleryExecutor
# Default Airflow home directory (where logs and configurations are stored)
ENV AIRFLOW_HOME=/opt/airflow
# Set the broker URL to use Redis (we'll configure this in docker-compose)
ENV AIRFLOW__CELERY__BROKER_URL=redis://redis:6379/0
# Set the result backend to PostgreSQL (we'll configure this in docker-compose)
ENV AIRFLOW__CELERY__RESULT_BACKEND=postgresql+psycopg2://airflow:airflow@postgres:5432/airflow

# Set default working directory
WORKDIR $AIRFLOW_HOME

# Install additional Python libraries and Airflow providers
RUN pip install --no-cache-dir \
    --constraint "${CONSTRAINT_URL}"
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    plotly \
    apache-airflow-providers-google \
    apache-airflow-providers-amazon \

# Initialize the Airflow database and start the webserver
CMD ["airflow", "webserver"]

# Expose port 8080 for the Airflow webserver
EXPOSE 8080
