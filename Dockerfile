FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y \
	usbutils

WORKDIR /root/backend

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /root/backend/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]