FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY starting_and_stopping_instances.py .

ENTRYPOINT ["python", "./starting_and_stopping_instances.py"]

CMD [ "" ]
