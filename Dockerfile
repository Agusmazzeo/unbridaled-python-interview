# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory to the workdir in the Docker image
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run the application when the container launches
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
