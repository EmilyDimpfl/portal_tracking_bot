FROM python:bullseye

WORKDIR /opt/portalbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY portalbot.py .

CMD ["python3", "portalbot.py"]