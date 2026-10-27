import streamlit as st
import pandas as pd
import requests
from pathlib import Path
from datetime import date, time

st.set_page_config(page_title="AI Smart Healthcare", page_icon="🏥", layout="wide")
BASE_DIR = Path(__file__).resolve().parent
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
LOW_STOCK_THRESHOLD = 10

PATIENT_COLUMNS = ["Patient ID", "Name", "Age", "Gender", "Disease"]
APPOINTMENT_COLUMNS = ["Appointment ID", "Patient ID", "Doctor", "Date", "Time"]
MEDICINE_COLUMNS = ["Medicine ID", "Name", "Quantity", "Price"]
DEMO_ACCOUNTS = {
    "doctor": {"password": "doctor123", "role": "Doctor"},
    "patient102": {"password": "patient123", "role": "Patient", "patient_id": "102"},
}

st.markdown("""
<style>
.stApp{background:#f4f7fc;color:#193451;font-family:Arial,sans-serif}
[data-testid="stHeader"]{background:rgba(244,247,252,.95)}
.block-container{padding-top:1.8rem;padding-bottom:2rem;max-width:1500px}
h1,h2,h3{color:#153d68;font-weight:750;letter-spacing:-.4px}
p,label{color:#354b65}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#102b49,#173f65)}
[data-testid="stSidebar"] *{color:#f4f8ff}
[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.18)}
.stTextInput input,.stNumberInput input,.stDateInput input,.stTimeInput input{border:1px solid #d5e1ef;border-radius:9px;background:white;min-height:42px}
[data-baseweb="select"]>div{border-radius:9px;border-color:#d5e1ef;background:white}
.stButton>button,.stFormSubmitButton>button{border-radius:9px;border:1px solid #246bd2;background:linear-gradient(100deg,#347fe5,#205fbd);color:white;font-weight:650;min-height:42px}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#174f9f;border-color:#174f9f;color:white}
[data-testid="stForm"]{background:white;border:1px solid #e0e9f5;border-radius:14px;padding:20px}
[data-testid="stExpander"]{background:white;border:1px solid #e0e9f5;border-radius:13px}
.stTabs [data-baseweb="tab-list"]{gap:8px;border-bottom:1px solid #dbe5f1}
.stTabs [data-baseweb="tab"]{background:#eaf0fa;border-radius:9px 9px 0 0;padding:12px 18px;color:#284969;font-weight:600}
.stTabs [aria-selected="true"]{background:white;color:#1766c4}
[data-testid="stMetric"]{background:white;border:1px solid #e0e9f5;border-radius:13px;padding:18px;box-shadow:0 3px 12px rgba(26,65,112,.04)}
[data-testid="stMetricLabel"]{color:#58718e;font-weight:600}
[data-testid="stMetricValue"]{color:#1c5eaf;font-weight:750}
[data-testid="stDataFrame"],[data-testid="stTable"]{border:1px solid #dce6f2;border-radius:10px;overflow:hidden}
[data-testid="stAlert"]{border-radius:10px}
.login-panel{background:linear-gradient(145deg,#fff,#f0f6ff);border:1px solid #dce8f8;border-radius:20px;padding:30px 26px;box-shadow:0 12px 40px rgba(24,70,125,.09);text-align:center}
.login-icon{font-size:54px}.login-title{font-size:32px;font-weight:800;color:#153d68}.login-subtitle{font-size:15px;color:#627993;margin-bottom:20px}
.dashboard-banner{background:linear-gradient(110deg,#174c87,#2d83df);padding:24px 28px;border-radius:16px;margin-bottom:22px;box-shadow:0 6px 20px rgba(30,95,170,.14)}
.dashboard-banner h2{color:white!important;margin:0}.dashboard-banner p{color:#e7f2ff!important;margin-top:7px;margin-bottom:0}
.app-footer{text-align:center;padding:20px 0 4px;color:#7a8ca3;font-size:12px}
</style>
""", unsafe_allow_html=True)

