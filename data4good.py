from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Company explorer",
        page_icon="👋",
    )

    st.title('Company explorer')

    st.markdown("objectives : analyze CBCR data from a given company "
                "e.g., analyze data from Shell")

    st.markdown("#### raw data - Cleaned CBCR data")
    data_root_path = './data/'
    df = pd.read_csv(data_root_path + 'dataset_multi_years_cleaned_completed (1).tab',
                     sep='\t')
    df['year'] = df['year'].astype(int)
    st.dataframe(df, height=100)

    df_map = pd.read_csv(data_root_path + 'average-latitude-longitude-countries.csv')
    df = df.merge(df_map, left_on='jur_name', right_on='Country')
    st.map(df,
           latitude='Latitude',
           longitude='Longitude',
           size='taxe_paid',
           #color='sector'
           )
    st.markdown('''
    
    ## CBCR data for the selected company
    
    On the left panel, you will find a select box for a company selection
    
    *SELECT BOX “COMPANY” (possibly ordered by sector)
    note to inform that if a company is absent, it means we have no report + that reports can be submitted through contact page*
        ''')

    selected_element_map = {}

    def create_selection(
            selection_colmun_name,
            selection_colmun_label,
    ):
        element_list = list(df[selection_colmun_name].unique())[::-1]

        selected_element_map[selection_colmun_name] = st.selectbox('Select a ' + selection_colmun_label, element_list, index=len(element_list) - 1)
        df_selected_element = df[df[selection_colmun_name] == selected_element_map[selection_colmun_name]]
        return df_selected_element

    with st.sidebar:
        df_selected_company = create_selection(
            'mnc',
            'company'
        )
        df_selected_fiscal_year = create_selection(
            'year',
            'fiscal year'
        )


    st.dataframe(df_selected_company)

    st.markdown('''
    # 1. Reports disclosed
        
    ### - reports published and transparency scores
        
    As a company has been selected, the dataset is now filtered according to this company.
    We ccan now group together all rows corresponding to a year (group by year) and compute 
    for each group several metric : 
    
    year_count will count the number of rows in the group (in our case this corresponds to the 
    number of report produce by the company on the given year
    ....
    ''')
    st.map(df_selected_company,
           latitude='Latitude',
           longitude='Longitude',
           size='taxe_paid',
           # color='sector'
           )
    df_selected_company_per_year = (df_selected_company.groupby(['year'])
                                    .aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    ))
    df_selected_company_per_year.columns = df_selected_company_per_year.columns.map('_'.join)
    df_selected_company_per_year = df_selected_company_per_year.reset_index()

    st.markdown('''#### dataframe of selected company peryear''')
    st.dataframe(df_selected_company_per_year)

    st.markdown('''#### line chart showing the evolution of number of report over the time''')
    st.line_chart(df_selected_company_per_year, x='year', y='year_count')


    st.markdown('''
    ### - comparison with sector / country
        
    #### - per company
    
    For each company, the same grouping system is applied. A box plot for each year is compute
    given an indication of the distribution of the number of report per year and per company.
    On the same graphic, the red dash line indicate the position of the selected company
    
    ''')
    df_company_per_year = df.groupby(['year', 'mnc']).aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    )
    df_company_per_year.columns = df_company_per_year.columns.map('_'.join)
    df_company_per_year = df_company_per_year.reset_index()
    st.dataframe(df_company_per_year)

    fig = px.box(df_company_per_year, x="year", y="year_count")
    plot_min = df_selected_company_per_year['year'].min()
    plot_max = df_selected_company_per_year['year'].max()
    # add a second axis that overlays the existing one
    fig.layout.xaxis2 = go.layout.XAxis(overlaying='x', range=[plot_min, plot_max], showticklabels=False)
    fig.add_scatter(
        x=list(df_selected_company_per_year['year']),
        y=list(df_selected_company_per_year['year_count']),
        mode='lines', xaxis='x2',
        showlegend=False, line=dict(dash='dash', color="firebrick", width=5))
    st.plotly_chart(fig)



    st.markdown('''
    #### - per sector
    ''')
    df_per_sector_per_year = df.groupby(['year', 'sector']).aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    )
    df_per_sector_per_year.columns = df_per_sector_per_year.columns.map('_'.join)
    df_per_sector_per_year = df_per_sector_per_year.reset_index()

    st.line_chart(df_per_sector_per_year, x='year', y='year_count', color='sector')
    st.markdown('''
       By sector, distribution of the number of report (for any year)
       ''')
    df_per_sector = df.groupby(['sector']).aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    )
    df_per_sector.columns = df_per_sector.columns.map('_'.join)
    df_per_sector = df_per_sector.reset_index()
    fig = px.box(df_per_sector, x="sector", y="year_count")
    st.plotly_chart(fig)

    st.markdown('''
       In the same sector as the selected company, distribution of the number of report
       per year
       ''')
    company_sector = list(df_selected_company['sector'].unique())[0]
    df_of_sector = df[df['sector']==company_sector]
    st.dataframe(df_of_sector)
    df_of_sector_per_year = df_of_sector.groupby(['year', 'mnc']).aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    )
    df_of_sector_per_year.columns = df_of_sector_per_year.columns.map('_'.join)
    df_of_sector_per_year = df_of_sector_per_year.reset_index()

    fig = px.box(df_of_sector_per_year, x="year", y="year_count")
    plot_min = df_selected_company_per_year['year'].min()
    plot_max = df_selected_company_per_year['year'].max()
    # add a second axis that overlays the existing one
    fig.layout.xaxis2 = go.layout.XAxis(overlaying='x', range=[plot_min, plot_max], showticklabels=False)
    fig.add_scatter(
        x=list(df_of_sector_per_year['year']),
        y=list(df_of_sector_per_year['year_count']),
        mode='lines', xaxis='x2',
        showlegend=False, line=dict(dash='dash', color="firebrick", width=5))
    st.plotly_chart(fig)


    st.markdown('''
    #### - per country
    ''')

    df_per_country_per_year = df.groupby(['year', 'jur_name']).aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    )
    df_per_country_per_year.columns = df_per_country_per_year.columns.map('_'.join)
    df_per_country_per_year = df_per_country_per_year.reset_index()
    st.dataframe(df_per_country_per_year)
    st.line_chart(df_per_country_per_year, x='year', y='year_count', color='jur_name')


    st.markdown('''
       By country, distribution of the number of report (for any year)
       ''')
    df_per_country = df.groupby(['jur_name']).aggregate(
        {
            'year': ['count'],
            'tax_paid': ['sum', 'min', 'max', 'mean']
        }
    )
    df_per_country.columns = df_per_country.columns.map('_'.join)
    df_per_country = df_per_country.reset_index()
    fig = px.box(df_per_country, x="jur_name", y="year_count")
    st.plotly_chart(fig)



    st.markdown('''
    # 2. Analysis of CbCRs published
       SELECT BOX "FISCAL YEAR"
        a) company’s key data (on selected FY) : 
            - how big is it ? total revenues, total related party revenues, pre-tax profits, taxes paid, employees
            - where does it operate ? top jurisdictions for revenues (or other metric ?) 
    
    ''')

    st.markdown('''### data for selected fiscal year''')
    st.dataframe(df_selected_fiscal_year)

    st.markdown('''### a) company’s key data (on selected FY) : 
    #### - how big is it ? total revenues, total related party revenues, pre-tax profits, taxes paid, employees
    ''')
    columns_of_interest =['total_revenues', 'related_revenues', 'profit_before_tax', 'tax_paid', 'employees']
    df_fiscal_year_per_company = df.groupby(['mnc'])[columns_of_interest].sum().reset_index()
    st.dataframe(df_fiscal_year_per_company)


    st.markdown('''#### - where does it operate ? top jurisdictions for revenues (or other metric ?)''')
    df_fiscal_year_country = df.groupby(['jur_name']).aggregate(
        {
            'mnc': ['count'],
            'total_revenues': ['sum'],
            'tax_paid': ['sum'],
            'related_revenues': ['sum'],
            'profit_before_tax': ['sum'],
            'employees': ['sum']
        }
    )
    df_fiscal_year_country.columns = df_fiscal_year_country.columns.map('_'.join)
    df_fiscal_year_country = df_fiscal_year_country.reset_index()
    st.dataframe(df_fiscal_year_country)
    # st.line_chart(df_selected_element, x='year', y="profit_before_tax")


if __name__ == "__main__":
    run()