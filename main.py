import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from math import ceil
import time

st.set_page_config(
    page_title= 'Analysis of Survey Data',
    page_icon = '📊',
    layout= 'wide'
)

st.title('Exploration of Data')   

PersonalInfo = pd.read_csv('./PersonalInfo.csv')
LocationData = pd.read_csv('./Location.csv')
CommonData = pd.read_csv('./CommonData.csv')

@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

def dirtyData(df):
    quality = pd.DataFrame(columns= PersonalInfo.columns)
    trueNA = []
    columns = []

    for column in quality.columns:
        quality[column] = df[column].isna()
        k = (np.count_nonzero(np.array(quality[column])))*100/len(quality[column])
        if k != 0:
            trueNA.append(k)
            columns.append(column)
    notNA = [100 - i for i in trueNA]
    fig = go.Figure()

    fig.add_trace(go.Bar(
            y = columns,
            x = trueNA,
            name = 'NA Values',
            orientation = 'h',
            marker = dict(
                color = 'rgBa(114, 222, 111, 0.6)',
                line = dict(   
                    color = 'rgBa(114, 222, 111, 1)',
                    width = 3
                )
            )
            
        )
    )

    fig.add_trace(go.Bar(
            y = columns,
            x = notNA,
            name = 'Non NA Values',
            orientation = 'h',
            marker = dict(
                color = 'rgBa(238, 115, 115, 0.6)',
                line = dict(   
                    color = 'rgBa(238, 115, 115, 1)',
                    width = 3
                )
            )
            
        )
    )

    fig.update_layout(barmode = 'stack', title = 'Percentage of NA Data', width = 1000, height = 600)

    return fig

def mapOut(data):
    fig = px.scatter_mapbox(data, lon = 'Long', lat = 'Lat', color = 'Employed', size = 'Family Size', title = 'Locations of Families', width= 1000, zoom = 7, hover_name= "_id")

    fig.update_layout(mapbox_style="open-street-map")
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

def treeFood(data):
    foodsList = ['papaya', 'potato', 'snake gourd', 'pirandai', 'curry leaves', 'coconut', 'long beans', 'tomato', 'banana', 'custard apple', 'cabbage', 'ridge gourd', 'drumstick leaves', 'carrot', 'pumpkin', ' ladies finger', 'lentil', 'kovakkai', 'bitter gourd', 'pomegranate', 'ladies finger', 'drumstick', 'beans', 'brinjal']
    foods = pd.DataFrame(columns = ['Food', 'Count'])
    i = 0
    for food in foodsList:
        foods.loc[i] = [food, data['locallyAvailableFoodsConsumed'].str.count(food.lower()).sum()]
        i += 1

    foodPlot = px.bar(foods, x = 'Count', y = 'Food', color = 'Food', orientation= 'h', title = 'Locally Available Foods Consumed', width = 1000)

    treesList = ['papaya', 'drumstick', 'cocount', 'banana', 'pomegranate', 'guava', 'neem', 'mango', 'NO' ]
    trees = pd.DataFrame(columns = ['Tree', 'Count'])
    i = 0
    for tree in treesList:
        trees.loc[i] = [tree, data['treesOwnedIfAny'].str.count(tree).sum()]
        i += 1

    treePlot = px.bar(trees, x = 'Count', y = 'Tree', color = 'Tree', orientation= 'h', title = 'Trees Owned', width = 1000)

    return foodPlot, treePlot

head = st.container()
body = st.container()

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
        
        c1, c2 = st.columns(2)
        
        #with c1:
        st.write(dirtyData(temp))
        st.write(
                px.bar(pd.crosstab(PersonalInfo.educationQualification, PersonalInfo.occupation), orientation = 'h', title = 'Highest Educational Qualifications and Occupations', width = 1000))

        #with c2:
        st.write(
            px.bar(pd.crosstab(temp.gender,temp.maritalStatus), color_discrete_map={
    'MARRIED' : 'rgBa(238, 115, 115, 1)',
    'UNMARRIED' : 'rgBa(114, 222, 111, 1)'
}, orientation='h', title = 'Demographic Distribution', width = 1000)
        )
        st.write(
            px.bar(pd.crosstab(temp.Vulnerabilities, temp.gender), color_discrete_map={
    'Male' : 'rgBa(238, 115, 115, 1)',
    'Female' : 'rgBa(114, 222, 111, 1)'
}, orientation='h', title = 'Vulnerabilities', width= 1000)
        )

        locations = LocationData.loc[LocationData._id.isin(temp._id.unique())]
        common = CommonData.loc[CommonData._id.isin(temp._id.unique())]

        st.markdown('###### Locations of Families')
        st.write(
            mapOut(locations)
        )

        st.write(
            px.bar(pd.crosstab(PersonalInfo.educationQualification, PersonalInfo.gender), color_discrete_map={
    'Male' : 'rgBa(238, 115, 115, 1)',
    'Female' : 'rgBa(114, 222, 111, 1)'
}, orientation = 'h', title = 'Highest Educational Qualification and Gender', width= 1000)
        )

        st.write(
            px.bar(pd.crosstab(PersonalInfo.occupation, PersonalInfo.gender), color_discrete_map={
    'Male' : 'rgBa(238, 115, 115, 1)',
    'Female' : 'rgBa(114, 222, 111, 1)'
}, orientation = 'h', title = 'Occupation and Gender', width= 1000)
        )

        st.write(
            px.bar(pd.crosstab(PersonalInfo.tobaccoBasedProductsUsage, PersonalInfo.gender), color_discrete_map={
    'Male' : 'rgBa(238, 115, 115, 1)',
    'Female' : 'rgBa(114, 222, 111, 1)'
}, orientation = 'h', title = 'Tobacco Based Product Usage and Gender', width= 1000)
        )

        st.write(
            px.bar(pd.crosstab(PersonalInfo.alcoholConsumption, PersonalInfo.gender), color_discrete_map={
    'Male' : 'rgBa(238, 115, 115, 1)',
    'Female' : 'rgBa(114, 222, 111, 1)'
}, orientation = 'h', title = 'Alcohol Consumption and Gender', width= 1000)
        )


        st.write(
            px.bar(pd.crosstab(PersonalInfo.oldAgePension, PersonalInfo.gender), color_discrete_map={
    'Male' : 'rgBa(238, 115, 115, 1)',
    'Female' : 'rgBa(114, 222, 111, 1)'
}, orientation = 'h', title = 'Old Age Pension and Gender', width= 1000)
        )

        st.write(px.bar(pd.crosstab(PersonalInfo['Age Group'], PersonalInfo['educationQualification']), title = 'Age Group and Highest Educational Qualification', width = 1000, orientation = 'h'))


        st.write(px.bar(pd.crosstab(PersonalInfo['Age Group'], PersonalInfo['occupation']), title = 'Age Group and Occupation',  width = 1000, orientation = 'h'))

        
        food, tree = treeFood(common)

        st.write(food)
        st.write(tree)
