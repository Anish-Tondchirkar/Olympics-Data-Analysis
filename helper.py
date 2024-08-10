# Function for year and country wise medal tally
def get_medal_tally(df, yr, country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Year','Games','City','Sport','Event','Medal'])
    ok = 0
    if yr == "Overall" and country == "Overall":
        temp_df = medal_df
    if yr == "Overall" and country != "Overall":
        ok = 1
        temp_df = medal_df[medal_df["region"] == country]
    if yr != "Overall" and country == "Overall":
        temp_df = medal_df[medal_df["Year"] == int(yr)]
    if yr != "Overall" and country != "Overall":
        temp_df = medal_df[(medal_df["Year"] == yr) & (medal_df["region"] == country)]

    if ok == 1:
        res = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values(by='Year',ascending=True).reset_index()
    else:
        res = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values(by='Gold',ascending=False).reset_index()
    # uint 64
    res['Gold'] = res['Gold'].astype('uint64')
    res['Silver'] = res['Silver'].astype('uint64')
    res['Bronze'] = res['Bronze'].astype('uint64')
    res['Total'] = res['Gold'] + res['Silver'] + res['Bronze']
    # Add rank column starting from 1
    res.reset_index(drop=True, inplace=True)
    res.index += 1  # Adjust index to start from 1
    res.index.name = 'Rank'
    return res


def medals_summ(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False)
    medal_tally = medal_tally.reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def country_year(df):
    yr = df["Year"].unique().tolist()
    yr.sort()
    yr.insert(0, "Overall")

    country = df["region"].dropna().unique().tolist()
    country.sort()
    country.insert(0, "Overall")

    return yr, country

def participating_nations(df):
    ok = df.drop_duplicates(['Year', 'region'])
    ok = ok['Year'].value_counts().reset_index()
    ok.rename(columns={'index': 'Edition', 'Year': 'Countries'}, inplace=True)
    nations_vs_time = ok.sort_values('Edition')
    nations_vs_time = nations_vs_time.drop(nations_vs_time[nations_vs_time['Edition'] == 1906].index)

    return nations_vs_time

def sport_time(df):
    spo = df.drop_duplicates(['Year', 'Sport'])
    spo = spo['Year'].value_counts().reset_index()
    spo.rename(columns={'index': 'Edition', 'Year': 'Sport'}, inplace=True)
    sports_vs_time = spo.sort_values('Edition')
    sports_vs_time = sports_vs_time.drop(sports_vs_time[sports_vs_time['Edition'] == 1906].index)

    return sports_vs_time

def eve_time(df):
    eve = df.drop_duplicates(['Year', 'Event'])
    eve = eve['Year'].value_counts().reset_index()
    eve.rename(columns={'index': 'Edition', 'Year': 'Event'}, inplace=True)
    eve_vs_time = eve.sort_values('Edition')
    eve_vs_time = eve_vs_time.drop(eve_vs_time[eve_vs_time['Edition'] == 1906].index)

    return eve_vs_time

def ath_time(df):
    ath = df.drop_duplicates(['Year', 'Name'])
    ath = ath['Year'].value_counts().reset_index()
    ath.rename(columns={'index': 'Edition', 'Year': 'Athlete'}, inplace=True)
    ath_vs_time = ath.sort_values('Edition')
    ath_vs_time = ath_vs_time.drop(ath_vs_time[ath_vs_time['Edition'] == 1906].index)

    return ath_vs_time


# Most successfull in each sport
def most_succ(df,sport):
    tmp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        tmp_df = tmp_df[tmp_df['Sport'] == sport]
    ok = tmp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    ok.rename(columns={'index':'Name','Name_x':'Medal Count','region':'Country'},inplace=True)
    ok_sorted = ok.sort_values(by=['Medal Count', 'Country'], ascending=[False, True])

    # Add rank column starting from 1
    ok_sorted.reset_index(drop=True, inplace=True)
    ok_sorted.index += 1  # Adjust index to start from 1
    ok_sorted.index.name = 'Rank'

    return ok_sorted

def men_vs_women(df):
    athlete_mf = df.drop_duplicates(['Name', 'region'])
    men = athlete_mf[athlete_mf['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_mf[athlete_mf['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    men_and_women = men.merge(women, on='Year', how='left')
    men_and_women.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'}, inplace=True)

    men_and_women.fillna(0, inplace=True)

    return men_and_women

def medal_year(df,country):
    tmp = df.dropna(subset='Medal')
    tmp.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_tmp = tmp[tmp['region'] == country]
    new_tmp = new_tmp.groupby('Year').count()['Medal'].reset_index()

    return new_tmp

def heat_map(df,country):
    tmp = df.dropna(subset='Medal')
    tmp.drop_duplicates(subset=['Team', 'NOC', 'Year', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_tmp = tmp[tmp['region'] == country]
    pt = new_tmp.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt

def most_succ_ath(df,country):
    tmp_df = df.dropna(subset=['Medal'])
    tmp_df = tmp_df[tmp_df['region'] == country]
    ok = tmp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')
    ok.rename(columns={'index':'Name','Name_x':'Medal Count','region':'Country'},inplace=True)
    # Add rank column starting from 1
    ok.reset_index(drop=True, inplace=True)
    ok.index += 1  # Adjust index to start from 1
    ok.index.name = 'Rank'
    return ok
