from common.neo import neoDB, neoGDS,neo
import pandas as pd
import helper as hp


# need to implement tranasction
# all the gds will be recalculated over the whole population every is actioned
def calculateSimilarity():
    Q_Delete_Rel = "MATCH ()-[s:SIMILAR_SKILL]-() DELETE s"
    Q_Create_Rel="""
            MATCH (p1:Person)-[:KNOWS]->(s1:Skill)<-[:KNOWS]-(p2:Person)
                WHERE p1.email < p2.email
                with p1.email as email1,p2.email as email2, count(DISTINCT(s1)) as skl_count WHERE skl_count > 0
                WITH COLLECT({person_1:email1, person_2:email2,skill_cnt:skl_count}) as data 
            call(data)
            {
            UNWIND data as val    
            MATCH(per:Person{email : val.person_1})
            MATCH(per1:Person{email : val.person_2})
            MERGE(per)-[s:SIMILAR_SKILL]->(per1)
            set s.overlap = val.skill_cnt
            }
    """
    driver = neoDB()
    with driver:
        driver.query(Q_Delete_Rel)
        driver.query(Q_Create_Rel)

def _createGraphProjection() -> None:
    graph_name = "person_similarity_projection"
    node_projection = ["Person"]
    rel_projection = {"SIMILAR_SKILL": {"orientation": 'UNDIRECTED', "properties": "overlap"}, }
    #drop existing projection:
    gds =  neoGDS()
    with gds:
        gds.graph.drop(graph_name,False) 
        return gds.graph.project(graph_name,node_projection,rel_projection)

def createLaidenCommunity():
    G, res = _createGraphProjection()
    gds =  neoGDS()
    with gds:
        gds.leiden.write(
        G,
        writeProperty='leiden_community',
        relationshipWeightProperty='overlap',
        maxLevels=100,
        gamma=1.5,
        theta=0.001,
        concurrency = 1,
        randomSeed = 42
)
        
# RUN GDS ALGO ON NEWLY IMPORTED RESUME w.r.t THE EXISTING BULK IMPORTED DATA

def _calculateSimilarityResume():
    Q_Delete_Rel = "MATCH ()-[s:MATCHED_SKILL]-() DELETE s"
    Q_Create_Rel="""
            MMATCH(r:Resume)-[k:KNOWS]->(rs:ResumeSkill)
            MATCH(s:Skill {name : rs.name})<-[k1:KNOWS]-(p:Person)
            with r.email as email1,p.email as email2, collect(rs.name) as ResumeSkills,count(DISTINCT(k)) as skl_count
            WITH COLLECT({person_1:email1, person_2:email2,skill_cnt:skl_count}) as data 
            call(data)
            {
            UNWIND data as val    
            MATCH(per:Resume{email : val.person_1})
            MATCH(per1:Person{email : val.person_2})
            MERGE(per)-[s:MATCHED_SKILL]->(per1)
            set s.overlap = val.skill_cnt
            }
    """
    driver = neoDB()
    with driver:
        driver.query(Q_Delete_Rel)
        driver.query(Q_Create_Rel)
    


def _createNewResumeProjection():
    graph_name = "resume_similarity_projection"
    node_projection = ['Person','Resume']
    rel_projection = {  'MATCHED_SKILL' : {'properties':'overlap', 'orientation': 'UNDIRECTED'} ,
                        'SIMILAR_SKILL' : {'properties':'overlap', 'orientation': 'UNDIRECTED'}}
    #drop existing projection:
    gds =  neoGDS()
    with gds:
        gds.graph.drop(graph_name,False) 
        return gds.graph.project(graph_name,node_projection,rel_projection)

def streamLeidenOnResume(email:str):
    Q_Leiden = """
                CALL gds.leiden.stream('resume_similarity_projection',
                {
                relationshipWeightProperty:'overlap',
                maxLevels:100, gamma:1.5,theta:0.001,concurrency : 1,randomSeed : 42
                })
                YIELD nodeId, communityId
                with communityId,collect(gds.util.asNode(nodeId).email) as groups
                RETURN *
                """
    driver = neo()
    with driver:
        df = driver.execute_query(
            Q_Leiden,
            result_transformer_=lambda res: res.to_df()
        )
        for group in df["groups"]:
            if email in group:
                # find the best match peer, their project & project skills
                similar_skills_df = driver.execute_query(
                    """
                    WITH  $group as persons
                    MATCH(p:Person where p.email in persons)-[:ASSIGNED_TO]->(pr:Project)-[:IMPLEMENTS]->(s:Skill)
                    RETURN p.name as Peer,pr.name as Project,collect(s.name) as Project_Skills
                    """,
                    result_transformer_= lambda r: r.to_df(),
                    group = group
                )
                return similar_skills_df
        



if __name__ == "__main__":
    data = streamLeidenOnResume('srijita.de@gmail.com')
    print(data)
