Part 1 : Build Application Implementing Knowledge Graph using Neo4j, LLM, FastAPI etc.

I just completed an end to end application the contains following features
This application will compare e fresher/lateral hire resume with the existing population based on their skill, project and the skills used in those projects. Based on the analysis (Graph data science) it will find the appropriate community where the user might belong, who might be his peer group and which project he might be assigned to.
Upload Bulk data via csv that contains enterprise skill dats for their employee (via pandas)
Extract relevant information from new Resume. (using Spacy & AzueAI)
Data and embeddings stored to neo4j graph database
Run multiple community algo based on relevance and use of skills distribution. (neo4j graph data science)
Exposing data and other http action via FastAPI
UI via streamlit and interaction graph report via pyvis

The project is fully functional. Code is present in github repo
