import streamlit as st
import random
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="SCADA PRO V6", layout="wide")

st.title("🏭 SCADA PRO — Operator Control Panel")

# ===== AUTO REFRESH =====
st_autorefresh(interval=2000, key="refresh")

# ===== STATE =====
if "running" not in st.session_state:
    st.session_state.running = False

if "mode" not in st.session_state:
    st.session_state.mode = "MANUAL"

if "data" not in st.session_state:
    st.session_state.data = []

if "alarms" not in st.session_state:
    st.session_state.alarms = []

# ===== SIDEBAR CONTROL =====
st.sidebar.header("🎛 Operator Panel")

if st.sidebar.button("🟢 START SYSTEM"):
    st.session_state.running = True

if st.sidebar.button("🔴 STOP SYSTEM"):
    st.session_state.running = False

if st.sidebar.button("🚨 EMERGENCY STOP"):
    st.session_state.running = False
    st.session_state.alarms.append({
        "time": datetime.now(),
        "msg": "EMERGENCY STOP ACTIVATED"
    })

mode = st.sidebar.radio("Mode", ["MANUAL", "AUTO"])
st.session_state.mode = mode

# ===== SIMULATION =====
if st.session_state.running:
    temp = random.randint(60, 180)
    pressure = random.randint(20, 140)
    vibration = random.randint(0, 100)
else:
    temp = 25
    pressure = 10
    vibration = 0

# ===== DATA SAVE =====
st.session_state.data.append({
    "time": datetime.now(),
    "temp": temp,
    "pressure": pressure,
    "vibration": vibration
})

if len(st.session_state.data) > 200:
    st.session_state.data = st.session_state.data[-200:]

df = pd.DataFrame(st.session_state.data)

# ===== ALARMS =====
def check_alarm(t, p, v):
    if t > 160 or p > 130:
        return "CRITICAL"
    elif t > 120 or v > 80:
        return "WARNING"
    return "OK"

status = check_alarm(temp, pressure, vibration)

if status != "OK":
    st.session_state.alarms.append({
        "time": datetime.now(),
        "msg": status
    })

# ===== DASHBOARD =====
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌡 Temp", temp)
col2.metric("⚙ Pressure", pressure)
col3.metric("📳 Vibration", vibration)
col4.metric("🏭 Mode", st.session_state.mode)

# ===== STATUS =====
if status == "CRITICAL":
    st.error("🔴 CRITICAL STATE")
elif status == "WARNING":
    st.warning("🟡 WARNING STATE")
else:
    st.success("🟢 NORMAL STATE")

# ===== TABS =====
tab1, tab2, tab3 = st.tabs(["📊 Trends", "🚨 Alarms", "🧠 AI Operator"])

# ===== TRENDS =====
with tab1:
    st.line_chart(df.set_index("time")[["temp", "pressure", "vibration"]])

# ===== ALARMS =====
with tab2:
    for a in st.session_state.alarms[-20:]:
        st.write(f"{a['time']} — {a['msg']}")

# ===== AI =====
with tab3:
    if status == "CRITICAL":
        st.error("SHUTDOWN REQUIRED IMMEDIATELY")
    elif status == "WARNING":
        st.warning("Reduce load and inspect system")
    else:
        st.success("System stable")

st.caption("SCADA PRO V6 — Industrial Operator System")