# Official Apache Airflow base image
FROM apache/airflow:2.10.4-python3.11

# Install system dependencies (if any additional are required)
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        vim \
    && build-essential \
    && libpq-dev \
    && tini \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Set environment variables
ENV AIRFLOW_VERSION=2.10.4
ENV PYTHON_VERSION=3.11
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# Default Airflow home directory (where logs and configurations are stored)
ENV AIRFLOW_HOME=/opt/airflow

# Set default working directory
WORKDIR ${AIRFLOW_HOME}

# Copy requirements.txt into the image
COPY requirements.txt /

# Install additional Python libraries and Airflow providers
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
    --constraint "${CONSTRAINT_URL}" \   

# Initialize the Airflow database and start the webserver
ENTRYPOINT ["tini", "--"]
CMD ["airflow", "webserver"]

# Expose port 8080 for the Airflow webserver
EXPOSE 8080