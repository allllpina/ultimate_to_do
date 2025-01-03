FROM python:3.9-slim

WORKDIR /model-part

COPY . /model-part

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask","--app", "model", "run" , "--host=0.0.0.0"]
