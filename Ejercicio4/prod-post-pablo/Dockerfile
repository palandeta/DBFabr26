FROM python:alpine3.22
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY apppostpablo.py .
EXPOSE 5001
CMD ["python", "apppostpablo.py"]