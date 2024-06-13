FROM python:3.11.1 as init
WORKDIR /usr/local/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

RUN useradd app
USER app

CMD ["python", "main.py"]