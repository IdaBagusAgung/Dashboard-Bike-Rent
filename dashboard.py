# Mengimport library yang digunakan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from io import BytesIO
import random

# Set style seaborn
sns.set(style='whitegrid')

# Menyiapkan data day
day = pd.read_csv("day.csv")
day.head()

# Menghapus kolom yang tidak diperlukan
drop_col = ['instant']

# Mengubah nama kolom
day.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'hum' : 'humidity',
    'weathersit': 'weather_condition',
    'cnt': 'count'
}, inplace=True)

# Perubahan data pada kolom month sesuai informasi pada dataset :  1:Jan, 2:Feb, 3:Mar, 4:Apr, 5:May, 6:Jun, 7:Jul, 8:Aug, 9:Sep, 10:Oct, 11:Nov, 12:Dec
day.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)

# Perubahan data pada kolom season sesuai informasi pada dataset : 1:Winter, 2:Spring, 3:Summer, 4:Fall
day.season.replace((1,2,3,4), ('Winter','Spring','Summer','Fall'), inplace=True)

# Perubahan data pada kolom weekday sesuai informasi pada dataset : 0:Sun, 1:Mon, 2:Tue, 3:Wed, 4:Thu, 5:Fri, 6:Sat
day.weekday.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)

# Perubahan data pada kolom weather_condition sesuai informasi pada dataset : 1:Clear, 2:Misty, 3:Light_RainSnow 4:Heavy_RainSnow
day.weather_condition.replace((1,2,3,4), ('Clear','Misty','Light_RainSnow','Heavy_RainSnow'), inplace=True)

# Perubahan data pada kolom year sesuai informasi pada dataset : 0:2011, 1:2012
day.year.replace((0,1), (2011,2012), inplace=True)

# Menyiapkan Helper Function
# Menyiapkan Helper Function daily_orders_df
def create_daily_orders_df(df):
    daily_orders_df = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_orders_df

# Menyiapkan Helper Function daily_casual_orders_df
def create_daily_casual_orders_df(df):
    daily_casual_orders_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_orders_df

# Menyiapkan Helper Function daily_registered_orders_df
def create_daily_registered_orders_df(df):
    daily_registered_orders_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_orders_df
    
# Menyiapkan Helper Function season_orders_df
def create_season_orders_df(df):
    season_orders_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_orders_df

# Menyiapkan Helper Function month_orders_df
def create_month_orders_df(df):
    month_orders_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    month_orders_df = month_orders_df.reindex(ordered_months, fill_value=0)
    return month_orders_df

# Menyiapkan Helper Function weekday_orders_df
def create_weekday_orders_df(df):
    weekday_orders_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_orders_df

# Menyiapkan Helper Function workingday_orders_df
def create_workingday_orders_df(df):
    workingday_orders_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_orders_df

# Menyiapkan Helper Function holiday_orders_df
def create_holiday_orders_df(df):
    holiday_orders_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_orders_df

# Menyiapkan Helper Function weather_orders_df
def create_weather_orders_df(df):
    weather_orders_df = df.groupby(by='weather_condition').agg({
        'count': 'sum'
    })
    return weather_orders_df


# Membuat filter data
min_date = pd.to_datetime(day['date']).dt.date.min()
max_date = pd.to_datetime(day['date']).dt.date.max()
 
with st.sidebar:
    #Menambahkan logo bike rent dicoding
    st.image('logo.png')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value= min_date, max_value= max_date, value=[min_date, max_date]
    )

