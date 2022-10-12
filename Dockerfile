FROM python:3.8

RUN mkdir /nums_api

WORKDIR /nums_api

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

RUN pip3 install psycopg2==2.9.3

COPY . .

EXPOSE 5001

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5001"]