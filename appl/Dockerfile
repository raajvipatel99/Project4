FROM python:3.8

EXPOSE 5000

WORKDIR /appl

COPY requirements.txt /appl
RUN pip install -r requirements.txt

COPY . /appl

CMD python3 -m  app