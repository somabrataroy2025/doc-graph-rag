import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from graphdatascience import GraphDataScience
from neo4j import GraphDatabase

load_dotenv()

def neo():
    driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )
    return driver

def neoDB()->Neo4jGraph:
    return Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USERNAME'),
    password=os.getenv('NEO4J_PASSWORD'),
    database='neo4j'
    )

def neoGDS()-> GraphDataScience:
    driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )
    gds = GraphDataScience.from_neo4j_driver(driver=driver)
    gds.set_database('neo4j')
    return gds

if __name__ == "__main__":
    print(neoGDS().server_version())