
import json
from typing import Any
import fitz
import spacy
from  spacy.tokens import Span,Doc
from spacy.matcher import Matcher
from sqlalchemy.util.typing import Self
from common.llm import llm
from model.datamodel import ResumeDetails
from pydantic import BaseModel
import json
import create_kg_resume as cr

class ParseResume:
    nlp: Any
    inputContent : bytes
    matcher : Any
    def __init__(self,str:bytes):
        self.inputContent = str
        #self.nlp = spacy.load("en_core_web_md")
        self.nlp = spacy.load(r"D:\My Work\doc-graph-rag\doc-graph-rag\.docragenv\Lib\site-packages\en_core_web_md\en_core_web_md-3.8.0")
        self.matcher = Matcher(self.nlp.vocab)

    def getResumeTxt(self) -> str|None:
        resume_text = ""
        if self.inputContent is not None:   
            #pdf = fitz.open(stream=self.inputContent)
            pdf = fitz.open(stream=self.inputContent,filetype = "pdf")
            for page in pdf:
                resume_text = resume_text+str(page.get_text())
            return resume_text  
        else:
            return None


    # Create matcher
    def _createSkillMatcher(self)->Matcher:
        skillpatter = r"D:\My Work\doc-graph-rag\doc-graph-rag\config\skillset.txt"
        matcherlist = self.matcher
        with open(skillpatter, "r",encoding="utf-8") as f:
            for line in f:
                patterndata = json.loads(line.strip())
                if(isinstance(patterndata["pattern"],list)):
                    matcherlist.add(patterndata["label"],patterns=[patterndata["pattern"]])
        return matcherlist

    #get skills
    def _getSkillMatched(self,matcher:Matcher,doc:Doc)->list:
        skills=[]
        matches = matcher(doc)
        for match_id,start,end in matches:
            span = doc[start:end]    
            if not any(span.text in skill[0] for skill in skills):
                skills.append(span.text)
        return skills

    #use llm to parse and fetch info

    def _llm_extract(self,text:str)->ResumeDetails:
        
        resp = llm.invoke(f'''
                            You are an expert data extractor
                            Extract name, email, mobile and country text in json output only with extra text
                            from the below text
                            : {text}                            
                                ''')
        respJson =  json.loads(resp.content)
        res =  ResumeDetails(name= respJson["name"],
                            email = respJson["email"],
                            mobile = respJson["mobile"],
                            address= respJson["country"] )
        return res


    def _extract_Resume(self) ->ResumeDetails|None:        
        text_resume = self.getResumeTxt()
        if text_resume is not None:
            objMatcher = self._createSkillMatcher()
            nlp = spacy.blank('en')
            doc_resume = nlp(text=text_resume)
            skills_resume = self._getSkillMatched(objMatcher,doc_resume)
            print(text_resume)
            resumeDetails = self._llm_extract(text_resume)
            resumeDetails.skill = skills_resume
            return resumeDetails
        else:
            return None

    def createResumeGraph(self):
        data = self._extract_Resume()
        #print(f"{data.name},{data.email},{data.mobile},{data.skill},{data.address}")
        cr.createPersonSkill(data)



if __name__ == "__main__":
    res = ParseResume("")
    res.createResumeGraph()