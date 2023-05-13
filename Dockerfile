# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for the application
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV SQLALCHEMY_DATABASE_URI=sqlite:///site.db
ENV SQLALCHEMY_TRACK_MODIFICATIONS=False

# Expose the port that the application runs on
EXPOSE 5000

# Run the command to start the application
# CMD ["flask", "run", "--host=0.0.0.0"]

CMD ["sh", "-c", "pytest && flask run --host=0.0.0.0"]
