# Basic flask container

FROM fanoftal2/flask-crud-base:1

ADD base-image/requirements.txt ./app /home/app/
WORKDIR /home/app/

COPY base-image/requirements.txt /home/app/requirements.txt

RUN pip install -r requirements.txt
COPY . /home/app/

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
