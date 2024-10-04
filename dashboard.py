import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the pre-calculated data from the CSV file you provided
df = pd.read_csv('cleaned_data.csv')

# Convert 'date' to datetime if not already in datetime format
df['date'] = pd.to_datetime(df['date'])

# Sidebar for navigation
st.sidebar.title('Navigation')
view = st.sidebar.selectbox('Select section', ['Main', 'Pertanyaan Bisnis'])

# Main Section
if view == 'Main':
    st.title('Main Dashboard')
    
    #header
    st.header('Tren tingkat polusi (PM2.5) di setiap stasiun sepanjang tahun 2013-2017')

    #chart1
    df.set_index('date', inplace=True)
    weekly_avg_df = df.groupby('station')['PM2.5'].resample('W').mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    for station in weekly_avg_df['station'].unique():
        station_data = weekly_avg_df[weekly_avg_df['station'] == station]
        ax.plot(station_data['date'], station_data['PM2.5'], label=station)
    
    ax.set_title('Weekly Average PM2.5 Trend by Station')
    ax.set_xlabel('Date')
    ax.set_ylabel('PM2.5 (µg/m³)')
    ax.legend(title='Station')
    
    st.pyplot(fig)

    #header2
    st.header('Peringkat stasiun dengan rata-rata polusi (PM2.5) tertinggi sepanjang tahun 2013-2017')

    # chart 2
    st.subheader('Station Ranking Based on PM2.5 Average')
    station_avg_df = df.groupby('station')['PM2.5'].mean().sort_values(ascending=False).reset_index()

    colors = ['#FF7F7F'] * len(station_avg_df)
    colors[0] = 'red'  # Bold the top station

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(station_avg_df['station'], station_avg_df['PM2.5'], color=colors)
    ax.set_xlabel('Average PM2.5 (µg/m³)')
    ax.set_title('Station Ranking Based on PM2.5 Average')

    ax.invert_yaxis()

    st.pyplot(fig)

    #penjelasan
    st.subheader('Kenapa kita berfokus pada PM2.5')
    st.write("""
    PM2.5 (bahan partikulat dengan diameter 2,5 mikrometer atau kurang) adalah salah satu polutan udara paling berbahaya 
    karena kemampuannya menembus jauh ke dalam paru-paru dan bahkan memasuki aliran darah. Pemantauan PM2.5 sangatlah penting 
    untuk memahami kualitas udara dan dampaknya terhadap kesehatan masyarakat. Oleh karena itu, fokus pada PM2.5 memberikan wawasan yang bermakna 
    mengenai tingkat keparahan polusi di berbagai wilayah.
    """)
# Pertanyaan Bisnis Section
elif view == 'Pertanyaan Bisnis':
    st.title('Pertanyaan Bisnis Section')

    # visualisasi 1
    st.subheader('Station Ranking Based on PM2.5 Average')
    station_avg_df = df.groupby('station')['PM2.5'].mean().sort_values(ascending=False).reset_index()

    colors = ['#FF7F7F'] * len(station_avg_df)
    colors[0] = 'red'  # Bold the top station

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(station_avg_df['station'], station_avg_df['PM2.5'], color=colors)
    ax.set_xlabel('Average PM2.5 (µg/m³)')
    ax.set_title('Station Ranking Based on PM2.5 Average')

    ax.invert_yaxis()
    st.pyplot(fig)

    #penjelasan pertanyaan 1
    st.subheader('Pertanyaan 1')
    st.write("""
    dapat dilihat bahwa urutan pertama stasiun dengan rata-rata tingkat polusi (PM2.5) tertinggi adalah Dongsi
    adapun yang paling rendah adalah dingling yang mana stasiun yang jauh dari Dongsi
    """)

    # visualisasi 2
    st.subheader('Rainfall vs PM2.5 Change')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='cumulative_rain', y='PM2.5_diff', data=df, scatter_kws={'s': 50}, line_kws={"color": "red"}, ax=ax)
    ax.set_title('Impact of Rainfall on PM2.5 (6hr Before vs After)')
    ax.set_xlabel('Cumulative Rain (mm)')
    ax.set_ylabel('Change in PM2.5 (6 hours after - 6 hours before)')

    st.pyplot(fig)

    # Calculate the correlation between cumulative rain and PM2.5 difference
    correlation = df[['cumulative_rain', 'PM2.5_diff']].corr().iloc[0, 1]
    st.write(f"Correlation between Cumulative Rain and Change in PM2.5: {correlation:.2f}")

    #penjelasan pertanyaan 2
    st.subheader('Pertanyaan 2')
    st.write("""
    Berdasarkan analisis scatterplot, di mana saya membandingkan tingkat PM2.5 6 jam sebelum hujan dengan
    6 jam setelah hujam, hasilnya adalah cumulative hujan tidak memiliki dampak apapun 6 jam pasca hujan,
    ini mengindikasikan bahwa hujan tidak cukup untuk membersihkan polutan PM2.5 dari udara. Terdapat
    dugaan bahwa ini disebabkan oleh ukuran partikel PM2.5 yang terlalu kecil sehingga tidak dapat 
    dibawa oleh air hujan
    """)
# Add download button for the cleaned data
st.sidebar.header('Download')
st.sidebar.download_button('Download Cleaned Data', df.to_csv(index=False), file_name='cleaned_data_v2.csv')
