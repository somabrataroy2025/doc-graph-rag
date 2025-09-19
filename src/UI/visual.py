from tkinter import N
from urllib import request
import streamlit as st
import streamlit.components.v1 as component
from streamlit.components.v1 import html
import requests as rq
import sys
sys.path.append('../../src')
import streamlit as st
import pandas as pd
import json
from user_data import UserData
from stvis import pv_static

st.set_page_config(layout="wide")

resumeuploadURL = 'http://127.0.0.1:8000/resume/upload'

uploaded_file = st.file_uploader("Choose a file",type=["pdf"])

coly,colz = st.columns(2)
with coly:    
        if st.button("Upload Resume", type="primary"):
            if uploaded_file is not None:
            # To read file as bytes:
                #bytes_data = uploaded_file.getvalue()
                response = rq.post(url = resumeuploadURL, data =  uploaded_file)
                if response.status_code == 200:
                    st.write(response.text)
                else:
                    st.write(response.text)
            else:
                st.write('Please browse a resume first .. (pdf)')
with colz:
    button_1_clicked = st.button("Analyze Resume", key="button_1",type="primary")
    
col1,col2= st.columns(2)


if button_1_clicked:
    try:
        fastapi_url = 'http://127.0.0.1:8000/resume/analytics?email=srijita.de@gmail.com'
        respose = rq.get(fastapi_url)
        if respose.status_code == 200:
            jsonResponse = json.loads(respose.text)
            with col1:
                colA,colB,colC = st.columns(3)
                with colA:
                    st.subheader('Peer details')
                    #st.write(respose.text)
                    for key in jsonResponse["Peer"]:
                        st.write(jsonResponse["Peer"][key])
                with colB:
                    st.subheader("Projects")
                    for key in jsonResponse["Project"]:
                        st.write(jsonResponse["Project"][key])
                with colC:
                    st.subheader("Project Skills")
                    for key in jsonResponse["Project_Skills"]:
                        st.write(','.join(jsonResponse["Project_Skills"][key]))
        else:
            st.error(f'Unable to fetch user data {respose.status_code}')
    except rq.exceptions.ConnectionError:
        st.error('Error')

    graphData =  UserData().getResumeSkillVisual()
    with col2:
        pv_static(graphData)
        



