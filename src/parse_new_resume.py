from ast import List
import json
from pydoc import doc
from typing import Self
from urllib import response
import fitz
import spacy
from spacy.tokens import Span,Doc
from spacy.matcher import Matcher
from test.test_doctest.test_doctest2 import run_docstring_examples
from common.llm import llm
from model.datamodel import ResumeDetails
from pydantic import BaseModel
import json
import create_kg_resume as cr


# replace by en_core_web_md
model_path=r"D:\My Work\doc-graph-rag\doc-graph-rag\.docragenv\Lib\site-packages\en_core_web_md\en_core_web_md-3.8.0"
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

def getResumeTxt(path:str) -> str:
    resume_text = ""
    pdf = fitz.open(path)
    for page in pdf:
        resume_text = resume_text+str(page.get_text())
    return resume_text  



# Create matcher
def _createSkillMatcher()->Matcher:
    skillpatter = r"D:\My Work\doc-graph-rag\doc-graph-rag\config\skillset.txt"
    with open(skillpatter, "r",encoding="utf-8") as f:
        for line in f:
            patterndata = json.loads(line.strip())
            if(isinstance(patterndata["pattern"],list)):
                matcher.add(patterndata["label"],patterns=[patterndata["pattern"]])
    return matcher

#get skills
def _getSkillMatched(matcher:Matcher,doc:Doc)->list:
    skills=[]
    matches = matcher(doc)
    for match_id,start,end in matches:
        span = doc[start:end]    
        if not any(span.text in skill[0] for skill in skills):
            skills.append(span.text)
    return skills

#use llm to parse and fetch info

def _llm_extract(text:str)->ResumeDetails:
    
    resp = llm.invoke(f'''
                           You are an expert data extractor
                           Extract name, email, mobile and address in json format only with extra text
                           from the below text
                          : {text}                            
                            ''')
    respJson =  json.loads(resp.content)
    res =  ResumeDetails(name= respJson["name"],
                         email = respJson["email"],
                         mobile = respJson["mobile"],
                         address= respJson["address"] )
    return res


def extract_Resume(path:str) ->ResumeDetails:
    text_resume = getResumeTxt(path)
    objMatcher = _createSkillMatcher()
    nlp = spacy.blank('en')
    doc_resume = nlp(text=text_resume)
    skills_resume = _getSkillMatched(objMatcher,doc_resume)
    resumeDetails = _llm_extract(text_resume)
    resumeDetails.skill = skills_resume
    return resumeDetails


if __name__ == "__main__":
    #pdftxt = getResumeTxt(r'D:\My Work\doc-graph-rag\doc-graph-rag\data\resume1.pdf')    
    data = extract_Resume(r'D:\My Work\doc-graph-rag\doc-graph-rag\data\resume1.pdf')    
    if data is not None:
        cr.createPersonSkill(data)