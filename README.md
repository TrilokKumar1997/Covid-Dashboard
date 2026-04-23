# COVID-19 Global Dashboard

An interactive dashboard analyzing COVID-19 trends across 200+ countries,
built with Python and Streamlit using the Our World in Data dataset.

## Features
- Global choropleth map filterable by cases, deaths and vaccination rate
- 7-day rolling average trend lines for any country combination
- Top 15 countries ranked by total case burden
- Vaccination rate vs case fatality rate scatter plot
- KPI summary cards showing global totals

## Tech stack
- Python
- pandas
- Plotly
- Streamlit

## Data source
Our World in Data — https://github.com/owid/covid-19-data

## How to run locally
git clone https://github.com/TrilokKumar1997/Covid-Dashboard.git
cd Covid-Dashboard
pip install -r requirements.txt
python download_data.py
streamlit run app.py

## Author
Trilok Kumar — Data Science MS, University of New Haven
