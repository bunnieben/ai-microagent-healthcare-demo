# AI Microagent Demo (Healthcare)

A tiny **Sales Engineer-style prototype** that simulates appointment/referral lookups with a mock API and logs CRM-style interactions.

---

## Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-microagent-healthcare-demo.streamlit.app/)


---

## Why this project matters
This demo mirrors an **Associate Sales Engineer workflow**:
- **Discovery → Solution Design → Demo Build**: chose a healthcare use case and mapped user intents to data lookups.
- **APIs & Integrations**: reads from a mock JSON, standing in for a REST API. In production, this would connect to real systems.
- **CRM Hygiene**: every interaction is logged to a CSV, simulating HubSpot or Salesforce deal activity.
- **Presentation**: packaged with a README, live demo, and Loom walkthrough—like a mini RFP/demo asset.

---

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
