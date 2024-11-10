# Base image
FROM python:3.13.0-alpine3.20

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the project dependencies
RUN pip install -r requirements.txt

RUN apk update && apk add --no-cache curl

# Copy the application code into the container
COPY app.py .

RUN addgroup -S nonroot \
    && adduser -S nonroot -G nonroot

USER nonroot

# Add the HEALTHCHECK instruction
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://127.0.0.1:5000 || exit 1

# Expose the port the Flask application will be listening on
EXPOSE 5000

# Set environment variables, if necessary
# ENV MY_ENV_VAR=value

# Run the Flask application
CMD ["python", "app.py"]