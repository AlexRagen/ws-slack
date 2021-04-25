FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

EXPOSE 8000

COPY ./ws-slack /app

RUN pip3 install -r ./requirements.txt

WORKDIR /app/ws-slack
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]
