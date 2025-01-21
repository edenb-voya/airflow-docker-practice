# Official Apache Airflow base image
FROM apache/airflow:2.5.3

# Set environment variables to minimize warnings and ensure compatibility
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW_HOME=/opt/airflow

# Install additional Python libraries and Airflow providers
RUN pip install --no-cache-dir \
    pandas \
    numpy \
    scikit-learn \
    matplotlib \
    plotly \
    apache-airflow-providers-google \
    apache-airflow-providers-amazon

# Copy local DAGs to the Airflow directory inside the container
COPY ./dags /opt/airflow/dags

# Copy local DAGs to the Airflow directory inside the container
COPY ./plugins /opt/airflow/plugins

# Expose port 8080 for the Airflow webserver
EXPOSE 8080

# Specify the default command to start the Airflow webserver
CMD ["webserver"]