# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 15:23:05 2021

@author: flopezr
"""

import streamlit as st
import numpy as np
import pandas as pd

import datetime

from pycaret.regression import load_model,predict_model

df=pd.read_excel('C:\\Users\\Admin\\OneDrive\\Documentos\\DataScience2021-2\\Trabajos_propios_felipe\\Proyecto_final\\bd_nueva.xlsx')
