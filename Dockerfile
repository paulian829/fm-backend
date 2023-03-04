# Start with a base image
FROM python:3.9

# Set the working directory for the app
WORKDIR /app

# Copy the requirements file to the app directory
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install opencv-python

RUN pip install -r requirements.txt

# Copy the Django project files to the app directory
COPY . /app

# Expose the port that the app will run on
EXPOSE 8000

# Start the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# docker build -t django-opencv .