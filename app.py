import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
url_view = 'https://drive.google.com/file/d/16YGHVk6p6F7mAMikowqg8CCSeNUsLHc4/view?usp=sharing' 
#Link to the unzipped csv file (with top description lines removed) stored in my Google drive. Anybody with this link can view the csv data file.
path = 'https://drive.google.com/uc?export=download&id='+url_view.split('/')[-2] #path to access the file

#read in the csv file into a dataframe
dfraw = pd.read_csv(path)

#perform the next few steps to make the dataframe tidy
dfraw = dfraw.dropna(axis=1, how='all') #drop columns with no non-null values
cols = ['Indicator Name', 'Indicator Code'] #making a list of unnecessary columns that will be dropped
dfraw = dfraw.drop(cols, axis=1)

# Now we will melt the dataframe so that it is long-form
df = pd.melt(dfraw, id_vars=['Country Name','Country Code'],var_name='Year',value_name='Renewable Energy Cons % of Total Energy Cons')
df['Year'] = pd.to_numeric(df['Year']) #setting the Year column datatype to numeric

# The dataframe is now tidy and ready to use. 

# Add the introductory remarks
st.title('World Bank Data on Renewable Energy Consumption as a Percentage of Total Energy Consumption')
st.write('We will be working with the Renewable Energy Consumption (% Of Total Final Energy Consumption) dataset from the World Bank. This interactive visualisation is created in Python using Plotly Express and Streamlit.')
st.header('Attribution' )
st.subheader('The World Bank (https://datacatalog.worldbank.org)')

st.subheader('Dataset Name')
st.write('Renewable Energy Consumption (% of Total Final Energy Consumption) (https://databank.worldbank.org/reports.aspx?source=2&series=EG.FEC.RNEW.ZS)')

st.subheader('Data Source')
st.write('World Bank, Sustainable Energy for All (SE4ALL) database from the SE4ALL Global Tracking Framework led jointly by the World Bank, International Energy Agency, and the Energy Sector Management Assistance Program.')

st.write('Renewable energy sources include geothermal, solar, tides, wind, biomass, biofuels, and hydroelectric. It will be interesting to see which countries use more renewable energy, and what kind of trend can be discerned in different regions over the years.')

# setting the dropdown list of country and region names, with the default values to start with
Regions = st.multiselect('Choose Country or Region', list(df['Country Name'].unique()), default = ['United Kingdom', 'United States', 'Japan', 'Germany', 'Australia', 'China', 'India'])
new_df = df[df['Country Name'].isin(Regions)] # this is a new dataframe filtered by the choices in the dropdown

#create the new plotly express chart based on this dataframe
fignew = px.line(new_df, x='Year',y='Renewable Energy Cons % of Total Energy Cons',color='Country Name', width = 1100)  #plots an interactive line chart with the data filtered on the country name
st.plotly_chart(fignew) # show the chart

#setting the year selection, with default set to most recent year
Years = st.slider('Choose Year', df['Year'].min(), df['Year'].max(), df['Year'].max())
year_df = df[df['Year']==Years] # this is a new dataframe filtered by the choice of year
figmap = px.choropleth(year_df,locations="Country Code",               
              color="Renewable Energy Cons % of Total Energy Cons",
              hover_name="Country Name",   
              color_continuous_scale='Greens',width=1100, height = 500) #plots a choropleth chart with the data filtered on the year

st.plotly_chart(figmap)

# Add the concluding remarks
"""
## Concluding Remarks

Play around with the countries and the years to see what percentage of the total energy consumption was from renewable energy sources.

I will just point out some observations below. Keep in mind that the data only spans 1990 to 2015, so there may have been significant developments in the last five years!

* Richer, developed countries generally have a low 
percentage of their total energy coming from renewable sources, though some of them show an increasing trend.

* Norway and Iceland, who make use of geothermal energy, have a higher proportion of their consumption coming from renewable energy.

* Many poorer and less-developed countries have MUCH higher levels of renewable energy consumption as a percentage of their total energy consumption, see Nepal for example.

* This could be due to a combination of hydroelectric power for industrial power generation and the use of biomass for domestic energy needs.

* The line charts for India and China show a decreasing trend over the years as they have grown richer, perhaps due to rapidly increasing energy demand that cannot be satisfied fast enough by renewable energy.

All of this gives us a lot to think about. We should keep in mind that 'renewable' does not necessarily mean 'clean' or 'sustainable' or 'environmentally friendly'.
Wood is technically renewable, but using too much of it as fuel could lead to deforestation, and domestic use for cooking produces indoor pollution that has negative effects on the health of household members. Hydroelectric power also has its own challenges with respect to negative environmental consequences.

But we should not be too quick to dismiss the data on this basis. Many developing countries are investing in better renewable energy technology nowadays.

The Renewables Global Status Report (https://ren21.net/gsr-2019/) (GSR), released annually by the Renewable Energy Policy Network for the 21st Century (REN21, a think tank) is a detailed report on the the different sources of renewable energy, their growth rates, and how various countries are using renewable energy.
"""