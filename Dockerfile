FROM python:3.11.1 as init
WORKDIR .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd app
USER app

COPY main.py .

STOPSIGNAL SIGINT
ENTRYPOINT ["python", "main.py"]