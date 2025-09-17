from fastapi import FastAPI,HTTPException,Path, Query,Depends, Request
import logging


app = FastAPI()

@app.post("/upload/resume")
def uploadResume():
    pass

@app.post("/upload/bulk")
def uploadBulk():
    pass

