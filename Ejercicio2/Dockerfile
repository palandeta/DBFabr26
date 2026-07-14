FROM python:alpine3.22
RUN mkdir -p /app
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python", "/app/main.py"]