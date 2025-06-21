import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz

# CSV published link for sheet Kcal
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSbTXMRRDRlwUjBWHEH3vonSAMdeAO_Msd7vzilOEn1Xcgq4mczGbThacy28t2XHVK8yMOf29-bvGWl/pub?gid=2018616909&single=true&output=csv"
df = pd.read_csv(sheet_url)

# Data Cleaning and Type Conversion
df.dropna(how='all', inplace=True)

# Convert date and numerical columns
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Kcal'] = pd.to_numeric(df['Kcal'], errors='coerce')
df['Protein'] = pd.to_numeric(df['Protein'], errors='coerce')
df['Carbs'] = pd.to_numeric(df['Carbs'], errors='coerce')
df['Fat'] = pd.to_numeric(df['Fat'], errors='coerce')
df['Maintenance'] = pd.to_numeric(df['Maintenance'], errors='coerce')
df['Rec Prot'] = pd.to_numeric(df['Rec Prot'], errors='coerce')
df['Deficit'] = pd.to_numeric(df['Deficit'], errors='coerce')

# Daily Calories Visualization with 7-Day Moving Average

# Add moving average
df['Calories_Mean_7d'] = df['Kcal'].rolling(window=7).mean()
df['Deficit_Mean_7d'] = df['Deficit'].rolling(window=7).mean()

# Sidebar options
st.sidebar.image("logo.png", width=150)
st.sidebar.markdown("## Navigation")
view = st.sidebar.radio("Choose Plot:", ["Calorie Plot", "7D Mov Avg Calories", "Deficit", "7D Mov Avg Deficit","Protein", "Carbohydrates", "Fat"])

# Title
st.title("LiftIQ: Daily Calorie and Macronutrient Tracker")
st.caption("Built with Python 💻 | Powered by Discipline 💪")

# Show plot
if view == "Calorie Plot":
    fig = px.line(df, x='Date', y=['Kcal', 'Maintenance'], title='Daily Calories')
    st.plotly_chart(fig, use_container_width=True)

elif view == "7D Mov Avg Calories":
    fig = px.line(df, x='Date', y=['Calories_Mean_7d', 'Maintenance'],
                  title='Daily Calories 7 Days Moving Average')
    st.plotly_chart(fig, use_container_width=True)

elif view == "Deficit":
    fig = px.line(df, x='Date', y='Deficit',
                  title='Daily Caloric Deficit')
    st.plotly_chart(fig, use_container_width=True)

elif view == "7D Mov Avg Deficit":
    fig = px.line(df, x='Date', y='Deficit_Mean_7d',
                  title='Daily Caloric Deficit 7 Days Moving Average')
    st.plotly_chart(fig, use_container_width=True)

elif view == "Protein":
    fig = px.line(df, x='Date', y=['Protein', 'Rec Prot'],
                  title='Daily Protein')
    st.plotly_chart(fig, use_container_width=True)

elif view == "Carbohydrates":
    fig = px.line(df, x='Date', y='Carbs',
                  title='Daily Carbohydrates')
    st.plotly_chart(fig, use_container_width=True)

elif view == "Fat":
    fig = px.line(df, x='Date', y='Fat',
                  title='Daily Fat')
    st.plotly_chart(fig, use_container_width=True)



# Optional footer
st.markdown("---")
st.markdown("📬 **Let's connect!**  \n[YouTube @LiftIQ](https://www.youtube.com/@LiftIQ_Official) · [GitHub](https://github.com/JennerFran) · [LinkedIn](https://linkedin.com/in/francodatascience)")

