import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

PATH = 'Overbuff_scraped_24-05-2020.csv'

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("Overwatch hero statistics 2020")
st.write("""
## From Overbuff
sources: [Overwatch hero statistics](https://www.kaggle.com/jamesryanralph/overwatch-hero-stats?select=Overbuff_scraped_24-05-2020.csv)
""")
st.image("OW_heroes.png")

df = pd.read_csv(PATH, encoding='latin1')
df = df.drop(["Unnamed: 0"], axis=1)
df = df.replace({"LÃºcio":"Lucio", "TorbjÃ¶rn":"Torbjörn"})
df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d %H:%M:%S')
df['Rank'].astype('category')
df['Rank'] = pd.Categorical(df['Rank'], categories=['Grandmaster', 'Master', 'Diamond', 'Platinum', 'Gold', 'Silver', 'Bronze', 'All'], 
                           ordered=True)

st.sidebar.header("Filter")
selected_rank = st.sidebar.multiselect("Rank", sorted(list(df.Rank.unique())), sorted(list(df.Rank.unique())))
selected_role = st.sidebar.multiselect("Role", sorted(list(df.Role.unique())), sorted(list(df.Role.unique())))
# selected_hero = st.sidebar.multiselect("Hero", sorted(list(df.Hero.unique())), sorted(list(df.Hero.unique())))

# @st.cache
# def filter_data(rank, role, hero, data): 
#     data = data[(data.Rank.isin(rank)) & (data.Role.isin(role)) & (data.Hero.isin(hero))]
#     return data

# df = filter_data(selected_rank, selected_role, selected_hero, df)

@st.cache
def filter_data(rank, role, data): 
    data = data[(data.Rank.isin(rank)) & (data.Role.isin(role))]
    return data

df = filter_data(selected_rank, selected_role, df)

st.write("The data has " + str(df.shape[0]) + " rows and " + str(df.shape[1]) + " columns.")
st.write(df.astype('object'))

if st.button("Hero Analysis"): 
    st.write("## Pick rate in each heroes.")
    hero = df.set_index(['Hero', 'Role']).sort_index()
    hero = hero.groupby('Hero').mean().sort_values('Pick_rate', ascending=False)
    ax = hero['Pick_rate'].plot(kind='barh', figsize=(9,9))
    ax.axvline(df.Pick_rate.mean(), color='orange', linestyle='--')
    st.pyplot()

    st.write("## Win rate in each heroes.")
    hero = df.set_index(['Hero', 'Role']).sort_index()
    hero = hero.groupby('Hero').mean().sort_values('Win_rate', ascending=False)
    ax = hero['Win_rate'].plot(kind='barh', figsize=(9,9))
    ax.axvline(50, color='orange', linestyle='--')
    st.pyplot()

if st.button("Rank Analysis"): 
    sns.lineplot(x='Date', y='Win_rate', data=df, ci=False, hue='Rank')
    plt.legend()
    st.pyplot()

    plt.figure(figsize=(6,4))
    ax = sns.scatterplot(x='On_fire', y='Win_rate', data=df, hue='Rank')
    ax.axhline(df.Win_rate.mean(), linestyle='--', color='orange')
    st.pyplot()

    g = sns.FacetGrid(df, col='Rank', hue='Role', col_wrap=3)
    g.map(sns.scatterplot, 'On_fire', 'Win_rate')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    st.pyplot(g)
