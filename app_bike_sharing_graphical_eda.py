import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

st.title("""Проанализируем набор данных, содержащий почасовое и ежедневное количество взятых напрокат велосипедов с 2011 по 2012 год с соответствующей информацией о погоде и сезонности.""")

df = pd.read_csv("bike_sharing.csv")
df = df.rename(columns={'count': 'total'})

st.dataframe(df)

st.header("""Построим гистограмы числовых переменных и проанализируем их распределение""")


def subhist(x, label=None, col=None):
    plt.hist(x, color=col)
    plt.xlabel(label)


fig = plt.figure(figsize=(10, 25))
plt.subplot(4, 2, 1)
subhist(df.season, 'season', '#cccccc')
plt.subplot(4, 2, 2)
subhist(df.holiday, 'holiday', '#cccccc')
plt.subplot(4, 2, 3)
subhist(df.workingday, 'workingday', '#cccccc')
plt.subplot(4, 2, 4)
subhist(df.weather, 'weather', '#cccccc')
plt.subplot(4, 2, 5)
sns.histplot(df.temp, kde=True, alpha=.4)
plt.subplot(4, 2, 6)
sns.histplot(df.atemp, kde=True, alpha=.4)
plt.subplot(4, 2, 7)
sns.histplot(df.humidity, kde=True, alpha=.4)
plt.subplot(4, 2, 8)
sns.histplot(df.windspeed, kde=True, alpha=.4)
st.pyplot(fig)

fig = plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
subhist(df.registered, 'registered', '#cccccc')
plt.subplot(1, 3, 2)
subhist(df.casual, 'casual', '#cccccc')
plt.subplot(1, 3, 3)
subhist(df.total, 'total', '#cccccc')
st.pyplot(fig)

st.header("""Посмотрим на некоторые характеристики и зависимости""")

st.markdown("""Узнаем почасовую тенденцию, в какое время более высокий спрос""")

hour = [int(d[11:13]) for d in df.datetime]
hour_data = df[['total', 'casual', 'registered']]
hour_data.insert(1, 'hour', hour)
total_mean = hour_data.groupby('hour')['total'].agg("mean")

fig = go.Figure()
fig.add_trace(go.Scatter(x=hour, y=df.total, mode='markers', name='mean value'))
fig.add_trace(go.Scatter(x=total_mean.index, y=total_mean.values, mode='lines', name='count of users'))
st.plotly_chart(fig)

st.markdown("""Видим тренд на каждый час и сразу выделяем три категории:

1. Самый высокий пик приходится на: 7-9 и 17-19 часов
2. Средний на: 10-16 часов
3. Низкий на: 0-6 и 20-24 часов

Давайте посмотрим на распределение зарегистрированных и случайных пользователей отдельно.
""")

registered_mean = hour_data.groupby('hour')['registered'].agg("mean")

fig = go.Figure()
fig.add_trace(go.Scatter(x=hour, y=df.total, mode='markers', name='mean value'))
fig.add_trace(go.Scatter(x=registered_mean.index, y=registered_mean.values, mode='lines',
                         name='count registered of users'))
st.plotly_chart(fig)

casual_mean = hour_data.groupby('hour')['casual'].agg("mean")

fig = go.Figure()
fig.add_trace(go.Scatter(x=hour, y=df.total, mode='markers', name='mean value'))
fig.add_trace(go.Scatter(x=casual_mean.index, y=casual_mean.values, mode='lines',
                         name='count casual of users'))
st.plotly_chart(fig)

fig = plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
sns.boxplot(x=hour, y=df.registered)
plt.xlabel("hour")
plt.subplot(1, 2, 2)
sns.boxplot(x=hour, y=df.casual)
plt.xlabel("hour")
st.pyplot(fig)

st.markdown("""Можно видеть, что registered users имеют ту же тенденцию, как и total users. 
А вот casual users и total users имеют разные тенденции. 
Таким образом, мы можем сказать, что hour является значимой переменной.

Высокий спрос происходит в рабочие моменты времени. Рано утром и поздно вечером может иметь разную тенденцию и 
низкий спрос в течение 10:00 вечера до 6:00 утра.

Теперь взглянем на еженедельную тенденцию:
""")

date = [datetime.strptime(d[0:10], "%Y-%m-%d") for d in df.datetime]
week = [d.isoweekday() for d in date]

fig = plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
sns.boxplot(x=week, y=df.registered)
plt.xlabel("week")
plt.subplot(1, 2, 2)
sns.boxplot(x=week, y=df.casual)
plt.xlabel("week")
st.pyplot(fig)

st.markdown("""registered users испоьзуют велосипеды немного больше в рабочие дни по сравнению с выходными
или праздникам, спрос же casual users увеличивается в выходные

Очевидно, в более плохую погоду спрос падает:
""")

fig = plt.figure(figsize=(10, 5))
sns.boxplot(x=df.weather, y=df.total)
plt.ylabel("Count of users")
st.pyplot(fig)

st.markdown("""Интересно также взглянуть, как изменяется температура и количество велосипедистов за сезон:""")

fig = plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
sns.boxplot(x=df.season, y=df.atemp)
plt.ylabel("Averange temperature")
plt.subplot(1, 2, 2)
sns.boxplot(x=df.season, y=df.total)
plt.ylabel("Count of users")
st.pyplot(fig)

st.markdown("""Что еще раз намекает на то, что велосипеды предпочитают в хорошую погоду

Посмотрим тенденцию спроса на велосипеды в течение года
""")

year = [d.year for d in date]
fig = plt.figure(figsize=(10, 5))
sns.boxplot(x=year, y=df.total)
plt.ylabel("Count of users")
st.pyplot(fig)

st.markdown("""По сравнению с 2011 в 2012 спрос увеличился""")

fig = plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
sns.boxplot(x=year, y=df.registered)
plt.ylabel("Count of registered users")
plt.subplot(1, 2, 2)
sns.boxplot(x=year, y=df.casual)
plt.ylabel("Count of casual users")
st.pyplot(fig)

st.markdown("""registered users внесли более высокий вклад в общий объем спроса по сравнению с casual users.
Это происходит потому, что зарегистрированная база пользователей будет увеличиваться с течением времени.
""")