import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Advanced Weather Dashboard", layout="wide")

st.title("🌦 Weather Data Analysis")

# Load dataset
df = pd.read_csv("weatherHistory.csv")

# Fix column spacing
df.columns = df.columns.str.strip()

# Convert date column
df["Formatted Date"] = pd.to_datetime(df["Formatted Date"], utc=True, errors="coerce")

# Extract date parts
df["Year"] = df["Formatted Date"].dt.year
df["Month"] = df["Formatted Date"].dt.month
df["Day"] = df["Formatted Date"].dt.day

# Sidebar Filters
st.sidebar.header("Filter Options")

year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
month = st.sidebar.slider("Select Month", 1, 12, (1,12))

filtered_df = df[(df["Year"] == year) &
                 (df["Month"] >= month[0]) &
                 (df["Month"] <= month[1])]

# Dataset Preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

# Basic statistics
st.subheader("Dataset Statistics")
st.write(filtered_df.describe())

# -------------------------
# Temperature Trend
# -------------------------
st.subheader("Monthly Average Temperature")

temp = filtered_df.groupby("Month")["Temperature (C)"].mean().reset_index()

fig1 = px.line(temp,
               x="Month",
               y="Temperature (C)",
               markers=True,
               title="Monthly Temperature Trend")

st.plotly_chart(fig1, use_container_width=True)

# -------------------------
# Humidity Trend
# -------------------------
st.subheader("Monthly Humidity Trend")

humidity = filtered_df.groupby("Month")["Humidity"].mean().reset_index()

fig2 = px.line(humidity,
               x="Month",
               y="Humidity",
               markers=True,
               title="Monthly Humidity Trend")

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Weather Summary
# -------------------------
st.subheader("Weather Type Distribution")

summary = filtered_df["Summary"].value_counts().reset_index()
summary.columns = ["Weather Type","Count"]

fig3 = px.bar(summary,
              x="Weather Type",
              y="Count",
              title="Weather Distribution")

st.plotly_chart(fig3, use_container_width=True)

# -------------------------
# Temperature vs Humidity
# -------------------------
st.subheader("Temperature vs Humidity")

fig4 = px.scatter(filtered_df,
                  x="Temperature (C)",
                  y="Humidity",
                  color="Humidity",
                  title="Temperature vs Humidity Relationship")

st.plotly_chart(fig4, use_container_width=True)

# -------------------------
# Heatmap Correlation
# -------------------------
st.subheader("Weather Feature Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include=["float64","int64"])

fig8, ax = plt.subplots()
sns.heatmap(numeric_df.corr(),
            annot=True,
            cmap="coolwarm",
            ax=ax)

st.pyplot(fig8)

# -------------------------
# Daily Temperature
# -------------------------
st.subheader("Daily Temperature Trend")

daily_temp = filtered_df.groupby("Day")["Temperature (C)"].mean().reset_index()

fig9 = px.line(daily_temp,
               x="Day",
               y="Temperature (C)",
               title="Daily Temperature")

st.plotly_chart(fig9, use_container_width=True)

# -------------------------
# Wind Bearing
# -------------------------
st.subheader("Wind Bearing Analysis")

fig10 = px.histogram(filtered_df,
                     x="Wind Bearing (degrees)",
                     nbins=50,
                     title="Wind Direction Distribution")

st.plotly_chart(fig10, use_container_width=True)

st.write("Advanced Weather Dashboard using Streamlit ")