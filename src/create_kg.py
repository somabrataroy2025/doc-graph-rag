from ast import List, Param
from typing import overload
import pandas as pd
from pandas import DataFrame
from common.neo import neoDB
from model.datamodel import ResumeDetails
import helper as hp

#neo4j Driver


def createPersonSkill(input: DataFrame):
    df_person = pd.DataFrame(input)
    
    driver = neoDB()
    with driver:
        for index,item in df_person.iterrows():
            print(f"processing user : {index}")
            properties={
                "rows":{
                    'email':item['email'],
                    'name' : item['name'],
                    'mobile': item['mobile'],
                    'skills' : item['skills_list'],
                    'address' : item['address'],
                    'skills_embed' : hp.embed_text(str(df_person['skills'])),
                    'address_embed' : hp.embed_text(str(df_person['address']))
                }
            }
            driver.query(
                """
                    UNWIND $rows as row
                    MERGE (p:Person {email:row.email})
                    set p.name = row.name,
                        p.mobile = row.mobile,
                        p.address = row.address,
                        p.skills_embed = row.skills_embed,
                        p.address_embed = row.address_embed
                    with p, row
                    foreach (item in row.skills |  
                            MERGE(s:Skill {name: rtrim(ltrim(item))}) 
                            MERGE (p)-[:KNOWS]->(s))
                """, properties
            )   
     
def createProjects(input: DataFrame):
    #add project node to db and map to person
    driver = neoDB()
    with driver:
        for index,item in input.iterrows():
            print(f"Create project mapping {index}")
            properties = {
                'rows':{
                    'email': item['email'],
                    'project':item['project']
                }
            }
            driver.query(
                """
                UNWIND $rows as row
                MERGE(p:Project{name:row.project})
                with row, p
                    MATCH(p1:Person{email: row.email})
                        MERGE(p1)-[:ASSIGNED_TO]->(p)

                """, properties
            )

def mapProjectSkills(input:DataFrame):
    df_projects = pd.DataFrame(input)
    df_projects['project_skills'] = df_projects['project_skills'].str.split(',')
    driver = neoDB()
    with driver:
        for index,item in df_projects.iterrows():
            print(f"Project Merged : {index}")
            properties={
                "rows":{
                    'project_name' : item['project'],
                    'project_skills' : item['project_skills']
                }
            }
            driver.query(
                """
                    UNWIND $rows as row
                    MATCH (p:Project {name:row.project_name})
                    with p, row.project_skills as skills
                        unwind skills as skill
                        MATCH(s:Skill {name:skill})
                        MERGE (p)-[:IMPLEMENTS]->(s)
                """, properties
            )   



