FROM bitnami/spark:3

WORKDIR /app

COPY app.py .

CMD [ "spark-submit", "--master", "spark://spark-master:7077", "/app/app.py" ]
