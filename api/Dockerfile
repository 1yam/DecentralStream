FROM python:3.9

WORKDIR /usr/app

COPY requirements.txt .

RUN pip install --requirement requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host=0.0.0.0" , "--reload" , "--port", "8000"]