def load_records(filename, columns):
    path = BASE_DIR / filename
    if not path.exists():
        return pd.DataFrame(columns=columns)
    try:
        df = pd.read_csv(path, sep="|", header=None, dtype=str, keep_default_na=False)
        if df.shape[1] != len(columns):
            st.error(f"{filename} contains an unexpected number of columns.")
            return pd.DataFrame(columns=columns)
        df.columns = columns
        return df
    except (pd.errors.ParserError, OSError, ValueError) as error:
        st.error(f"Could not read {filename}: {error}")
        return pd.DataFrame(columns=columns)

def save_records(filename, df):
    try:
        df.to_csv(BASE_DIR / filename, sep="|", header=False, index=False, encoding="utf-8")
        return True
    except (OSError, ValueError) as error:
        st.error(f"Could not save {filename}: {error}")
        return False

def invalid_text(*values):
    return any("|" in str(v) or "\n" in str(v) or "\r" in str(v) for v in values)

def duplicate_id(df, column, value):
    return (df[column].astype(str) == str(value)).any()

def parse_dates(series):
    return pd.to_datetime(series, errors="coerce").dt.date

# LOGIN
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    _, login_col, _ = st.columns([1, 1.15, 1])
    with login_col:
        st.markdown("""<div class="login-panel"><div class="login-icon">🏥</div><div class="login-title">AI Smart Healthcare</div><div class="login-subtitle">Better Care · Healthier Tomorrow</div></div>""", unsafe_allow_html=True)
        st.write("")
        with st.form("login_form"):
            st.markdown("### Welcome Back")
            st.caption("Sign in to access your healthcare dashboard.")
            selected_role = st.selectbox("Login as", ["Doctor", "Patient"])
            username = st.text_input("Username", placeholder="Enter your username").strip().lower()
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_clicked = st.form_submit_button("🔐 Sign In", use_container_width=True)
        if login_clicked:
            account = DEMO_ACCOUNTS.get(username)
            if account and account["password"] == password and account["role"] == selected_role:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_role = account["role"]
                st.session_state.patient_id = account.get("patient_id")
                st.rerun()
            else:
                st.error("Invalid username, password, or selected role.")
        with st.expander("View demo login credentials"):
            st.markdown("**👨‍⚕️ Doctor account**")
            st.code("Username: doctor\nPassword: doctor123")
            st.markdown("**🧑 Patient account**")
            st.code("Username: patient102\nPassword: patient123")
        st.info("Local demonstration only. Use fictional patient information; do not enter real medical records.")
    st.markdown('<div class="app-footer">AI Smart Healthcare · Local Demo Application</div>', unsafe_allow_html=True)
    st.stop()

# LOAD DATA
patients = load_records("patients.txt", PATIENT_COLUMNS)
appointments = load_records("appointments.txt", APPOINTMENT_COLUMNS)
medicines = load_records("medicines.txt", MEDICINE_COLUMNS)
role = st.session_state.user_role
username = st.session_state.username

# SIDEBAR
with st.sidebar:
    st.markdown("# 🏥 AI Healthcare")
    st.caption("Better Care · Healthier Tomorrow")
    st.divider()
    st.markdown(f"**Welcome, {role}**")
    st.caption(f"Signed in as: {username}")
    st.divider()
    st.markdown("### 🩺 Doctor Workspace" if role == "Doctor" else "### 💙 Patient Workspace")
    st.markdown("Manage patients, appointments, and medicines." if role == "Doctor" else "View your patient record and appointments.")
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        for key in ["logged_in", "username", "user_role", "patient_id"]:
            st.session_state.pop(key, None)
        st.rerun()
    st.divider()
    st.caption("🔒 Local demo application · Use fictional data only")

st.markdown(f'<div class="dashboard-banner"><h2>🏥 AI Smart Healthcare</h2><p>Your healthcare management workspace · Logged in as {role}</p></div>', unsafe_allow_html=True)

