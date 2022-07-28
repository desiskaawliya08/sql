import pandas as pd 
import streamlit as st 
import plotly.express as px
from PIL import Image

st.set_page_config(page_title='Data Penindakan Pelanggaran Lalin 2022 DKI Jakarta')
st.header('Penindakan Pelanggaran Lalu Lintas 2022 DKI Jakarta')


### --- LOAD DATAFRAME
excel_file = 'uas_visdat.xlsx'
sheet_name = 'Sheet1'

df = pd.read_excel(excel_file,
                   sheet_name=sheet_name,
                   usecols='A:I',
                   header=0)

df_bapTilang = pd.read_excel(excel_file,
                             sheet_name= sheet_name,
                             usecols='K:L',
                             header=0)

# --- STREAMLIT SELECTION
bln = df['bulan'].unique().tolist()
derek = df['penderekan'].unique().tolist()

derek_selection = st.slider('Rasio Penderekan:',
                        min_value= min(derek),
                        max_value= max(derek),
                        value=(min(derek),max(derek)))

bulan_selection = st.multiselect('Bulan:',
                                  bln,
                                  default=bln)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['penderekan'].between(*derek_selection)) & (df['bulan'].isin(bulan_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['wilayah']).count()[['penderekan']]
df_grouped = df_grouped.rename(columns={'penderekan': 'Derek'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   x='wilayah',
                   y='Derek',
                   text='Derek',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = st.columns(2)
image = Image.open('lalin.jpg')
print(image)
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_bapTilang,
                title='Total BAP Tilang',
                values='bap_tilang1',
                names='Wilayah')

st.plotly_chart(pie_chart)