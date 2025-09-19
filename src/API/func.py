from http.client import HTTPResponse, responses
from typing import Any
from urllib import response
from fastapi import FastAPI,HTTPException,Path, Query,Depends, Request, File, UploadFile
import logging
import sys
from stvis import pv_static
from pyvis.network import Network
sys.path.append('../../src')
from parse_new_resume import ParseResume
from user_data import UserData
from kg_gds import KGGDS


app = FastAPI()

@app.post("/resume/get")
async def getResumeData():
    response = UserData().getResumeData()
    return response

@app.post("/resume/upload")
async def uploadResume(req:Request):
    try:
        content : bytes = await req.body()
        print(content)
        pr = ParseResume(content)
        pr.createResumeGraph()
        return {"Resume Uploaded"}
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")



@app.get('/resume/analytics')
async def runAnalyticsOnResume(email:str):
    response = KGGDS().streamLeidenOnResume(email=email)
    return response


@app.post("/upload/bulk")
def uploadBulk():
    pass

