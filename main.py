
import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
import time
import numpy as np

st.set_page_config(
    page_title= 'Analysis of Survey Data',
    page_icon = '📊',
    layout= 'wide'
)

st.title('Exploration of Data')   

PersonalInfo = pd.read_csv('./MainData.csv')
CommonData = pd.read_csv('./CommonData.csv')

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def plot_stack(data, featureA, featureB):
    try:
        if len(data[featureA].unique()) > 2:
            data = data[data[featureA] != 'NO']
        if len(data[featureB].unique()) > 2:
            data = data[data[featureB] != 'NO']
            
        lenData = len(data)
        title = f'Relating {featureA} and {featureB}, N = {lenData}'
        fig = px.bar(pd.crosstab(data[featureA], data[featureB]), color=featureB, title = title, width = 1000, orientation = 'h')
    
    except:
        fig = Image.open('./error.png')
    
    return placeholder.write(fig)

def splitList(data):

    temp = data.str.strip().str.lower()

    ls = []

    for i in temp:
        try:
            [ls.append(k.strip(' ')) for k in i.split(',')]
        except:
            pass

    return pd.Series(ls).sort_values()  


def plot_bar(data, feature):
    try:
        if len(data[feature].unique()) > 2:
            data = data[data[feature] != 'NO']

        lenData = len(data)
        title = f'Distribution of {feature}, N = {lenData}'

        if feature in ['locallyAvailableFoodsConsumed', 'brandsOfTwoWheelers', 'anganwadiServicesUtilised', 'brandsof', 'specialSkills', 'brandsOfThreeWheelers', 'brandsOfFourWheelers', 'cropsCultivated', 'treesOwnedIfAny', 'cropsInKitchenGarden']:
            splitVal = splitList(data[feature])
            fig = px.histogram(splitVal, title = title, width = 1000)
    
            return placeholder.plotly_chart(fig) 
              
        else:         
            fig = px.histogram(data[feature].sort_values(), title = title, width = 1000)

            return placeholder.plotly_chart(fig)
    
    except:
        fig = Image.open('./error.png')

        return placeholder.image(fig)
    
    

def plot_pie(data, feature):
    try:
        if len(data[feature].unique()) > 2:
            data = data[data[feature] != 'NO']

        lenData = len(data)
        title = f'Distribution of {feature}, N = {lenData}'

        if feature in ['locallyAvailableFoodsConsumed', 'brandsOfTwoWheelers', 'anganwadiServicesUtilised', 'brandsof', 'specialSkills', 'brandsOfThreeWheelers', 'brandsOfFourWheelers', 'cropsCultivated', 'treesOwnedIfAny', 'cropsInKitchenGarden']:
            splitVal = splitList(data[feature])
            fig = px.pie(names = splitVal, title = title, width = 1000)
            
        else:
            
            fig = px.pie(names = data[feature].sort_values(), title = title, width = 1000)
            
        
    except:
        fig = Image.open('./error.png')
    
    return placeholder.write(fig)

head = st.container()
body = st.container()
placeholder = st.container()
    
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

    village = st.selectbox('Select Village', ('All', 'ntp', 'thc', 'kmp', 'cgpr'))

    applied = st.form_submit_button("Apply")

dfname = st.sidebar.selectbox('Select Dataset', ('Personal Info', 'Common Data'))

with st.sidebar.form("choice"):

    

    plotType = st.selectbox('Choose type of plot', ('Stacked bar', 'Bar graph', 'Pie chart'))

    if dfname == 'Personal Info':
        features = st.multiselect('Choose features to plot', PersonalInfo.columns, ['Age Group', 'gender'])
    
    elif dfname == 'Common Data':
        features = st.multiselect('Choose features to plot', CommonData.columns)

    submitted = st.form_submit_button("Submit")
            

            
personal = PersonalInfo

with body:
    if applied:
        
        if len(occupation) != 0:
            personal = personal.loc[personal.occupation.isin(occupation)] 
        if len(education) != 0:
            personal = personal.loc[personal.educationQualification.isin(education)]
        if gender in ['Male', 'Female']:
            personal = personal[personal.gender == gender]
        if maritalStatus in ['Married', 'Unmarried']:
            personal = personal[personal.maritalStatus == maritalStatus.upper()]
        if dailyWage:
            personal = personal[personal.isADailyWageWorker == 'YES']
        
        with st.spinner('Fetching Data...'):
            time.sleep(2)

        outFile = convert_df(personal)
        st.download_button(
            label = 'Download Data as CSV',
            data = outFile,
            file_name = 'DataQueries.csv',
            mime = 'text/csv'
        )
        with st.expander('View Dataframe'):
            st.write(personal)


common = CommonData.loc[CommonData._id.isin(personal._id.unique())]

      

if submitted:     

    if dfname == 'Personal Info':
        data = personal
    elif dfname == 'Common Data':
        data = common

    if plotType == 'Stacked bar':
        
        plot_stack(data, features[0], features[1])

    elif plotType == 'Bar graph':
    
        plot_bar(data, features[0])

    elif plotType == 'Pie chart':
    
        plot_pie(data, features[0])

        

        


