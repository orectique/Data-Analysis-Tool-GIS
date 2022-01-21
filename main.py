from numpy import place
import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
import time

st.set_page_config(
    page_title= 'Analysis of Survey Data',
    page_icon = '📊',
    layout= 'wide'
)

st.title('Exploration of Data')   

PersonalInfo = pd.read_csv('./MainData.csv')

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def plot(data, type, featureA, featureB):
    try:
        if type == 'Stacked bar':
            title = f'Relating {featureA} and {featureB}'
            fig = px.bar(pd.crosstab(data[featureA], data[featureB]), color=featureB, title = title, width = 1000, orientation = 'h')

        elif type == 'Bar graph':
            title = f'Distribution of {featureA}'
            fig = px.histogram(data[featureA], title = title, width = 1000)
    
    except:
        fig = Image.open('./error.png')
    
    return fig

head = st.container()
body = st.container()
placeholder = st.container()

with head:
    
    st.sidebar.header('Filters')
    with st.sidebar.form('filterForm'):
        gender = st.selectbox('Select Gender', ('Both', 'Male', 'Female'))

        maritalStatus = st.selectbox('Marital Status', ('Both', 'Married', 'Unmarried'))

        education = st.multiselect('Highest Educational Qualification', ['Secondary', 'Primary', 'Diploma', 'Under graduate', 'Higher secondary',
'Middle school', 'Uneducated', 'Post graduate'])

        occupation = st.multiselect('Occupation', ['Elementary occupations', 'Plant and machine operators and assemblers',
'Unemployed', 'Managers', 'Clerical support workers',
'Craft and related trades workers', 'Service and sales workers', 
'Skilled agricultural, forestry and fishery workers',
'Technician and associate professionals', 'Professional',
'Armed Forces occupations'])

        dailyWage = st.checkbox('Daily Wage')    

        applied = st.form_submit_button("Apply")
            

            

with body:
    if applied:
        temp = PersonalInfo
        if len(occupation) != 0:
            temp = temp.loc[temp.occupation.isin(occupation)] 
        if len(education) != 0:
            temp = temp.loc[temp.educationQualification.isin(education)]
        if gender in ['Male', 'Female']:
            temp = temp[temp.gender == gender]
        if maritalStatus in ['Married', 'Unmarried']:
            temp = temp[temp.maritalStatus == maritalStatus.upper()]
        if dailyWage:
            temp = temp[temp.isADailyWageWorker == 'YES']
        
        with st.spinner('Fetching Data...'):
            time.sleep(2)

        outFile = convert_df(temp)
        st.download_button(
            label = 'Download Data as CSV',
            data = outFile,
            file_name = 'DataQueries.csv',
            mime = 'text/csv'
        )
        with st.expander('View Dataframe'):
            st.write(temp)

        with st.form("choice"):

            plotType = st.selectbox('Choose type of plot', ('Stacked bar', 'Bar graph'))

            features = st.multiselect('Choose features to plot', PersonalInfo.columns, ['Age', 'gender'])

            submitted = st.form_submit_button("Submit")

            if submitted:     

                if plotType == 'Stacked bar':
                    
                    st.write(plot(temp, plotType, features[0], features[1]))

                elif plotType == 'Bar graph':
                
                    st.write(plot(temp, plotType, features[0]))

        


