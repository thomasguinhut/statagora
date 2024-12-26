import streamlit as st

conn = st.connection("statagora", type="sql")

df = conn.query("SELECT * FROM publication;", ttl="10m")

for row in df.itertuples():
    st.write(f"{row.date}")
