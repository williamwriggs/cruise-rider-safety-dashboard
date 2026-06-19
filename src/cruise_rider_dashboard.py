import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Cruise Rider Safety Dashboard', layout='wide')

st.title('Cruise Rider Safety Dashboard')
st.caption('Companion dashboard for: Advances in Automated Driving: Perceptions of Safety, Operations, and Comfort From Riders')

st.info('Initial deployment scaffold. Upload or add cruise_research_rider_public_safe.csv to the data folder to activate analytics.')

st.markdown('### Planned Views')
st.markdown('- Rider vs Non-rider comparison')
st.markdown('- Scenario mentions')
st.markdown('- Sentiment distribution')
st.markdown('- Trip purpose')
st.markdown('- Alternative mode')
st.markdown('- Late-night mobility')
st.markdown('- Value priorities')

try:
    df = pd.read_csv('data/cruise_research_rider_public_safe.csv')
    st.success(f'Loaded {len(df)} records')
    if 'Scenario' in df.columns:
        fig = px.bar(df['Scenario'].value_counts().reset_index(), x='Scenario', y='count')
        st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.warning('Dataset not yet present in repository. Dashboard scaffold deployed successfully.')
