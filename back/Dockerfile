FROM python:bookworm

ADD back_socket.py /backend/
ADD db_handler.py /backend/
ADD main.py /backend/
COPY requirements.txt /backend/requirements.txt
WORKDIR /backend/
RUN pip install -r requirements.txt

EXPOSE 57360

VOLUME /backend/logs

CMD ["python", "main.py"]
