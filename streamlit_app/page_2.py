# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 12:29:43 2021

@author: flopezr
"""
import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
#from pyxlsb import open_workbook as open_xlsb
import datetime

from pycaret.regression import load_model,predict_model

df=pd.read_excel('C:\\Users\\Admin\\OneDrive\\Documentos\\DataScience2021-2\\Trabajos_propios_felipe\\Proyecto_final\\ML-RetoDS-EAFIT-G6\\streamlit_app\\bd_nueva.xlsx')




def app():
    #cargamos el modelo
    modelo=load_model('C:\\Users\\Admin\\OneDrive\\Documentos\\DataScience2021-2\\Trabajos_propios_felipe\\Proyecto_final\\ML-RetoDS-EAFIT-G6\\streamlit_app\\modelo_final')
    modelo_proceso=load_model('C:\\Users\\Admin\\OneDrive\\Documentos\\DataScience2021-2\\Trabajos_propios_felipe\\Proyecto_final\\ML-RetoDS-EAFIT-G6\\streamlit_app\\modelo_procesos')
    #Diseño de la pagina
    select_box=st.sidebar.selectbox('Tipo de predicción',('Unica predicción Online','Grupo de predicciones'))
    st.sidebar.info('Modelo predictivo del tiempo de aprobación de la orden y del tiempo de entrega del pedido usando un modelo de bosques aleatorios donde se puede hacer un batch de predicciónes con un archivo de excel con los datos o una solo predicción ingresando los parametros ')
    
    st.markdown("<h1 style='text-align: center; color: #1338BE ;>TIEMPO DE APROBACIÓN</h1>", unsafe_allow_html=True)
    #datos previos
    
    #Funciones de la pagina 
    
    if select_box=='Unica predicción Online':

            today=datetime.date.today()
            FECHAORDEN=st.date_input('Fecha orden(AAAA-MM-DD)',value=today)
            
            USUARIO= st.number_input('Numero usuario solicitante',min_value=0)
            
            USUARIO1=str('Usuario solicitante '+str(USUARIO))
            
           
            
            if USUARIO1 in df['USUARIO'].values:
                usuario_aprobador=list(df.loc[df['USUARIO']==USUARIO1,'USUARIO APROBADOR'].unique())
                usuario_aprobador.remove(np.nan)
               
            else:
                usuario_aprobador=[]
            
            
            USUARIOAPROBADOR=st.selectbox('Seleccione el usuario aprobador',usuario_aprobador)
            categorias=list(df['CATEGORÍA'].unique())
            #categorias.remove(np.nan)
            categoria=st.selectbox('Seleccione la categoría del producto',categorias)
            
            
            
            output=""
       
            input_dict={'FECHA ORDEN':FECHAORDEN,'USUARIO':USUARIO1,
                   'USUARIO APROBADOR':USUARIOAPROBADOR,
                   'CATEGORÍA':categoria}
            base_datos=pd.DataFrame([input_dict])
            base_datos.dropna(axis=1,inplace=True)
            base_datos['FECHA ORDEN']=pd.to_datetime(base_datos['FECHA ORDEN'])
            base_datos['dia fecha orden']=base_datos['FECHA ORDEN'].dt.dayofweek #0 lunes, 6 domingo
            base_datos['mes fecha orden']=base_datos['FECHA ORDEN'].dt.month #Meses de ordbación 
            base_datos['semana del año orden']=base_datos['FECHA ORDEN'].dt.isocalendar().week
            base_datos['semana del año orden']=base_datos['semana del año orden'].astype('float64')
            
            
            #st.table(base_datos)
            proveedor=list(df.loc[df['CATEGORÍA']==base_datos['CATEGORÍA'][0],'PROVEEDOR'].unique())
            #proveedor.remove(np.nan)
            proveedor=st.selectbox('Seleccione un proveedor',proveedor,index=0)
      
            if st.button('Hacer predicción'):
                prediction_df=predict_model(estimator=modelo,data=base_datos)
                prediccion=prediction_df['Label'][0]
                output=(datetime.timedelta(prediccion)+base_datos['FECHA ORDEN'])[0]
                output=pd.to_datetime(output)
                st.success('Posible fecha de aprobación: {}'.format(output.date()))
                
            #-------------------------------------------prediccioon de tiempo de proceso-------------------------------------
                
            
            
        
            
                input_dic2={'FECHA APROBACION':output,'USUARIO':USUARIO1,
                       'USUARIO APROBADOR':USUARIOAPROBADOR,
                       'CATEGORÍA':categoria,'PROVEEDOR':proveedor}
                base_datos2=pd.DataFrame([input_dic2])
                base_datos2['FECHA APROBACION']=pd.to_datetime(base_datos2['FECHA APROBACION'])
                base_datos2['dia fecha aprobacion']=base_datos2['FECHA APROBACION'].dt.dayofweek #0 lunes, 6 domingo
                base_datos2['mes fecha aprobacion']=base_datos2['FECHA APROBACION'].dt.month #Meses de aprobación 
                base_datos2['semana del año aprobacion']=base_datos2['FECHA APROBACION'].dt.isocalendar().week
                prediccion2=predict_model(estimator=modelo_proceso,data=base_datos2)
                prediccion2_=prediccion2['Label'][0]
                output=pd.to_datetime(output)
                fecha_entrega_estimada=(datetime.timedelta(prediccion2_)+output)
                st.success('La posible fecha de entrega será: {}'.format(fecha_entrega_estimada.date()))
                
                
                
            
            

        
    if select_box=='Grupo de predicciones':
        
        file_upload=st.file_uploader('Subir documento',type=['xlsx'])
        
        if file_upload is not None:
            data_=pd.read_excel(file_upload)
            data_['FECHA ORDEN']=pd.to_datetime(data_['FECHA ORDEN'])
            data_['dia fecha orden']=data_['FECHA ORDEN'].dt.dayofweek #0 lunes, 6 domingo
            data_['mes fecha orden']=data_['FECHA ORDEN'].dt.month #Meses de ordbación 
            data_['semana del año orden']=data_['FECHA ORDEN'].dt.isocalendar().week
            data_['semana del año orden']=data_['semana del año orden'].astype('float64')
            predicciones=predict_model(estimator=modelo,data=data_)
            predicciones['FECHA APROBACIÓN ESTIMADA']=predicciones['FECHA ORDEN']+ (predicciones['Label'].apply(lambda x: datetime.timedelta(x)))
            fecha_orden=pd.to_datetime(predicciones['FECHA ORDEN'])
            pre=pd.to_datetime(predicciones['FECHA APROBACIÓN ESTIMADA'])
            dic_out={'NÚMERO PEDIDO':predicciones['NÚMERO PEDIDO'],'ORDEN NÚMERO':predicciones['ORDEN NÚMERO'],
                     'FECHA ORDEN':fecha_orden.dt.date,'FECHA DE APROBACIÓN ESTIMADA':pre.dt.date,'PROVEEDOR':predicciones['PROVEEDOR'],
                     'USUARIO':predicciones['USUARIO'],'CATEGORÍA':predicciones['CATEGORÍA'],'PRODUCTO O SERVICIO':predicciones['PRODUCTO O SERVICIO'],
                     'CANTIDAD PEDIDA':predicciones['CANTIDAD PEDIDA']}
            db_output=pd.DataFrame(dic_out)
            #-----------------fecha de entrega estimada-----------------------------------------------
            db_output['dia fecha aprobación']=pd.to_datetime(db_output['FECHA DE APROBACIÓN ESTIMADA']).dt.dayofweek 
            db_output['mes fecha aprobacion']=pd.to_datetime(db_output['FECHA DE APROBACIÓN ESTIMADA']).dt.month
            db_output['semana del año aprobacion']=pd.to_datetime(db_output['FECHA DE APROBACIÓN ESTIMADA']).dt.isocalendar().week
            prediccion2=predict_model(estimator=modelo_proceso,data=db_output)
            db_output['POSIBLE FECHA ENTREGA']=prediccion2['FECHA DE APROBACIÓN ESTIMADA']+ (prediccion2['Label'].apply(lambda x: datetime.timedelta(x)))
            
            #fecha_entrega_estimada=(datetime.timedelta(prediccion2)+output)
            db_output1=db_output[['NÚMERO PEDIDO','ORDEN NÚMERO','FECHA ORDEN','FECHA DE APROBACIÓN ESTIMADA','POSIBLE FECHA ENTREGA']]
            
            st.table(db_output1.head(30))
            #st.write(predicciones[['FECHA ORDEN','FECHA APROBACIÓN ESTIMADA']])
        
            predicciones_dow=db_output[['NÚMERO PEDIDO','ORDEN NÚMERO','CATEGORÍA','PRODUCTO O SERVICIO','FECHA ORDEN','CANTIDAD PEDIDA','FECHA DE APROBACIÓN ESTIMADA',
                                        'POSIBLE FECHA ENTREGA']]
            predicciones_dow=pd.DataFrame(predicciones_dow)
            def to_excel(df):
                output = BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook = writer.book
                worksheet = writer.sheets['Sheet1']
                format1 = workbook.add_format({'num_format': '0.00'}) 
                worksheet.set_column('A:A', None, format1)  
                writer.save()
                processed_data = output.getvalue()
                return processed_data
            df_xlsx = to_excel(predicciones_dow)
            
            st.download_button('Descargar predicciones',data=df_xlsx,file_name= 'predicciones.xlsx')

    

if __name__=='__main__':
      app()