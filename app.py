import streamlit as st
import pandas as pd
import datetime
from openai import OpenAI

client = OpenAI()

st.sidebar.title("Elder Health Profile")
name = st.sidebar.text_input("Name")
age = st.sidebar.number_input("Age", min_value=50, max_value=120)
gender = st.sidebar.radio("Gender", ["Male", "Female", "Other"])
st.sidebar.markdown("---")

st.title("Elder Health Management Dashboard")

tab1, tab2, tab3, tab4 = st.tabs([
    "Daily Vitals", "Health Trends", "Medication Reminders", "Smart Health Assistant"
])

with tab1:
    st.subheader("Record Today's Vitals")
    date = st.date_input("Date", datetime.date.today())
    bp = st.text_input("Blood Pressure (e.g. 120/80)")
    pulse = st.number_input("Pulse Rate", min_value=40, max_value=160)
    sugar = st.number_input("Sugar Level (mg/dL)", min_value=60, max_value=350)
    weight = st.number_input("Weight (kg)", min_value=35.0, max_value=200.0, step=0.1)
    notes = st.text_area("Symptoms/Notes")
    if st.button("Save Vitals"):
        if "vitals" not in st.session_state:
            st.session_state["vitals"] = []
        st.session_state["vitals"].append(dict(
            Date=date, BP=bp, Pulse=pulse, Sugar=sugar, Weight=weight, Notes=notes
        ))
        st.success("Vitals saved!")

with tab2:
    st.subheader("Health Reports & Trends")
    if "vitals" in st.session_state and st.session_state["vitals"]:
        df = pd.DataFrame(st.session_state["vitals"])
        st.dataframe(df)
        st.line_chart(df[["Pulse", "Sugar", "Weight"]])
        st.write(df.describe())
    else:
        st.info("Please add at least one vitals entry.")

with tab3:
    st.subheader("Medication Reminder")
    med_name = st.text_input("Medicine")
    med_time = st.time_input("Time to Take")
    if st.button("Add Reminder"):
        if "meds" not in st.session_state:
            st.session_state["meds"] = []
        st.session_state["meds"].append({"Medicine": med_name, "Time": med_time})
        st.success("Reminder added!")
    if "meds" in st.session_state and st.session_state["meds"]:
        st.table(pd.DataFrame(st.session_state["meds"]))

with tab4:
    st.subheader("Ask ChatGPT-3.5 (Health Assistant)")
    user_query = st.text_area("Type your health question")
    if st.button("Ask ChatGPT"):
        if user_query:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful health assistant for elders."},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=800,
                temperature=0.7
            )
            st.write(response.choices[0].message.content.strip())
        else:
            st.warning("Enter a question.")

st.markdown("---")
st.caption("Demo: Elder Health Management with Streamlit & ChatGPT-3.5")

