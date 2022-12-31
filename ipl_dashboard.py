import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

ipl = pd.read_csv('matches (1).csv')
deliveries = pd.read_csv('deliveries (1).csv')
data = deliveries.merge(ipl, left_on='match_id', right_on='id')
st.set_page_config(layout='wide')

st.header('IPL - Dashboard')


# Batsman
player = st.sidebar.selectbox('Batsman',sorted(data['batsman'].unique()))
search_player = st.sidebar.button('Search_Batsman')


bowler = st.sidebar.selectbox('Bowler',sorted(data['bowler'].unique()))
search_bowler = st.sidebar.button('Search_Bowler')


# team vs team
team1 = st.sidebar.selectbox('Team1',sorted(data['team1'].unique()))
st.sidebar.write('      Vs    ')
team2 = st.sidebar.selectbox('Team2',sorted(data['team1'].unique()))
stats = st.sidebar.button('Stats')



purple = st.sidebar.button('Purple Cap Holders')
Orange = st.sidebar.button('Orange Cap Holders')
TopBatsman = st.sidebar.button("Highest Runs Getter in IPL")
TopBowler = st.sidebar.button("Highest Wicket Taker in IPL")


if search_player:
    st.header(player)
    col1,col2 = st.columns(2)

    with col1:
        st.image('MS Dhoni.jpg', width=200)
    with col2:

        def player_data(player):
            ipl = pd.read_csv('matches (1).csv')
            deliveries = pd.read_csv('deliveries (1).csv')
            data = deliveries.merge(ipl, left_on='match_id', right_on='id')

            season_runs = data[data['batsman'] == player].groupby(['season', 'batsman'])[
                'batsman_runs'].sum().reset_index()
            total_runs = data[data['batsman'] == player]['batsman_runs'].sum()
            dismissed = data[data['player_dismissed'] == player].shape[0]
            avg = round(total_runs / dismissed, 2)
            highest_runs = data[data['batsman'] == player].groupby(['match_id', 'batsman'])['batsman_runs'].sum().max()
            balls = data[(data['batsman'] == player) & (data['wide_runs'] == 0)].shape[0]
            strike_rate = round((total_runs / balls) * 100, 2)
            return season_runs, total_runs, avg, highest_runs, strike_rate



        t = player_data(player)

        st.metric('Total Runs ' , t[1])
        st.metric('Average  ', t[2])
        st.metric('Highest Runs  ', t[3])
        st.metric('Strike Rate ', t[4])


    col1, col2 = st.columns(2)


    with col1:
        st.dataframe(t[0])

    with col2:

        fig3 , ax3 = plt.subplots()
        ax3.bar(t[0]['season'],t[0]['batsman_runs'])
        st.pyplot(fig3)


if stats:
    def team1_vs_team2(team1,team2):
        if team1 == team2:
            st.subheader("choose 2 different teams")
        else:
            row1 = ipl[(ipl['team1'] == team1) & (ipl['team2'] == team2)]
            row2 = ipl[(ipl['team1'] == team2) & (ipl['team2'] == team1)]
            row1 = row1.append(row2)
            total_matches = row1.shape[0]
            team1_won = row1[row1['winner'] == team1].shape[0]
            team2_won = row1[row1['winner'] == team2].shape[0]
            draw = total_matches - (team1_won + team2_won)
            Top_Player = row1['player_of_match'].value_counts().index[0]

            st.subheader(team1 + "   vs   " + team2)
            st.write("##")
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                st.image(team1+'.jpg')  #Chennai Super Kings.jpg
            with col2:
                st.subheader('Head to Head')
            with col3:
                st.image(team2+'.jpg')
            with col4:
                st.write()

            st.write("##")
            col1,col2 = st.columns(2)
            with col1:


                st.write(":blue[Total Matches Played]  = ", total_matches)
                st.write(team1, ':blue[won] = ', team1_won)
                st.write(team2, ':blue[won] = ', team2_won)
                st.write(':blue[Draw] = ', draw)
                st.write(':blue[Most POTM awards ] = ', Top_Player)

            with col2:
                fig3, ax3 = plt.subplots()
                ax3.pie([int(team1_won), int(team2_won)], labels=[team1, team2])
                st.pyplot(fig3)


    team1_vs_team2(team1,team2)



if purple:
    df = data[(~data['player_dismissed'].isnull()) & (data['dismissal_kind'] != 'run out')].groupby('season')['bowler'].value_counts().reset_index(name='count')
    season = pd.Series(df['season'].unique())

    l = []
    def purple_cap(year):
        l.append([df[df['season'] == year].head(1).values[0][0],df[df['season'] == year].head(1).values[0][1],df[df['season'] == year].head(1).values[0][2]])


    season.apply(purple_cap)
    w=pd.DataFrame(l,columns=['Year','Player','Wickets'])
    st.dataframe(w)

if Orange:
    s = data.groupby(['season', 'batsman'])['batsman_runs'].sum().reset_index().sort_values('batsman_runs',
                                                                                           ascending=False).drop_duplicates(subset=['season'], keep='first').sort_values('season')
    st.dataframe(s)

if TopBatsman:
    st.dataframe(data.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index())

if TopBowler:
    st.dataframe(data[(~data['player_dismissed'].isnull()) & (data['dismissal_kind'] != 'run out')]['bowler'].value_counts().head(10).reset_index(name='count'))

if search_bowler:
    st.header(bowler)
    col1,col2 = st.columns(2)
    with st.container():
        with col1:
            st.image('MS Dhoni.jpg', width=200)
        with col2:

            def bowler_data(bowler):
                ipl = pd.read_csv('matches (1).csv')
                deliveries = pd.read_csv('deliveries (1).csv')
                data = deliveries.merge(ipl, left_on='match_id', right_on='id')

                bowls = data[data['bowler'] == bowler]
                runs_conceded = bowls['batsman_runs'].sum()
                wickets = bowls[(~bowls['player_dismissed'].isnull()) & (bowls['dismissal_kind'] != 'run out')]
                avg = runs_conceded / wickets.shape[0]
                strike_rate = bowls.shape[0] / wickets.shape[0]
                season = wickets.groupby(['season', 'bowler'])['bowler'].count().reset_index(name='count')
                return season,wickets.shape[0],avg,strike_rate


            t = bowler_data(bowler)

            st.metric('Wickets ' , t[1])
            st.metric('Average  ', round(t[2],2))
            st.metric('Strike_rate  ', t[3])

    with st.container():
        st.write('##')
        col1, col2 = st.columns(2)


        with col1:
            st.dataframe(t[0])

        with col2:

            fig3 , ax3 = plt.subplots()
            ax3.bar(t[0]['season'],t[0]['count'])
            st.pyplot(fig3)
