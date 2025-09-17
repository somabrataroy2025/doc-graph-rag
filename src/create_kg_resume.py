import common.llm as llm
from common.neo import neoDB
from model.datamodel import ResumeDetails
import helper as hp

# merge node : User, Skill, 
# merge relationships : [:KNOWS]
# analytic properties : skill embed, address embed, degree centrality, community (Louvein/Leinden)
# cosince similarity

def createPersonSkill(input:ResumeDetails):
    driver = neoDB()
    with driver:       
        properties={
            "rows":{
                'name' : input.name,
                'email':input.email,
                'mobile' : input.name,
                'skills' : input.skill,
                'skills_embed' : hp.embed_text(','.join(input.skill)),
                'address_embed' : hp.embed_text(input.address)
            }
        }
        driver.query(
            """
                UNWIND $rows as row
                MERGE (p:Resume {email:row.email})
                set p.name = row.name,
                p.email = row.email,
                p.mobile = row.mobile,
                p.address_embed = row.address_embed,
                p.skills_embed = row.skills_embed

                with p, row
                foreach (item in row.skills |  
                        MERGE(s:ResumeSkill {name: rtrim(ltrim(item))}) 
                        MERGE (p)-[:KNOWS]->(s))
            """, properties
        )   