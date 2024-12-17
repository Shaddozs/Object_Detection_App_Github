# Gunakan base image Python resmi
FROM python:3.11-slim

# Install dependensi sistem yang dibutuhkan
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file terlebih dahulu
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh project
COPY . .

# Buat direktori untuk uploads dan outputs
RUN mkdir -p /app/uploads /app/outputs && \
    chmod -R 777 /app/uploads /app/outputs

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port yang digunakan Flask
EXPOSE 5000

# Command untuk menjalankan aplikasi
CMD ["flask", "run"]