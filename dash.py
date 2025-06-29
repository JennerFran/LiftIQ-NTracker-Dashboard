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
df['Protein_Mean_7d'] = df['Protein'].rolling(window=7).mean()
df['Carbs_Mean_7d'] = df['Carbs'].rolling(window=7).mean()
df['Fat_Mean_7d'] = df['Fat'].rolling(window=7).mean()
df['Cals_Protein'] = 4 * df['Protein']
df['Cals_Carbs'] = 4 * df['Carbs']
df['Cals_Fat'] = 9 * df['Fat']
df['Total_Cals'] = df['Cals_Protein'] + df['Cals_Carbs'] + df['Cals_Fat']
df['Pct_Cals_Protein'] = 100 * df['Cals_Protein']/df['Total_Cals']
df['Pct_Cals_Carbs'] = 100 * df['Cals_Carbs']/df['Total_Cals']
df['Pct_Cals_Fat'] = 100 * df['Cals_Fat']/df['Total_Cals']
df['Pct_7dMA_Protein'] = df['Pct_Cals_Protein'].rolling(window=7).mean()
df['Pct_7dMA_Carbs'] = df['Pct_Cals_Carbs'].rolling(window=7).mean()
df['Pct_7dMA_Fat'] = df['Pct_Cals_Fat'].rolling(window=7).mean()

# Sidebar options
st.sidebar.image("logo.png", width=150)
st.sidebar.markdown("## Navigation")
view = st.sidebar.radio("Choose Plot:", ["Calories", "Deficit","Protein", "Carbohydrates", "Fat", "Percentages"])

# Title
st.title("LiftIQ: Daily Calorie and Macronutrient Tracker")
st.caption("Built with Python 💻 | Powered by Discipline 💪")

# Show plot
if view == "Calories":
    fig = px.line(df, x='Date', y=['Kcal', 'Maintenance', 'Calories_Mean_7d'], 
                  title='Daily Calories')                 
    st.plotly_chart(fig, use_container_width=True)

elif view == "Deficit":
     fig = px.line(df, x='Date', y=['Deficit', 'Deficit_Mean_7d'],
                  title='Daily Calorie Deficit')
     # Add horizontal line at y = 0
     fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Line", annotation_position="top left")
     st.plotly_chart(fig, use_container_width=True)

elif view == "Protein":
    fig = px.line(df, x='Date', y=['Protein', 'Rec Prot', 'Protein_Mean_7d'],
                  title='Daily Protein',
                  labels={'value': 'Grams'})
    st.plotly_chart(fig, use_container_width=True)

elif view == "Carbohydrates":
    fig = px.line(df, x='Date', y=['Carbs', 'Carbs_Mean_7d'],
                  title='Daily Carbohydrates',
                  labels={'Carbs': 'Grams'})
    st.plotly_chart(fig, use_container_width=True)

elif view == "Fat":
    fig = px.line(df, x='Date', y=['Fat', 'Fat_Mean_7d'],
                  title='Daily Fat',
                  labels={'Fat': 'Grams', 'Date': 'Date'})
    st.plotly_chart(fig, use_container_width=True)

elif view == "Percentages":
    fig = px.line(df, x='Date', y=['Pct_Cals_Protein', 'Pct_7dMA_Protein', 'Pct_Cals_Carbs', 'Pct_7dMA_Carbs', 'Pct_Cals_Fat', 'Pct_7dMA_Fat'],
                  title='Percentages of calories for each macro',
                  labels={'value': 'Percent', 'Date': 'Date'})
    # Líneas de referencia para tus metas de macros
    fig.add_hline(y=35, line_dash="dot", line_color="blue", 
                   annotation_text="Protein Goal (35%)", annotation_position="top right")

    fig.add_hline(y=45, line_dash="dot", line_color="red", 
                   annotation_text="Carbs Goal (45%)", annotation_position="top left")

    fig.add_hline(y=20, line_dash="dot", line_color="green", 
                   annotation_text="Fat Goals (20%)", annotation_position="bottom left")
    st.plotly_chart(fig, use_container_width=True)



# Optional footer
st.markdown("---")
st.markdown("📬 **Let's connect!**  \n[YouTube @LiftIQ](https://www.youtube.com/@LiftIQ_Official) · [GitHub](https://github.com/JennerFran) · [LinkedIn](https://linkedin.com/in/francodatascience)")

