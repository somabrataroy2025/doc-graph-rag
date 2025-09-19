from typing import Any
from common.neo  import neo,neoDB,neoGDS
from pandas import DataFrame
from neo4j import RoutingControl,Result
from pyvis.network import Network
import helper as hp
import neo4j

class UserData:
    def __init__(self):
        pass

    def getResumeData(self)-> DataFrame|None:
        Q_User = """
                MATCH path = (r:Resume)-[:KNOWS]->(s:ResumeSkill)
                RETURN r.name as name,r.email as email,r.mobile as mobile,r.address as address,COLLECT(distinct s.name) as skils
                    """
        driver = neo()
        with driver:
            result = driver.execute_query(query_=Q_User,
                                result_transformer_= lambda r:r.to_df())
            return result

    def getUserSkillMatchedToOther(self,howManyRecords:int = 5):
        pass
    
    def getResumeSkillVisual(self) -> Network:
        driver = neo()
        with driver:
            result = driver.execute_query(
                """
                    MATCH (r:Resume)-[k:KNOWS]->(s:ResumeSkill)
                    RETURN r,k,s
                    """,
                database_="neo4j", result_transformer_=neo4j.Result.graph,
            )
            nodes_text = {  # what property to use as text for each node
                "Resume": "name",
                "ResumeSkill": "name",
            }

            result_visual = hp.visualize_result(result,nodes_text_properties=nodes_text)
            return result_visual
    
    
if __name__ == "__main__":
    data = UserData().visualPyvis()
    print(data)