FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV LISTEN_PORT=8000
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/