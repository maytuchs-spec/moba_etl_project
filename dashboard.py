import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="MOBA Dashboard", layout="wide")
st.title("🎮 MOBA Esports Analytics Dashboard")

# 1. โหลดข้อมูลจาก SQLite ที่เราทำ ETL ไว้
@st.cache_data
def load_data():
    # ดึงข้อมูลจากไฟล์ Database ของเรา
    conn = sqlite3.connect('data/processed/moba_database.db')
    df = pd.read_sql_query("SELECT * FROM match_statistics", conn)
    return df

df = load_data()

# 2. แบ่งคอลัมน์โชว์ตัวเลขสรุปด้านบน
col1, col2, col3 = st.columns(3)
col1.metric("จำนวนฮีโร่ที่ถูกเลือกเล่น", len(df))
col2.metric("KDA สูงสุด", df['kda'].max())
col3.metric("KDA เฉลี่ยรวม", round(df['kda'].mean(), 2))

st.divider()

# 3. สร้างกราฟ
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("⚔️ ประสิทธิภาพฮีโร่ (KDA)")
    # กราฟแท่งเปรียบเทียบ KDA ของแต่ละฮีโร่
    fig1 = px.bar(df, x='hero_name', y='kda', color='hero_name', text='kda')
    st.plotly_chart(fig1, use_container_width=True)

with col_chart2:
    st.subheader("🏆 สัดส่วนแพ้/ชนะ (Win/Loss)")
    # กราฟโดนัท (Pie Chart) นับจำนวนครั้งที่ชนะและแพ้
    win_counts = df['win'].value_counts().reset_index()
    win_counts.columns = ['Status', 'Count']
    win_counts['Status'] = win_counts['Status'].replace({1: 'Win', 0: 'Loss'})
    
    fig2 = px.pie(win_counts, values='Count', names='Status', hole=0.4, 
                  color='Status', color_discrete_map={'Win':'#00CC96', 'Loss':'#EF553B'})
    st.plotly_chart(fig2, use_container_width=True)

# 4. โชว์ตารางข้อมูลดิบเผื่อเจาะลึก
st.subheader("📋 ตารางข้อมูลหลังทำ ETL")
st.dataframe(df, use_container_width=True)
# เพิ่มต่อท้ายไฟล์ dashboard.py
st.divider()
st.subheader("🎯 Top Killers (ใครโหดสุดในแมตช์)")
fig3 = px.scatter(df, x='hero_name', y='kills', size='kills', color='hero_name', 
                 hover_data=['assists', 'deaths'])
st.plotly_chart(fig3, use_container_width=True)