main_df = day[(day['date'] >= str(start_date)) & 
                (day['date'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)
daily_casual_orders_df = create_daily_casual_orders_df(main_df)
daily_registered_orders_df = create_daily_registered_orders_df(main_df)
season_orders_df = create_season_orders_df(main_df)
month_orders_df = create_month_orders_df(main_df)
weekday_orders_df = create_weekday_orders_df(main_df)
workingday_orders_df = create_workingday_orders_df(main_df)
holiday_orders_df = create_holiday_orders_df(main_df)
weather_orders_df = create_weather_orders_df(main_df)


# Membuat tampilan dashboard
# Memberikan judul dashboard
st.header('Agung Bike Rent Dashboard :sparkles:')

# Membuat jumlah penyewaan harian
st.subheader('Daily Renting')
col1, col2, col3 = st.columns(3)

# Menampilkan total user pada kolom 1
with col1:
    daily_orders_total = daily_orders_df['count'].sum()
    st.metric('Total User', value= daily_orders_total)

# Menampilkan registered user pada kolom 2
with col2:
    daily_orders_registered = daily_registered_orders_df['registered'].sum()
    st.metric('Registered User', value= daily_orders_registered)

# Menampilkan casual user pada kolom 3
with col3:
    daily_orders_casual = daily_casual_orders_df['casual'].sum()
    st.metric('Casual User', value= daily_orders_casual)

# Membuat jumlah penyewaan bulanan
st.subheader('Penyewaan Sepeda Bulanan')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_orders_df.index,
    month_orders_df['count'],
    marker='o', 
    linewidth=2,
    color='red'
)
for index, row in enumerate(month_orders_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=15)

# Menampilkan grafik penyewaan bulanan
st.pyplot(fig)


# Membuat grafik jumlah penyewaan berdasarkan season
st.subheader('Total Penyewaan Sepeda Berdasarkan Musim/Season')

plt.figure(figsize=(10,6))

# Mendefinisikan warna yang ingin digunakan untuk setiap tahunnya
colors = ["#FFD700", "#006400"]

sns.barplot(x='season', y='count', data=day, hue='year', palette=colors, ci=None)

plt.xlabel("Season")
plt.ylabel("Total Penyewa")
plt.title("Total penyewaan sepeda berdasarkan season")

# Menampilkan grafik jumlah penyewaan berdasarkan season
st.pyplot(plt) 


# Membuah grafik jumlah penyewaan berdasarkan bulan dan tahun
st.subheader('Jumlah total penyewaan sepeda berdasarkan bulan dan tahun')

# Dataframe monthly_counts
monthly_counts = day.groupby(by=["month", "year"]).agg({
    "count": "sum"
}).reset_index()

# Memfilter DataFrame untuk tahun 2011
monthly_counts_2011 = monthly_counts[monthly_counts['year'] == 2011]

# Memfilter DataFrame untuk tahun 2012
monthly_counts_2012 = monthly_counts[monthly_counts['year'] == 2012]

# Membuat plot menggunakan seaborn dan atur warna garis untuk masing-masing tahun
fig, ax = plt.subplots()
sns.lineplot(
    data=monthly_counts_2011,
    x="month",
    y="count",
    color='red',  # Warna merah
    marker="o",
    label='Tahun 2011',
    ax=ax
)

sns.lineplot(
    data=monthly_counts_2012,
    x="month",
    y="count",
    color='green',  # Warna hijau
    marker="o",
    label='Tahun 2012',
    ax=ax
)

plt.title("Jumlah total sepeda yang disewakan berdasarkan Bulan dan tahun")
plt.xlabel(None)
plt.ylabel(None)

# Tampilan legenda/informasi tentang line chart
plt.legend(title="Tahun", loc="upper left", fontsize='x-small', bbox_to_anchor=(1, 1))
plt.tight_layout()

# Menampilkan grafik jumlah penyewaan berdasarkan bulan dan tahun
st.pyplot(fig)


# Membuat grafik jumlah penyewaan berdasarkan hari
st.subheader('Jumlah penyewaan sepeda berdasarkan hari')

# Mendefinisikan warna untuk plot
colors=["tab:pink", "tab:red", "tab:brown", "tab:purple", "tab:blue", "tab:green", "tab:orange"]

# Mengacak urutan warna
random.shuffle(colors)

# Grafik berdasarkan weekday
plt.figure(figsize=(10, 6))
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_orders_df,
    palette=colors
)

# Menambahkan label pada bar
for index, row in enumerate(weekday_orders_df['count']):
    plt.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

plt.title('Jumlah penyewaan sepeda berdasarkan hari')
plt.ylabel(None)
plt.xlabel(None)
plt.xticks(fontsize=15)
plt.yticks(fontsize=10)

plt.tight_layout()

# Simpan plot sebagai BytesIO object
buffer = BytesIO()
plt.savefig(buffer, format='png')
plt.close()

# Tampilkan gambar menggunakan st.image()
buffer.seek(0)
st.image(buffer, use_column_width=True)

# Memberikan caption copyright
st.caption('Copyright (c) Ida Bagus Agung Bajerapany')