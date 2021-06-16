FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

EXPOSE 8432
VOLUME /secrets
COPY . /app

RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

WORKDIR /app/ws_slack
CMD ["uvicorn", "app:api", "--host", "0.0.0.0", "--port", "8432", "--ssl-keyfile" , "/secrets/key.pem", "--ssl-certfile", "/secrets/server_crt.pem", "--ssl_keyfile_password", ""]
