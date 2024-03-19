from datetime import datetime

import pandas as pd
import streamlit as st
import altair as alt
from numpy.lib.function_base import select
from streamlit.logger import get_logger

import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def show_faq():
    text = '''
    # FAQ
    '''
    st.markdown(text)
