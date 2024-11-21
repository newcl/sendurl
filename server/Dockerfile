# Use an official Python 3 image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Update the system and install necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install the latest version of yt-dlp and Flask via pip
RUN pip install --no-cache-dir yt-dlp flask

# Copy the application files to the container (if you have a Flask app)
# Uncomment the following line if you want to add your Flask app
COPY . /app

# Set the environment variable for Flask
ENV FLASK_APP=server.py

# Set default command to use Flask (you can replace 'app.py' with your main Flask file)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
