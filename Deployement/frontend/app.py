import streamlit as st
import requests


st.title("Prediction of Churn Customer")
tenure = st.number_input("Tenure",min_value=0)
OnlineSecurity = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
MonthlyCharges = st.number_input("Monthly Charges",min_value=0)
TotalCharges = st.number_input("Total Charges",min_value=0)
# inference
data = {'tenure':tenure,
        'OnlineSecurity':OnlineSecurity,
        'Contract': Contract,
        'MonthlyCharges':MonthlyCharges,
        'TotalCharges':TotalCharges}

URL = "https://backend-model.herokuapp.com/predict"

# komunikasi
r = requests.post(URL, json=data)
res = r.json()
if res['code'] == 200:
    with st.expander("RESULT"):
        if res['result']['prediction'] == '1':
            st.title("Churn Customer")
        else:
            st.title("Not Churn Customer")
else:
    st.write("Mohon maaf terjadi kesalahan")
    st.write(f"keterangan : {res['result']['error_msg']}")