
FROM python:3.10-slim 


WORKDIR /app

COPY requirements.txt .


RUN pip install -r requirements.txt 


COPY pobierz_pogode_auto.py .


CMD ["python","-u","pobierz_pogode_auto.py"]
