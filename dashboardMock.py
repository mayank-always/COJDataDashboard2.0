import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# Load the data
data = pd.read_csv('newData.csv')
st.title('COJ Ticket Dashboard')
add_tabs = st.sidebar.selectbox(
    "Choose The Dashboard",
    ("Total Ticket Count", "Types of incidents", "Average Incidents Daily")
)
tab1, tab2, tab3 = st.tabs(["Total Ticket Count", "Types of incidents","Average Incidents Daily"])
# Total Ticket Count
total_tickets = len(data)
avg_res_time= data['Average Total Resolution Time (Days, Minutes & Seconds)']
# Streamlit Dashboard
with tab1:
    st.header('Total Ticket Count')
    st.metric(label="Total Tickets", value= total_tickets, delta= 0, delta_color="off")
    st.header('Average Resolution Time')
    st.write("7 days 17 minutes 26 seconds")
with tab2:
    st.header('Types of Incidents')
    category_counts = data['TypeDescription'].value_counts()
    total_count = category_counts.sum()
    category_percentages = (category_counts / total_count) * 100
    small_categories = category_percentages[category_percentages < 1].index.tolist()
    fig = px.pie(category_counts, values=category_counts, names=category_counts.index, title='Category Distribution')
    st.subheader('Category Distribution Pie Chart')
    st.plotly_chart(fig)
    if small_categories:
        st.subheader('Categories with less than 1% representation:')
    for category in small_categories:
        st.write(f"- {category} ({category_percentages[category]:.2f}%)")
    else:
        st.write('No categories with less than 1% representation.')
with tab3:
   # Ensure the 'DateOnly' column is in datetime format
    data['DateOnly'] = pd.to_datetime(data['DateOnly'])
# Extract year and month from the 'DateOnly' column
    data['Year'] = data['DateOnly'].dt.year
    data['Month'] = data['DateOnly'].dt.strftime('%B')
# Group by month to get total and average incidents across all years
    monthly_data = data.groupby(['Month']).size().reset_index(name='Total Incidents')
    monthly_data['Average Daily Incidents'] = monthly_data['Total Incidents'] / data.groupby(['Month'])['DateOnly'].nunique().values
# Ensure months are in calendar order
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monthly_data['Month'] = pd.Categorical(monthly_data['Month'], categories=month_order, ordered=True)
    monthly_data = monthly_data.sort_values('Month')
# Streamlit app
    st.title('Incidents by Month')
# Create the bar graph with a trend line
    fig1 = px.bar(monthly_data, x='Month', y='Total Incidents', title='Total and Average Daily Incidents by Month',
             labels={'Total Incidents': 'Total Incidents'})
# Adding scatter plot for average daily incidents
    fig1.add_scatter(x=monthly_data['Month'], y=monthly_data['Average Daily Incidents'], mode='lines+markers',
                name='Average Daily Incidents', yaxis='y2')
# Update layout for dual y-axes and increased width
    fig1.update_layout(
        yaxis=dict(title='Total Incidents'),
        yaxis2=dict(title='Average Daily Incidents', overlaying='y', side='right'),
        width=1000,  # Increase the width of the plot
        height=500   # Optional: Increase the height of the plot
    )
    st.plotly_chart(fig1)
