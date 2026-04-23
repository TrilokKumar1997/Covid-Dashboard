import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="COVID-19 Global Dashboard",
    layout="wide",
    page_icon="🌍"
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/covid_clean.csv", parse_dates=["date"])
    latest = pd.read_csv("data/latest_snapshot.csv")
    return df, latest

df, latest = load_data()

st.title("COVID-19 Global Dashboard")
st.caption("Data source: Our World in Data · github.com/owid/covid-19-data")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total cases",        f"{latest['total_cases'].sum()/1e9:.2f}B")
col2.metric("Total deaths",       f"{latest['total_deaths'].sum()/1e6:.1f}M")
col3.metric("Vaccinations given", f"{latest['total_vaccinations'].sum()/1e9:.1f}B")
col4.metric("Countries tracked",  f"{latest['location'].nunique()}")
st.divider()

st.subheader("Global case map")
metric_options = {
    "Cases per million":      "total_cases_per_million",
    "Deaths per million":     "total_deaths_per_million",
    "% Fully vaccinated":     "people_fully_vaccinated_per_hundred",
    "Case fatality rate (%)": "case_fatality_rate"
}
selected_metric = st.selectbox("Color map by", list(metric_options.keys()))
metric_col = metric_options[selected_metric]

fig_map = px.choropleth(
    latest,
    locations="location",
    locationmode="country names",
    color=metric_col,
    hover_name="location",
    color_continuous_scale="YlOrRd",
    labels={metric_col: selected_metric}
)
fig_map.update_layout(
    margin=dict(l=0, r=0, t=10, b=0),
    geo=dict(showframe=False, showcoastlines=True)
)
st.plotly_chart(fig_map, use_container_width=True)
st.divider()

st.subheader("Daily new cases — country comparison")
all_countries = sorted(df["location"].unique().tolist())
default_countries = ["United States", "India", "Brazil", "Germany", "United Kingdom"]
selected_countries = st.multiselect(
    "Select countries to compare",
    all_countries,
    default=default_countries
)

if selected_countries:
    df_sel = df[df["location"].isin(selected_countries)].copy()
    df_sel["new_cases_7d"] = (
        df_sel
        .groupby("location")["new_cases"]
        .transform(lambda x: x.rolling(7, min_periods=1).mean())
        .round(0)
    )
    fig_line = px.line(
        df_sel, x="date", y="new_cases_7d", color="location",
        labels={"new_cases_7d": "New cases (7-day avg)", "date": "Date"}
    )
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.info("Select at least one country above.")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Top 15 countries by cases")
    n = st.slider("Show top N countries", 5, 30, 15)
    top_n = latest.nlargest(n, "total_cases")
    fig_bar = px.bar(
        top_n, x="total_cases_M", y="location", orientation="h",
        color="case_fatality_rate", color_continuous_scale="Reds",
        labels={"total_cases_M": "Cases (millions)", "location": ""}
    )
    fig_bar.update_layout(yaxis=dict(autorange="reversed"),
                          margin=dict(l=0, r=0))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    st.subheader("Vaccination rate vs fatality rate")
    vax_df = latest.dropna(subset=[
        "people_fully_vaccinated_per_hundred", "case_fatality_rate"
    ])
    fig_sc = px.scatter(
        vax_df,
        x="people_fully_vaccinated_per_hundred",
        y="case_fatality_rate",
        size="population",
        color="continent",
        hover_name="location",
        size_max=50,
        labels={
            "people_fully_vaccinated_per_hundred": "% vaccinated",
            "case_fatality_rate": "Fatality rate (%)"
        }
    )
    st.plotly_chart(fig_sc, use_container_width=True)

st.divider()
st.caption("Built by Your Name · Data Science MS, University of New Haven")
