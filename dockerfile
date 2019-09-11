# Alpine doesn't work with opencv-python
FROM python:3.7-slim 
COPY . /app
WORKDIR /app
RUN \
    pip install --upgrade pip && \
    pip install -r requirements.txt
EXPOSE 5000
CMD python ./index.py