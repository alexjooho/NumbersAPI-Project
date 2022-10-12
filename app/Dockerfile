FROM python:3.8

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

RUN mkdir /nums_api

WORKDIR /nums_api

COPY . .

EXPOSE 8000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8000"]