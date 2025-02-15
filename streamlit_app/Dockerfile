FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

RUN apt-get update && apt-get install -y libgl1-mesa-glx

RUN apt-get update && apt-get install -y \
    v4l-utils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /dev/video

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
