# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests py2neo

# Define environment variable for Neo4j and RapidAPI Key
ENV NEO4J_URI=bolt://IP:PORT
ENV NEO4J_USER=username
ENV NEO4J_PASSWORD=password
ENV RAPIDAPI_KEY=RAPIDAPI_KEY

# Run scrapeMediumUser.py when the container launches
ENTRYPOINT ["python", "./scrapeMediumUser.py"]