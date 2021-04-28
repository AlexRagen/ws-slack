FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

EXPOSE 8000

COPY . /app

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

WORKDIR /app/ws_slack
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8000"]
