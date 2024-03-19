from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from streamlit_navigation_bar import st_navbar
import pages as pg

LOGGER = get_logger(__name__)

def show_home():

    text = '''
        # Home
        **objectives : introduce the tracker, its objective and added value + show snapshots of data to drive exploration** 
        
        - Presentation of the tracker   
            - Objective of the tracker: Collect, format, and make available 
              data from Country-by-Country Reports (CbCRs) disclosed by companies  
            - Why : facilitate access to CbCR data to all  
                - CbCRs data is instrumental for analyzing companies' tax
                 practices  
                - CbCRs data is public but not centralized/standardized, 
                hence difficult to access  
                - Difficulty to access will grow as way more reports are 
                expected  
        - Snapshot of the database  
            - Overview of available data  
                - Number of tracked reports  
                - Number of companies with at least one report  
                - Breakdown of the number of companies with at least 
                one report by hq country/sector  
                - Cloud of available companies with sector color  
            - Example of analysis it unlocks  
                - See where companies declare profits and how much tax 
                they pay : fake dataviz  
                - Detect suspicious behavior by looking at countries 
                with high profits but few employees / high profit per employee : fake data viz  
                - Analyze presence in countries considered tax havens : 
                fake data viz  
            - Database growth  
                - Number of reports actual growth : 
                Number of tracked reports over time  
                - Expected boom within the next 2 years upon the 
                implementation of the directive visualization: Number of 
                multinational corporations subject to the directive  
            - Disclaimer on the inconsistent comprehensiveness of reports 
            published  
                - % of reports with transparent data (pick 1 indicator among transparency indicators)  
        
        - Links to exploration tool  
            - publication trends  
            - companies  
            - countries  
            - sectors  
        - Link to download data  
        - Link to methodology  

    '''
    st.markdown(text)


    # st.markdown("# Viz")
    #
    # data_root_path = './data/'
    #
    # df = pd.read_csv(data_root_path + 'dataset_multi_years_cleaned_completed (1).tab',
    #                  sep='\t')
    # df['year'] = df['year'].astype(int)
    # company_list = list(df['mnc'].unique())[::-1].sort()
    # selected_company = st.selectbox('Select a company', company_list,  index=len(company_list) - 1)
    # df_selected_company = df[df['mnc'] == selected_company]
    # #selected_company_sector = df_selected_company['sector'].unique()
    #
    #
    # df_viz = pd.read_csv(data_root_path + 'vizs.csv')
    # st.table(df_viz)
    #
    # header = st.columns(6)
    # header[0].write("what")
    # header[1].write("viz")
    # header[2].write("how")
    # header[3].write("variaint")
    # header[4].write("comment")
    # header[5].write("specific value")
    #
    # row1 = st.columns(6)
    # row1[0].write("Number of tracked reports")
    #
    # row1[1].write("raw figure")
    # number_of_tracked_reports = len(df.groupby(['year', 'mnc'])['mnc'])
    # row1[1].write(number_of_tracked_reports)
    # row1[2].write("len(df.groupby(['year', 'mnc'])['mnc'])")
    # row1[3].markdown(
    #     '''
    #     - total : len(df.groupby(['year', 'mnc'])['mnc'])
    #     - company : len(df_selected_company.groupby(['year'])['year'])
    #     - sector :
    #     len(df[df['sector'] == selected_company_sector].groupby(['year'])['year'])
    #     - country :
    #     len(df[df['country'] == selected_company_country].groupby(['year'])['year'])
    #     ''')
    # row2 = st.columns(6)
    # row3 = st.columns(6)






        