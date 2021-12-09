# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 12:31:07 2021

@author: flopezr
"""

import streamlit as st
import page_2
import page_1

PAGES = {
    "Home": page_1,
    "Modelo predictivo": page_2
}
st.sidebar.title('Navegador')
selection = st.sidebar.radio("Ir a", list(PAGES.keys()))
page = PAGES[selection]

page.app()