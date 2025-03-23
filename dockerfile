# Gunakan base image Python dengan dukungan Jupyter Notebook
FROM python:3.10-slim

# Install alat bantu dan Jupyter Notebook
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install jupyter notebook

# Set working directory di dalam container
WORKDIR /app

# Copy semua file dari host ke container
COPY . /app

# Install dependencies Python
# Jika Anda memiliki file requirements.txt, gunakan baris berikut
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements file found"

# Expose port Jupyter Notebook
EXPOSE 8888

# Jalankan Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
