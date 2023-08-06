# Structure

## Overview 

Structure can be used both as a server and as a standalone package. 

## Steps

1. Before starting, set the OPENAI_API_KEY variable. 
2. Create a schema 
3. Load your unstructured data and receive it in a structured format. 

## Server mode
### Start the server

    structure server --host 0.0.0.0 --port 8080 --log-level info

### API calls 

    curl -X POST -H "Content-Type: multipart/form-data" -F "file=@file.pdf" http://localhost:8000/cv-parser

### Load from DockerHub 

If you prefer the image, simply download it from DockerHub. 