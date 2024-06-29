import streamlit as st
import pandas as pd
import numpy as np


# Set page title
st.title('COJ Ticket Dashboard')

# Sidebar options
add_tabs = st.sidebar.radio(
    "Choose The Dashboard",
    ("Total Ticket Count", "Types of Incidents", "Average Incidents Daily", "Chatbot", "Daily Average Cases by Year")
)

# Function to upload data
@st.cache(allow_output_mutation=True)
def upload_data():
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None

# Upload data
data = upload_data()

# Tabs based on uploaded data
if data is not None:
    if add_tabs == "Total Ticket Count":
        st.header('Total Ticket Count')
        total_tickets = len(data)
        avg_res_time = data['Average Total Resolution Time (Days, Minutes & Seconds)']
        st.metric(label="Total Tickets", value=total_tickets, delta=0, delta_color="off")
        st.header('Average Resolution Time')
        st.write("7 days 17 minutes 26 seconds")

    elif add_tabs == "Types of Incidents":
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

    elif add_tabs == "Average Incidents Daily":
        st.header('Average Incidents Daily')
        data['DateOnly'] = pd.to_datetime(data['DateOnly'])
        data['Year'] = data['DateOnly'].dt.year
        data['Month'] = data['DateOnly'].dt.strftime('%B')
        monthly_data = data.groupby(['Month']).size().reset_index(name='Total Incidents')
        monthly_data['Average Daily Incidents'] = monthly_data['Total Incidents'] / data.groupby(['Month'])['DateOnly'].nunique().values
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        monthly_data['Month'] = pd.Categorical(monthly_data['Month'], categories=month_order, ordered=True)
        monthly_data = monthly_data.sort_values('Month')
        fig1 = px.bar(monthly_data, x='Month', y='Total Incidents', title='Total and Average Daily Incidents by Month', labels={'Total Incidents': 'Total Incidents'})
        fig1.add_scatter(x=monthly_data['Month'], y=monthly_data['Average Daily Incidents'], mode='lines+markers', name='Average Daily Incidents', yaxis='y2')
        fig1.update_layout(
            yaxis=dict(title='Total Incidents'),
            yaxis2=dict(title='Average Daily Incidents', overlaying='y', side='right'),
            width=1000,
            height=500
        )
        st.plotly_chart(fig1)

    elif add_tabs == "Chatbot":
        st.header('Chatbot')
        st.write("Work in progress.")

    elif add_tabs == "Daily Average Cases by Year":
        st.header('Daily Average Cases by Year')
        data['DateOnly'] = pd.to_datetime(data['DateOnly'])
        data['Year'] = data['DateOnly'].dt.year
        data['DayOfYear'] = data['DateOnly'].dt.dayofyear
        daily_avg_data = data.groupby(['Year', 'DayOfYear']).size().reset_index(name='Daily Cases')
        annual_avg_data = daily_avg_data.groupby('Year')['Daily Cases'].mean().reset_index(name='Average Daily Cases')
        fig2 = px.line(annual_avg_data, x='Year', y='Average Daily Cases', title='Average Daily Cases by Year', labels={'Average Daily Cases': 'Average Daily Cases'})
        fig2.update_layout(
            xaxis=dict(
                dtick=1
            )
        )
        st.plotly_chart(fig2)
else:
    st.write("Upload a CSV file to get started.")
