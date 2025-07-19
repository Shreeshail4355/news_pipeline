# Dockerized News Pipeline (Skift & PhocusWire → PostgreSQL)

## Overview
A Docker Compose-based Python application that scrapes the latest news articles from Skift and PhocusWire, stores them in PostgreSQL, and displays the top 5 latest articles upon execution.

## Setup

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repo (or copy the directory):
   ```bash
   git clone <this_repo_url> news_pipeline
   cd news_pipeline


To build and run the application using Docker:

1. **Build and start the containers**:
   ```bash
   docker-compose up --build -d
   ```

2. **Access the running container**  
   Replace `<container_name>` with your actual container name:
   ```bash
   docker exec -it <container_name> bash
   ```

3. **Connect to PostgreSQL inside the container**:
   ```bash
   psql -U newsuser -d newsdb
   ```

4. **Query the `articles` table**:
   ```sql
   SELECT * FROM articles;
