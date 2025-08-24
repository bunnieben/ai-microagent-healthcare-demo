
import json, re
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path("data/mock_health_api.json")
CRM_LOG = Path("crm_log.csv")

st.set_page_config(page_title="AI Microagent (Healthcare)", page_icon="🩺")

@st.cache_data
def load_data():
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def log_crm(user_text, intent, result):
    row = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "user_text": user_text,
        "intent": intent,
        "result": result[:2000]
    }
    if CRM_LOG.exists():
        df = pd.read_csv(CRM_LOG)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])
    df.to_csv(CRM_LOG, index=False)

def detect_intent(text):
    t = text.lower()
    if "appointment" in t and any(k in t for k in ["status","when","time","date","confirm"]):
        return "appointment_status"
    if "referral" in t or ("order" in t and "status" in t):
        return "referral_status"
    if "resched" in t or "change" in t:
        return "reschedule_appointment"
    if "member id" in t or "insurance" in t:
        return "member_info"
    return "small_talk"

def find_patient(data, name_or_id):
    if not name_or_id: return None
    name_or_id = name_or_id.lower()
    for p in data["patients"]:
        if p["patient_id"].lower() == name_or_id or p["name"].lower() == name_or_id:
            return p
    return None

def get_latest_appointment(data, pid):
    appts = [a for a in data["appointments"] if a["patient_id"] == pid]
    if not appts: return None
    appts.sort(key=lambda x: (x["date"], x["time"]), reverse=True)
    return appts[0]

def get_latest_referral(data, pid):
    refs = [o for o in data["orders"] if o["patient_id"] == pid]
    if not refs: return None
    refs.sort(key=lambda x: x["last_update"], reverse=True)
    return refs[0]

st.title("AI Microagent (Healthcare) 🩺")
st.caption("Prototype: appointment & referral status via mock API + CRM logging.")

data = load_data()
example = st.radio("Examples:", [
    "What's my next appointment for Alex Kim?",
    "Referral status for Jordan Lee",
    "Can I reschedule Alex Kim's appointment to next week?",
    "What is the member ID for Jordan Lee?"
], index=0)

user_text = st.text_input("Your message", value=example)
if st.button("Send") and user_text.strip():
    intent = detect_intent(user_text)
    m = re.search(r"for ([A-Za-z]+(?: [A-Za-z]+)?)", user_text, flags=re.IGNORECASE)
    name = m.group(1) if m else None
    patient = find_patient(data, name)
    if intent == "appointment_status":
        if not patient: resp = "Whose appointment should I check?"
        else:
            appt = get_latest_appointment(data, patient["patient_id"]); resp = f"{patient['name']}'s next appt: {appt['date']} {appt['time']} ({appt['department']}). Status: {appt['status']}." if appt else "No appointments."
    elif intent == "referral_status":
        if not patient: resp = "Whose referral should I check?"
        else:
            ref = get_latest_referral(data, patient["patient_id"]); resp = f"{patient['name']}'s referral: {ref['item']} ({ref['order_id']}), status {ref['status']}." if ref else "No referrals."
    elif intent == "reschedule_appointment":
        resp = f"I can request a reschedule for {patient['name'] if patient else 'this patient'}."
    elif intent == "member_info":
        resp = f"{patient['name']}'s member ID is {patient['member_id']}." if patient else "Which patient?"
    else:
        resp = "I can check appointment or referral status."
    st.markdown(resp); log_crm(user_text,intent,resp)

if Path("crm_log.csv").exists():
    st.subheader("CRM Log (last 10)")
    df = pd.read_csv("crm_log.csv"); st.dataframe(df.tail(10))
