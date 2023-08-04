FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that the Flask app will be running on (adjust the port if needed)
EXPOSE 5000

# Set the entry point for the container (replace 'your_flask_app.py' with the name of your Flask app)
CMD ["python", "app.py"]