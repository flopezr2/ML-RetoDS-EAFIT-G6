# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:59:05 2021

@author: flopezr
"""

import streamlit as st
from PIL import Image

def app():
    imagen_bpo=Image.open('C:\\Users\\Admin\\OneDrive\\Documentos\\DataScience2021-2\\Trabajos_propios_felipe\\Proyecto_final\\ML-RetoDS-EAFIT-G6\\streamlit_app\\compras.png')
    st.image(imagen_bpo,use_column_width=True,caption='PROYECTO FINAL CIENCIA DE DATOS')
    st.markdown("<h1 style='text-align: center; color: #133EBE;'>Predicción de fechas de entrega de bienes y/o servicios con algoritmos de Aprendizaje Supervisado –ML-</h1>", unsafe_allow_html=True)
    
if __name__=='__main__':
    app()