import pandas as pd
from pandas import DataFrame
from typing import Any
import helper as hp
import create_kg as ck

class ParseDf:
    csvPath = ""
    df : DataFrame
    def __init__(self, path):
        self.csvPath = path
        self.df = pd.read_csv(path)

    def _convert_df(self,col:str, splitBy = None)->DataFrame|None: 
        df1 = pd.DataFrame(self.df)
        df1 = df1[[col]]
        col_trans = 'transformed'
        if col in df1.columns:
            if splitBy is not None:
                df1[col_trans] =  df1[col].str.split(splitBy)
                df1[col_trans] = df1[col_trans].explode(col_trans).drop_duplicates().reset_index(drop=True)  
            else:
                df1[col_trans] = df1[col].drop_duplicates().reset_index(drop=True)
                df1 = df1.dropna()
        else:
            return None
        return df1


    def _embed_df(self,colEmbd:str)->DataFrame|None:
        if self.df:
            df = pd.DataFrame(input)
            df["embedding"] = df[colEmbd].apply(lambda item: hp.embed_text(item[0]))
            return df 
        else:
            return None



    def _split_dataframe(self, chunk_size = 5):
        df = self.df
        chunks = list()
        num_chunks = len(df) # chunk_size + 1
        for i in range(num_chunks):
            chunks.append(df[i*chunk_size:(i+1)*chunk_size])
        return chunks


    def _transform_skill(self) -> DataFrame:
        df_person = pd.DataFrame(self.df)
        df_person['skills_list'] = df_person['skills'].str.split(',')
        return df_person


def bulkSkillUpload(filePath:str):
    dfemp = ParseDf(filePath)
    dfemptrans = dfemp._transform_skill()
    ck.createPersonSkill(dfemptrans)
    ck.createProjects(dfemp.df)
    ck.mapProjectSkills(dfemp.df)

