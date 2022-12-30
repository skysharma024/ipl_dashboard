import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

ipl = pd.read_csv('matches (1).csv')
deliveries = pd.read_csv('deliveries (1).csv')
data = deliveries.merge(ipl, left_on='match_id', right_on='id')

st.title('IPL - Dashboard')



player = st.sidebar.selectbox('Player',sorted(data['batsman'].unique()))
search_player = st.sidebar.button('Search')



team1 = st.sidebar.selectbox('Team1',sorted(data['team1'].unique()))
st.sidebar.write('      Vs    ')
team2 = st.sidebar.selectbox('Team2',sorted(data['team1'].unique()))
stats = st.sidebar.button('Stats')




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
            col1, col2 = st.columns(2)

            with col1:


                st.write("Total Matches Played  = ", total_matches)
                st.write(team1, ' won = ', team1_won)
                st.write(team2, ' won = ', team2_won)
                st.write('Draw = ', draw)
                st.write('Player who got the most POTM **awards**  = ', Top_Player)

            with col2:
                fig3, ax3 = plt.subplots()
                ax3.pie([int(team1_won), int(team2_won)], labels=[team1, team2])
                st.pyplot(fig3)


    team1_vs_team2(team1,team2)



