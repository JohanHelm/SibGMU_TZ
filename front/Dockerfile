FROM python:bookworm

COPY /templates/index.html /frontend/templates/index.html
ADD app.py /frontend/
COPY requirements.txt /frontend/requirements.txt
WORKDIR /frontend/
RUN pip install -r requirements.txt


CMD ["python", "app.py"]
