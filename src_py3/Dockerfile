FROM python:3.9-slim-buster
WORKDIR /src

RUN apt-get update && \
    apt-get install -y ffmpeg
    
COPY requirements.txt .
RUN pip install -r requirements.txt

# cache whisper
RUN python -c "import whisper; whisper.load_model('tiny')"

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]