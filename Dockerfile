FROM python:bullseye

WORKDIR /opt/portalbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY userdata.py .
COPY portalbot.py .

# CMD ["python3", "portalbot.py"]
ENTRYPOINT ["python3", "portalbot.py"]