# DOCTOR DASHBOARD
if role == "Doctor":
    dates = parse_dates(appointments["Date"]) if not appointments.empty else pd.Series(dtype="object")
    if appointments.empty:
        todays = appointments.copy()
        upcoming = appointments.copy()
        past = appointments.copy()
    else:
        valid = dates.notna()
        todays = appointments[dates == date.today()].copy()
        upcoming = appointments[(dates > date.today()) & valid].copy()
        past = appointments[(dates < date.today()) & valid].copy()

    st.markdown("## 📊 Dashboard Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👥 Total Patients", len(patients))
    m2.metric("📅 Total Appointments", len(appointments))
    m3.metric("🗓️ Today's Appointments", len(todays))
    m4.metric("💊 Medicine Types", len(medicines))

    schedule_tab, patient_tab, appointment_tab, medicine_tab = st.tabs([
        "🗓️ Schedule Overview", "👥 Patient Management", "📅 Appointments", "💊 Medicine Inventory"
    ])

    with schedule_tab:
        st.markdown("### 🗓️ Today's Schedule")
        if todays.empty:
            st.info("There are no appointments scheduled for today.")
        else:
            st.dataframe(todays.sort_values("Time"), use_container_width=True, hide_index=True)
        st.markdown("### ⏭️ Upcoming Appointments")
        if upcoming.empty:
            st.info("There are no upcoming appointments.")
        else:
            upcoming_view = upcoming.copy()
            upcoming_view["_date_sort"] = pd.to_datetime(upcoming_view["Date"], errors="coerce")
            upcoming_view = upcoming_view.sort_values(["_date_sort", "Time"]).drop(columns="_date_sort")
            st.dataframe(upcoming_view, use_container_width=True, hide_index=True)
        if not past.empty:
            with st.expander("View past appointments"):
                st.dataframe(past, use_container_width=True, hide_index=True)

    with patient_tab:
        st.markdown("## 👥 Patient Management")
        st.caption("Register new patients, search existing records, and review patient information.")
        with st.expander("➕ Add a New Patient", expanded=True):
            with st.form("add_patient_form"):
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("Patient Name", placeholder="Enter full name")
                    age = st.number_input("Age", min_value=1, max_value=120, value=25)
                with c2:
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    disease = st.text_input("Disease / Condition", placeholder="Enter condition")
                add_patient = st.form_submit_button("➕ Add Patient", use_container_width=True)
            if add_patient:
                if not name.strip() or not disease.strip():
                    st.error("Please enter the patient name and disease.")
                elif invalid_text(name, disease):
                    st.error("The | character and newlines are not allowed.")
                else:
                    try:
                        response = requests.post(f"{API_URL}/patients", json={"name": name.strip(), "age": int(age), "gender": gender, "disease": disease.strip()}, timeout=10)
                        if response.status_code == 201:
                            try:
                                result = response.json()
                            except ValueError:
                                result = {}
                            if "id" in result:
                                st.success(f"Patient added successfully! Patient ID: {result['id']}")
                                st.rerun()
                            else:
                                st.error("Patient creation response did not contain a patient ID.")
                        else:
                            try:
                                message = response.json().get("detail", "Could not add patient.")
                            except ValueError:
                                message = "Could not add patient."
                            st.error(f"Error: {message}")
                    except requests.exceptions.ConnectionError:
                        st.error("Cannot connect to FastAPI. Start the backend in another terminal.")
                    except requests.exceptions.Timeout:
                        st.error("The API request timed out. Check the server before retrying.")
                    except requests.exceptions.RequestException as error:
                        st.error(f"Request failed: {error}")

        st.markdown("### 🔎 Search Patient")
        sc1, sc2 = st.columns([3, 1])
        with sc1:
            search_id = st.text_input("Patient ID", placeholder="Enter patient ID", key="doctor_search_patient")
        with sc2:
            st.write("")
            st.write("")
            search_clicked = st.button("🔎 Search", key="search_patient_button", use_container_width=True)
        if search_clicked:
            if not search_id.strip():
                st.warning("Enter a patient ID first.")
            else:
                found = patients[patients["Patient ID"].astype(str) == search_id.strip()]
                if found.empty:
                    st.warning("No patient found.")
                else:
                    st.success("Patient found.")
                    st.dataframe(found, use_container_width=True, hide_index=True)
        st.divider()
        st.markdown("### 📋 All Patient Records")
        if patients.empty:
            st.info("No patient records are available yet. Add your first patient above.")
        else:
            st.dataframe(patients, use_container_width=True, hide_index=True)

    with appointment_tab:
        st.markdown("## 📅 Appointment Management")
        c1, c2 = st.columns(2)
        c1.metric("Total Appointments", len(appointments))
        c2.metric("Registered Patients", len(patients))
        with st.expander("➕ Book a New Appointment", expanded=True):
            with st.form("add_appointment_form"):
                appointment_id = st.number_input("Appointment ID", min_value=1, value=1, step=1)
                if not patients.empty:
                    patient_options = patients["Patient ID"].tolist()
                    selected_patient = st.selectbox("Select Patient ID", patient_options)
                else:
                    selected_patient = None
                    st.info("Register a patient before booking an appointment.")
                doctor_name = st.text_input("Doctor Name", placeholder="Enter doctor's name")
                c1, c2 = st.columns(2)
                with c1:
                    appointment_date = st.date_input("Appointment Date", value=date.today(), min_value=date.today())
                with c2:
                    appointment_time = st.time_input("Appointment Time", value=time(10, 0))
                add_appointment = st.form_submit_button("📅 Book Appointment", use_container_width=True)
            if add_appointment:
                if patients.empty:
                    st.error("Register a patient before booking.")
                elif not doctor_name.strip():
                    st.error("Enter the doctor's name.")
                elif invalid_text(doctor_name):
                    st.error("The | character and newlines are not allowed.")
                elif duplicate_id(appointments, "Appointment ID", int(appointment_id)):
                    st.error("Appointment ID already exists.")
                else:
                    new_row = pd.DataFrame([{
                        "Appointment ID": str(int(appointment_id)),
                        "Patient ID": str(selected_patient),
                        "Doctor": doctor_name.strip(),
                        "Date": appointment_date.strftime("%Y-%m-%d"),
                        "Time": appointment_time.strftime("%H:%M")
                    }])
                    updated = pd.concat([appointments, new_row], ignore_index=True)
                    if save_records("appointments.txt", updated):
                        st.success("Appointment booked successfully!")
                        st.rerun()
        st.divider()
        st.markdown("### 📋 All Appointments")
        if appointments.empty:
            st.info("No appointments have been booked yet.")
        else:
            st.dataframe(appointments, use_container_width=True, hide_index=True)

    with medicine_tab:
        st.markdown("## 💊 Medicine Inventory")
        st.caption("Add medicines, monitor quantities, and update stock.")
        qty = pd.to_numeric(medicines["Quantity"], errors="coerce").fillna(0) if not medicines.empty else pd.Series(dtype="float64")
        total_stock = int(qty.sum()) if not qty.empty else 0
        low_stock = medicines[qty < LOW_STOCK_THRESHOLD].copy() if not medicines.empty else medicines.copy()
        a, b, c = st.columns(3)
        a.metric("Medicine Types", len(medicines))
        b.metric("Total Units in Stock", total_stock)
        c.metric("⚠️ Low-Stock Items", len(low_stock))
        if not low_stock.empty:
            st.warning(f"Low-stock alert: {len(low_stock)} medicine(s) have fewer than {LOW_STOCK_THRESHOLD} units remaining.")
            st.dataframe(low_stock, use_container_width=True, hide_index=True)
        else:
            st.success(f"No low-stock medicines. All quantities are at least {LOW_STOCK_THRESHOLD} units.")

        with st.expander("➕ Add a New Medicine", expanded=True):
            with st.form("add_medicine_form"):
                c1, c2 = st.columns(2)
                with c1:
                    medicine_id = st.number_input("Medicine ID", min_value=1, value=1, step=1)
                    medicine_name = st.text_input("Medicine Name", placeholder="Enter medicine name")
                with c2:
                    quantity = st.number_input("Quantity", min_value=0, value=0, step=1)
                    price = st.number_input("Price", min_value=0.0, value=0.0, step=0.5, format="%.2f")
                add_medicine = st.form_submit_button("➕ Add Medicine", use_container_width=True)
            if add_medicine:
                if not medicine_name.strip():
                    st.error("Enter the medicine name.")
                elif invalid_text(medicine_name):
                    st.error("The | character and newlines are not allowed.")
                elif duplicate_id(medicines, "Medicine ID", int(medicine_id)):
                    st.error("Medicine ID already exists.")
                else:
                    new_row = pd.DataFrame([{
                        "Medicine ID": str(int(medicine_id)), "Name": medicine_name.strip(),
                        "Quantity": str(int(quantity)), "Price": f"{price:.2f}"
                    }])
                    updated = pd.concat([medicines, new_row], ignore_index=True)
                    if save_records("medicines.txt", updated):
                        st.success("Medicine added successfully!")
                        st.rerun()

        st.markdown("### 📦 Update Medicine Stock")
        if not medicines.empty:
            medicine_ids = medicines["Medicine ID"].tolist()
            selected_mid = st.selectbox("Select Medicine ID", medicine_ids)
            selected_rows = medicines[medicines["Medicine ID"].astype(str) == str(selected_mid)]
            selected_medicine = selected_rows.iloc[0]
            st.info(f"Selected medicine: {selected_medicine['Name']}")
            try:
                current_quantity = int(selected_medicine["Quantity"])
            except (ValueError, TypeError):
                current_quantity = 0
            new_quantity = st.number_input("New Quantity", min_value=0, value=max(0, current_quantity), step=1, key=f"stock_{selected_mid}")
            if st.button("💾 Update Stock"):
                updated = medicines.copy()
                updated.loc[updated["Medicine ID"].astype(str) == str(selected_mid), "Quantity"] = str(int(new_quantity))
                if save_records("medicines.txt", updated):
                    st.success("Medicine stock updated successfully!")
                    st.rerun()
        else:
            st.info("No medicines are available. Add your first medicine above.")
        st.divider()
        st.markdown("### 📋 All Medicines")
        if medicines.empty:
            st.info("No medicines found.")
        else:
            st.dataframe(medicines, use_container_width=True, hide_index=True)

