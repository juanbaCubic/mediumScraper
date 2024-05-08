# Medium Scraper

This repository contains a Python script for scraping user information and articles from Medium via the RapidAPI and storing it in a Neo4j database.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:

- Python 3
- Docker (for running Neo4j)

### Installing

A step-by-step series of examples that tell you how to get a development env running:

#### Setting Up Neo4j with Docker

1. Pull the official Neo4j image from Docker Hub:
   ```bash
   docker pull neo4j:latest
   ```
   
2. Run the Neo4j container:
   ```bash
   docker run --name neo4j -p7474:7474 -p7687:7687 -d \
	-v $HOME/neo4j/data:/data \
	-v $HOME/neo4j/logs:/logs \
	-v $HOME/neo4j/import:/var/lib/neo4j/import \
	-v $HOME/neo4j/plugins:/plugins \
	--env NEO4J_AUTH=username/password neo4j:latest
	```
This command starts a Neo4j container with the password test for the neo4j username. Adjust the volumes and password as needed.
