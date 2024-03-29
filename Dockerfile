FROM python:3.8

WORKDIR /usr/src/app

RUN python -m pip install  --no-cache-dir --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# ENTRYPOINT [ "flask" ]
CMD ["bash", "./start_prod_server.sh"]
# CMD ["run", "--host=0.0.0.0", "--port=5000"]
