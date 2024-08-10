import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as pe
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

df_sum = pd.read_csv('Athletes_summer_games.csv')
df_win = pd.read_csv('Athletes_winter_games.csv')
region_df = pd.read_csv('regions.csv')

df_s = preprocessor.preprocess(df_sum, region_df)
df_w = preprocessor.preprocess(df_win, region_df)
st.sidebar.title("Olympics Analysis")
olympic_type = st.sidebar.selectbox("Select Olympics Type", ["Summer", "Winter"])

# Load the appropriate dataframe
if olympic_type == "Summer":
    df_summer = df_s

else:
    df_summer = df_w

# Sidebar options
user_menu = st.sidebar.radio(
    'Select',
    ('Medal Tally', 'Overall Olympics Analysis', 'Country-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    yr, country = helper.country_year(df_summer)
    sel_yr = st.sidebar.selectbox("Select year", yr)
    sel_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.get_medal_tally(df_summer, sel_yr, sel_country)

    # Header for medal tally India's 2008 Summer Olympics Medal Tally
    if sel_yr == "Overall" and sel_country == "Overall":
        st.header(f"{olympic_type} Olympics Overall Medal Tally")
    if sel_yr == "Overall" and sel_country != "Overall":
        st.header(f"{sel_country}'s {olympic_type} Olympics Medal Tally")
    if sel_yr != "Overall" and sel_country == "Overall":
        st.header(f"{sel_yr} {olympic_type} Olympics Medal Count")
    if sel_yr != "Overall" and sel_country != "Overall":
        st.header(f"{sel_country}'s {sel_yr} {olympic_type} Olympics Medal Tally")

    st.table(medal_tally)

elif user_menu == 'Overall Olympics Analysis':
    st.header("Top Stats")
    editions = df_summer['Year'].unique().shape[0] - 1
    hosts = df_summer['City'].unique().shape[0]
    sports = df_summer['Sport'].unique().shape[0]
    events = df_summer['Event'].unique().shape[0]
    ath = df_summer['Name'].unique().shape[0]
    cntry = df_summer['region'].unique().shape[0]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.header("Editions")
        st.title(editions)

    with c2:
        st.header("Host")
        st.title(hosts)

    with c3:
        st.header("Sports")
        st.title(sports)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.header("Events")
        st.title(events)

    with c5:
        st.header("Athletes")
        st.title(ath)

    with c6:
        st.header("Country")
        st.title(cntry)

    nations_vs_time = helper.participating_nations(df_summer)
    fig = pe.line(nations_vs_time, x="Edition", y="Countries")
    st.header("Participating Nations Over Year")
    st.plotly_chart(fig)

    sports_vs_time = helper.sport_time(df_summer)
    fig2 = pe.line(sports_vs_time, x="Edition", y="Sport")
    st.header("No. of Sports over Time")
    st.plotly_chart(fig2)

    eve_vs_time = helper.eve_time(df_summer)
    fig3 = pe.line(eve_vs_time, x="Edition", y="Event")
    st.header("No. of Events over Time")
    st.plotly_chart(fig3)

    ath_vs_time = helper.ath_time(df_summer)
    fig4 = pe.line(ath_vs_time, x="Edition", y="Athlete")
    st.header("No. of Athletes over Time")
    st.plotly_chart(fig4)

    men_and_women = helper.men_vs_women(df_summer)
    lin2 = pe.line(men_and_women, x='Year', y=['Men', 'Women'])
    st.header("Men vs Women participation over the years")
    st.plotly_chart(lin2)

    st.header('Most Successfull Athlete')
    sport_list = df_summer['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    sel_sport = st.selectbox('Select a Sport', sport_list)
    ok = helper.most_succ(df_summer, sel_sport)
    st.table(ok)


elif user_menu == 'Country-wise Analysis':
    st.sidebar.header("Country-wise Analysis")
    country_list = df_summer['region'].dropna().unique().tolist()
    country_list.sort()
    sel_cnt = st.sidebar.selectbox('Select a country', country_list)

    new_tmp = helper.medal_year(df_summer, sel_cnt)
    fig6 = pe.line(new_tmp, x="Year", y="Medal")
    st.header(sel_cnt + ' Medal over years')
    st.plotly_chart(fig6)

    st.header(sel_cnt + ' Medal Tally over years')
    pt = helper.heat_map(df_summer, sel_cnt)
    if pt.empty:
        st.write("No data available for the selected criteria.")
    else:
        plt.figure(figsize=(12, 12))
        fig7 = sns.heatmap(pt, annot=True, cmap='Greens')
        figg = fig7.get_figure()  # Get the current figure
        st.pyplot(figg)

    st.header('Top 15 Athletes of ' + sel_cnt)
    top15 = helper.most_succ_ath(df_summer, sel_cnt)
    st.table(top15)

# if __name__ == "__main__":
#     main()
