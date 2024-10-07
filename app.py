import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

# Set page configuration
st.set_page_config(
    page_title='Urban Heat Island Effect in Moroccan Cities',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Load data
data = pd.read_csv('interview_data.csv')

# Clean and preprocess data
data['Q2 Multiple Choice'] = data['Q2 Multiple Choice'].str.strip().str.lower()
data['Q3 Multiple Choice'] = data['Q3 Multiple Choice'].str.strip().str.lower()

# Title and header image
st.title('🌆 Urban Heat Island Effect in Moroccan Cities')
st.markdown('---')

# Sidebar for navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Go to:', ['Overview', 'Detailed Analysis', 'Individual Responses'])

# Overview Section
if options == 'Overview':
    st.header('Overview of Survey Results')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Experience of Unusual Temperature Rise')
        q2_counts = data['Q2 Multiple Choice'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(q2_counts, labels=q2_counts.index.str.capitalize(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.subheader('Health Issues Due to Temperature Rise')
        q3_counts = data['Q3 Multiple Choice'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(q3_counts, labels=q3_counts.index.str.capitalize(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax2.axis('equal')
        st.pyplot(fig2)

    st.markdown('---')
    st.subheader('Number of Participants per City')
    city_counts = data['City'].value_counts()
    fig3, ax3 = plt.subplots()
    city_counts.plot(kind='bar', ax=ax3, color='skyblue')
    ax3.set_xlabel('City')
    ax3.set_ylabel('Number of Participants')
    st.pyplot(fig3)

# Detailed Analysis Section
elif options == 'Detailed Analysis':
    st.header('Detailed Analysis of Responses')
    st.subheader('Common Themes in Solutions Suggested (Q5)')

    # Generate word cloud for Q5 answers
    text = ' '.join(data['Q5 Answer'].dropna().values)
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text)
    fig4, ax4 = plt.subplots(figsize=(15, 7.5))
    ax4.imshow(wordcloud, interpolation='bilinear')
    ax4.axis('off')
    st.pyplot(fig4)

    st.markdown('---')
    st.subheader('Suggestions to Address Rising Temperatures')

    # Display all unique suggestions from Q5
    suggestions = data['Q5 Answer'].unique()
    for suggestion in suggestions:
        st.markdown(f"- {suggestion}")

# Individual Responses Section
elif options == 'Individual Responses':
    st.header('Explore Individual Responses')
    selected_city = st.selectbox('Select a city to view responses:', sorted(data['City'].unique()))
    city_data = data[data['City'] == selected_city]

    st.write(f"### Participants from {selected_city}")
    for idx, row in city_data.iterrows():
        st.markdown(f"""
        **Participant {int(row['Person ID'])}:**
        - **Q1:** {row['Q1 Answer']}
        - **Q2:** {row['Q2 Multiple Choice'].capitalize()} - {row['Q2 Text']}
        - **Q3:** {row['Q3 Multiple Choice'].capitalize()} - {row['Q3 Text']}
        - **Q4:** {row['Q4 Answer']}
        - **Q5:** {row['Q5 Answer']}
        """)

# Footer
st.markdown('---')
st.markdown('© 2023 Urban Heat Island Study in Morocco')

# Hide Streamlit style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)