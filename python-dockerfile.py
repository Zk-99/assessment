# Use an official Python runtime
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy current directory contents into the container at /app
COPY . /app

# Install packages specified in packages.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install MySQL client for Python
RUN apt-get update && apt-get install -y default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

# Expose the port the app runs on
EXPOSE 5000

# Run the script
CMD ["python", "python-code.py"]