# PATIENT DASHBOARD
elif role == "Patient":
    patient_id = str(st.session_state.patient_id)
    my_patients = patients[patients["Patient ID"].astype(str) == patient_id]
    my_appointments = appointments[appointments["Patient ID"].astype(str) == patient_id]
    st.markdown("## 💙 My Health Dashboard")
    st.caption("View your patient record and upcoming appointments.")
    c1, c2 = st.columns(2)
    c1.metric("My Patient ID", patient_id)
    c2.metric("My Appointments", len(my_appointments))
    record_tab, my_appointments_tab = st.tabs(["💙 My Patient Record", "📅 My Appointments"])
    with record_tab:
        st.markdown("### 🩺 Personal Health Record")
        if my_patients.empty:
            st.warning(f"No patient record exists for ID {patient_id}. Please ask the doctor to add your record.")
        else:
            st.success("Your patient record is available.")
            record = my_patients.iloc[0]
            c1, c2 = st.columns(2)
            c1.metric("Patient Name", record["Name"])
            c1.metric("Age", record["Age"])
            c2.metric("Gender", record["Gender"])
            c2.metric("Recorded Condition", record["Disease"])
            st.markdown("#### Complete Record")
            st.dataframe(my_patients, use_container_width=True, hide_index=True)
    with my_appointments_tab:
        st.markdown("### 📅 My Appointments")
        if my_appointments.empty:
            st.info("You do not have any appointments yet. Contact your doctor to book an appointment.")
        else:
            st.dataframe(my_appointments, use_container_width=True, hide_index=True)
    st.divider()
    st.info("This application is a local demonstration, not a medical advice service. Contact a qualified healthcare professional for personal medical advice.")

st.markdown('<div class="app-footer">🏥 AI Smart Healthcare | Local Demo Application<br><br>Better Care · Healthier Tomorrow</div>', unsafe_allow_html=True)
