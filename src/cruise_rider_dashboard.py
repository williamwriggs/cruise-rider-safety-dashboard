from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/williamwriggs/rideshare-safety-rider-analysis/main/data/research_rider_dataset.csv"

st.set_page_config(page_title="Cruise Rider Safety Dashboard", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)
    df.columns = [col.strip() for col in df.columns]
    df = df[df["Service"].astype(str).str.lower() == "cruise"].copy()
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    if "Sentiment Score" in df.columns:
        df["Sentiment Score"] = pd.to_numeric(df["Sentiment Score"], errors="coerce")
    return df.dropna(subset=["Latitude", "Longitude"])


def count_table(data: pd.DataFrame, column: str, label: str) -> pd.DataFrame:
    if data.empty or column not in data.columns:
        return pd.DataFrame(columns=[label, "Count", "Percent"])
    table = data[column].fillna("Missing").replace("", "Missing").value_counts().rename_axis(label).reset_index(name="Count")
    table["Percent"] = (table["Count"] / table["Count"].sum() * 100).round(1)
    return table


def bar_count(data: pd.DataFrame, column: str, title: str, color: str | None = None):
    if data.empty or column not in data.columns:
        st.info("No records available for this view.")
        return
    group_cols = [column]
    if color and color in data.columns:
        group_cols.append(color)
    chart_data = data.groupby(group_cols).size().reset_index(name="Count")
    fig = px.bar(chart_data, x=column, y="Count", color=color if color in chart_data.columns else None, barmode="group")
    fig.update_layout(title=title, xaxis_tickangle=-30)
    st.plotly_chart(fig, use_container_width=True)


def mean_value_chart(data: pd.DataFrame):
    value_cols = [
        "Zero_Emission_Score",
        "Accessibility_Score",
        "Distribution_Score",
        "Transit_Connectivity_Score",
    ]
    rows = []
    for col in value_cols:
        if col in data.columns:
            score = pd.to_numeric(data[col], errors="coerce").mean()
            if pd.notna(score):
                rows.append({"Value": col.replace("_Score", "").replace("_", " "), "Average score": score})
    value_df = pd.DataFrame(rows)
    if not value_df.empty:
        fig = px.bar(value_df, x="Value", y="Average score")
        fig.update_layout(title="Average value importance scores", xaxis_tickangle=-25, yaxis_range=[0, 5])
        st.plotly_chart(fig, use_container_width=True)


st.title("Cruise Rider Safety Dashboard")
st.caption("Companion dashboard for: Advances in Automated Driving: Perceptions of Safety, Operations, and Comfort From Riders")

with st.expander("Data note", expanded=True):
    st.write(
        "This app uses the same public-safe Cruise research rider dataset developed for the paper workflow. "
        "Riders are mapped using dropoff coordinates; non-riders are mapped using survey-location coordinates. "
        "Raw survey files are not stored in this repository."
    )
    st.write(f"Data source: `{DATA_URL}`")

try:
    df = load_data()
except Exception as exc:
    st.error("Could not load the Cruise public-safe dataset.")
    st.exception(exc)
    st.stop()

with st.sidebar:
    st.header("Filters")
    respondent_options = sorted(df["Respondent_Group"].dropna().unique()) if "Respondent_Group" in df.columns else []
    scenario_options = sorted(df["Scenario"].dropna().unique()) if "Scenario" in df.columns else []
    sentiment_options = sorted(df["Sentiment"].dropna().unique()) if "Sentiment" in df.columns else []

    selected_respondents = st.multiselect("Respondent group", respondent_options, default=respondent_options)
    selected_scenarios = st.multiselect("Scenario", scenario_options, default=scenario_options)
    selected_sentiments = st.multiselect("Sentiment", sentiment_options, default=sentiment_options)

filtered_df = df.copy()
if selected_respondents:
    filtered_df = filtered_df[filtered_df["Respondent_Group"].isin(selected_respondents)]
if selected_scenarios:
    filtered_df = filtered_df[filtered_df["Scenario"].isin(selected_scenarios)]
if selected_sentiments:
    filtered_df = filtered_df[filtered_df["Sentiment"].isin(selected_sentiments)]

metric_cols = st.columns(5)
metric_cols[0].metric("Records", len(filtered_df))
metric_cols[1].metric("Riders", int((filtered_df["Respondent_Group"] == "Rider").sum()) if "Respondent_Group" in filtered_df.columns else 0)
metric_cols[2].metric("Non-riders", int((filtered_df["Respondent_Group"] == "Non-rider").sum()) if "Respondent_Group" in filtered_df.columns else 0)
metric_cols[3].metric("Scenarios", filtered_df["Scenario"].nunique() if "Scenario" in filtered_df.columns else 0)
metric_cols[4].metric("Avg sentiment", f"{filtered_df['Sentiment Score'].mean():.2f}" if "Sentiment Score" in filtered_df.columns and not filtered_df.empty else "N/A")

st.subheader("Respondent geography")
map_df = filtered_df[["Latitude", "Longitude", "Respondent_Group", "Scenario", "Sentiment"]].dropna()
st.map(map_df.rename(columns={"Latitude": "lat", "Longitude": "lon"}), latitude="lat", longitude="lon", use_container_width=True)

chart_cols = st.columns(2)
with chart_cols[0]:
    bar_count(filtered_df, "Scenario", "Scenario mentions", "Respondent_Group")
with chart_cols[1]:
    bar_count(filtered_df, "Sentiment", "Sentiment distribution", "Respondent_Group")

if "Respondent_Group" in filtered_df.columns:
    rider_only_df = filtered_df[filtered_df["Respondent_Group"] == "Rider"]
    st.subheader("Rider-only breakdown")
    st.caption("Only respondents who completed a Cruise research ride are included in this section.")
    table_cols = st.columns(2)
    with table_cols[0]:
        st.markdown("**Rider scenario mentions**")
        st.dataframe(count_table(rider_only_df, "Scenario", "Scenario"), use_container_width=True, hide_index=True)
    with table_cols[1]:
        st.markdown("**Rider sentiment distribution**")
        st.dataframe(count_table(rider_only_df, "Sentiment", "Sentiment"), use_container_width=True, hide_index=True)

st.subheader("Survey views")
survey_cols = st.columns(2)
with survey_cols[0]:
    bar_count(filtered_df, "Trip_Purpose", "Trip purpose", "Respondent_Group")
    bar_count(filtered_df, "Late_Night_Travel_Change", "Late-night travel change", "Respondent_Group")
with survey_cols[1]:
    bar_count(filtered_df, "Alternative_Mode", "Alternative mode", "Respondent_Group")
    bar_count(filtered_df, "Views_Changed", "Views changed after participation", "Respondent_Group")

mean_value_chart(filtered_df)

st.subheader("Filtered public-safe records")
st.dataframe(filtered_df, use_container_width=True)
