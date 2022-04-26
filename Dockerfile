FROM python:3.9

WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD bot/corona.py .
ADD bot/goroskop.py .
ADD bot/main.py .
ADD bot/pogoda.py .
ADD bot/users_data.txt .
ADD bot/znaki_pictures ./znaki_pictures

CMD [ "python", "./main.py" ]
