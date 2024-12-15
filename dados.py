import pandas as pd
import streamlit as st

@st.cache_data
def carregar():
    df_grupos = pd.read_excel('Orcamento_2.xlsx',sheet_name='DespesaIndividual')
    df=pd.read_csv( 'Gastos.csv',sep=';',decimal=',')
    orcamento = pd.read_excel('Orcamento_2.xlsx',sheet_name='Categoria')
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
    df.drop(columns=['Cor','Etiquetas','Unnamed: 13','Sentimento', 'Compensado'],inplace=True)
    df = df[df['Concluído']=='Sim']
    df['Valor2'] = df['Valor'].str.split(r'\s+', n=1).str[-1]
    df['Valor2']  =df['Valor2'].str.replace('.','')
    df['Valor2']  =df['Valor2'].str.replace(',','.')

    df['Valor2']=pd.to_numeric(df['Valor2'],errors='coerce')
    df=df[df['Tipo']=='Gasto']
    df['Ano-Mês']=df['Data'].dt.year.astype(str)+'-'+df['Data'].dt.month.astype(str).str.zfill(2)
    df=df[df['Data']<=pd.Timestamp.today()]
    df=pd.merge(df,df_grupos,on='Destino',how='left')

    orcamento = orcamento[['Origem', 'Destino',  '01/12/2024',
       '01/01/2025', '01/02/2025', '01/03/2025', '01/04/2025', '01/05/2025',
       '01/06/2025', '01/07/2025', '01/08/2025', '01/09/2025', '01/10/2025',
       '01/11/2025', '01/12/2025']]
    orcamento = pd.melt(orcamento,id_vars=['Origem', 'Destino'],var_name='mes_ano',value_name='total')
    orcamento['mes_ano']=pd.to_datetime(orcamento['mes_ano'],format='%d/%m/%Y')
    orcamento['Ano-Mês']=orcamento['mes_ano'].dt.year.astype(str)+'-'+orcamento['mes_ano'].dt.month.astype(str).str.zfill(2)
    df_temp=df.groupby(['Ano-Mês','Destino'])['Valor2'].sum().reset_index()
    orcamento=pd.merge(orcamento,df_temp,on=['Ano-Mês','Destino'],how='left')
    orcamento['Valor2']=orcamento['Valor2'].fillna(0).astype('float')
    orcamento['Disponivel']=orcamento['total']-orcamento['Valor2']
    orcamento['Disponivel']=orcamento['Disponivel'].fillna(0).astype('float')

   #  df4 = orcamento.groupby(['Origem','Ano-Mês'],dropna=False)[['Disponivel','total']].sum().reset_index()


    return df_grupos,df,orcamento

# df_grupos,df,orcamento,df4 = carregar(),df4