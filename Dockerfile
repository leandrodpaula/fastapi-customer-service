# Dockerfile

# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the listening port for Uvicorn. Cloud Run will map its external port to this.
# As per our terraform (main.tf), the container_port is 80.
ENV PORT 80
ENV APP_MODULE "src.interfaces.api.main:app" # Module and app instance for Uvicorn

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies if any (not immediately needed for this app)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package

# 5. Install Python dependencies
# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip &&     pip install --no-cache-dir -r requirements.txt

# 6. Copy the application source code into the container
COPY ./src ./src

# 7. Expose the port the app runs on
# This is more for documentation; Cloud Run uses the PORT env var or a default.
EXPOSE ${PORT}

# 8. Define the command to run the application
# Uvicorn will run on 0.0.0.0 to be accessible from outside the container (within Cloud Run's environment)
# The port is taken from the PORT environment variable.
CMD ["uvicorn", "src.interfaces.api.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
