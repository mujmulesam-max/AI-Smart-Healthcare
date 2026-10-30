
import streamlit as st
import pandas as pd
import cv2
import numpy as np

from pathlib import Path
from datetime import date, datetime, time


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Smart Healthcare",
    page_icon="🏥",
    layout="wide"
)


# ==========================================
# 2. FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

PATIENT_FILE = BASE_DIR / "patients.txt"
APPOINTMENT_FILE = BASE_DIR / "appointments.txt"
MEDICINE_FILE = BASE_DIR / "medicines.txt"

FACE_MODEL = BASE_DIR / "haarcascade_frontalface_default.xml"


# ==========================================
# 3. MODERN DARK HEALTHCARE UI
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --bg:#080f1d; --panel:#111d30; --panel2:#15243a; --line:#243a55; --cyan:#43d9ee; --muted:#91a8c2; }
.stApp { background:radial-gradient(circle at 75% 0%,#142b43 0%,#0a1424 38%,#070d18 100%); color:#eaf3ff; font-family:'DM Sans',sans-serif; }
.block-container { max-width:1440px; padding-top:2rem; padding-bottom:3rem; }
h1,h2,h3,h4 { font-family:'Manrope',sans-serif!important; color:#f2f8ff!important; letter-spacing:-.4px; }
h1 { font-size:2.15rem!important; }
p,li,label,.stMarkdown { color:#c5d4e6; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0d1a2c,#091321); border-right:1px solid #20354e; }
[data-testid="stSidebar"] > div { padding:1.5rem 1rem; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .55rem .7rem; border-radius:10px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:#172b42; }
[data-testid="stSidebar"] [data-testid="stRadio"] label p { color:#c9d9eb!important; font-weight:600; }
.stButton>button,.stFormSubmitButton>button { background:linear-gradient(100deg,#087eaa,#12b9c8); color:white!important; border:0; border-radius:10px; min-height:2.7rem; font-weight:700; box-shadow:0 7px 18px #00a9c51c; transition:.2s; }
.stButton>button:hover,.stFormSubmitButton>button:hover { background:linear-gradient(100deg,#0c9dcc,#25d9df); transform:translateY(-1px); box-shadow:0 8px 22px #00c5dd35; }
[data-testid="stMetric"] { background:linear-gradient(145deg,#172941,#101d30); border:1px solid #29445f; border-radius:16px; padding:18px 20px; box-shadow:0 10px 25px #00000020; }
[data-testid="stMetricLabel"] p { color:#9fb4cb!important; font-size:.85rem!important; }
[data-testid="stMetricValue"] { color:#53dff0!important; font-family:'Manrope',sans-serif; }
.stTextInput input,.stNumberInput input,.stDateInput input,.stTextArea textarea { background:#0d1a2b!important; color:#eef7ff!important; border:1px solid #2a435e!important; border-radius:10px!important; }
[data-baseweb="select"]>div { background:#0d1a2b!important; border-color:#2a435e!important; border-radius:10px!important; }
[data-baseweb="select"] * { color:#eef7ff!important; }
button[data-baseweb="tab"] { color:#9fb6ce!important; font-weight:700; }
button[data-baseweb="tab"][aria-selected="true"] { color:#51dcec!important; border-bottom:2px solid #51dcec!important; }
[data-testid="stDataFrame"],[data-testid="stTable"] { border:1px solid #29435e; border-radius:12px; overflow:hidden; }
div[data-testid="stForm"],div[data-testid="stExpander"] { background:#101d30; border:1px solid #263e59; border-radius:14px; padding:12px; }
hr { border-color:#263e59!important; }
a { color:#54d9ec!important; }
/* reusable visual sections */
.hero-panel { background:linear-gradient(110deg,#12344b,#14253b 65%,#17263d); border:1px solid #2b526d; border-radius:20px; padding:25px 28px; margin:0 0 22px 0; box-shadow:0 16px 35px #00000024; }
.hero-kicker { color:#58dff0; text-transform:uppercase; letter-spacing:1.5px; font-size:11px; font-weight:800; }
.hero-title { color:#f4f9ff; font-family:'Manrope',sans-serif; font-size:27px; font-weight:800; margin:7px 0 4px; }
.hero-copy { color:#b4c8dc; font-size:14px; }
.section-label { color:#55d9eb; font-size:11px; letter-spacing:1.5px; font-weight:800; text-transform:uppercase; margin:8px 0 10px; }
.info-panel { background:linear-gradient(145deg,#14243a,#101c2e); border:1px solid #29415c; border-radius:16px; padding:18px; min-height:110px; }
.info-panel .small { color:#91a9c2; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:.8px; }
.info-panel .big { color:#eff8ff; font-family:'Manrope',sans-serif; font-size:23px; font-weight:800; margin-top:8px; }
.info-panel .hint { color:#91a9c2; font-size:12px; margin-top:3px; }
[data-testid="stAlert"] { border-radius:12px; }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. TEXT FILE STORAGE
# ==========================================

def read_records(file_path):
    if not file_path.exists():
        return []

    records = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                records.append(line.split("|"))

    return records


def save_record(file_path, record):
    with open(file_path, "a", encoding="utf-8") as file:
        file.write("|".join(str(value) for value in record) + "\n")


def initialize_files():
    if not PATIENT_FILE.exists():
        save_record(
            PATIENT_FILE,
            ["102", "Demo Patient", "20", "Other", "General Checkup"]
        )

    if not APPOINTMENT_FILE.exists():
        APPOINTMENT_FILE.touch()

    if not MEDICINE_FILE.exists():
        save_record(
            MEDICINE_FILE,
            ["1", "Paracetamol", "20", "5"]
        )

        save_record(
            MEDICINE_FILE,
            ["2", "Cough Syrup", "10", "80"]
        )


initialize_files()


# ==========================================
# 5. HELPER FUNCTIONS
# ==========================================

def heading(title, description=""):
    st.markdown(f"<div class='section-label'>AI SMART HEALTHCARE</div><h1>{title}</h1>", unsafe_allow_html=True)
    if description:
        st.caption(description)
    st.divider()


def get_patients():
    return read_records(PATIENT_FILE)



# Doctor schedules: working days and available appointment times
DOCTOR_SCHEDULES = {
    "Dr. Sharma": {
        "days": [0, 1, 2, 3, 4, 5],  # Monday to Saturday
        "times": [
            "09:00 AM", "10:00 AM", "11:00 AM",
            "12:00 PM", "02:00 PM", "03:00 PM"
        ]
    },
    "Dr. Patel": {
        "days": [0, 1, 2, 3, 4],  # Monday to Friday
        "times": [
            "10:00 AM", "11:00 AM", "12:00 PM",
            "02:00 PM", "03:00 PM", "04:00 PM"
        ]
    },
    "Dr. Deshmukh": {
        "days": [1, 2, 3, 4, 5],  # Tuesday to Saturday
        "times": [
            "09:00 AM", "10:00 AM", "11:00 AM",
            "02:00 PM", "03:00 PM", "04:00 PM"
        ]
    }
}


def get_appointments():
    """Read appointments and support older five-field records."""
    appointments = []

    for record in read_records(APPOINTMENT_FILE):
        if len(record) == 5:
            # Existing appointments are treated as upcoming.
            record = record + ["Upcoming"]

        elif len(record) != 6:
            continue

        appointments.append(record)

    return appointments


def is_slot_booked(doctor, appointment_date, appointment_time):
    """Cancelled appointments do not block a slot."""
    for appointment in get_appointments():
        if (
            appointment[2] == doctor
            and appointment[3] == str(appointment_date)
            and appointment[4] == appointment_time
            and appointment[5] != "Cancelled"
        ):
            return True

    return False


def get_available_slots(doctor, appointment_date):
    """Return slots within the doctor's configured schedule."""
    schedule = DOCTOR_SCHEDULES[doctor]

    # Python weekday: Monday=0, Sunday=6
    if appointment_date.weekday() not in schedule["days"]:
        return []

    available = []

    for slot in schedule["times"]:
        if is_slot_booked(doctor, appointment_date, slot):
            continue

        slot_time = datetime.strptime(
            slot, "%I:%M %p"
        ).time()

        # Do not offer a time that has already passed today.
        if appointment_date == date.today():
            if slot_time <= datetime.now().time():
                continue

        available.append(slot)

    return available


def save_appointment_record(appointment_id, patient_id,
                            doctor, appointment_date,
                            appointment_time, status="Upcoming"):
    """Save a new appointment with its status."""
    save_record(
        APPOINTMENT_FILE,
        [
            appointment_id,
            patient_id,
            doctor,
            appointment_date,
            appointment_time,
            status
        ]
    )



def get_medicines():
    return read_records(MEDICINE_FILE)


def records_to_dataframe(records, columns):
    valid_records = [
        record for record in records
        if len(record) == len(columns)
    ]

    return pd.DataFrame(valid_records, columns=columns)


def next_record_id(records):
    ids = [
        int(record[0])
        for record in records
        if record and record[0].isdigit()
    ]

    return max(ids, default=0) + 1


# ==========================================
# 6. LOGIN PAGE
# ==========================================

def login_page():
    st.markdown(
        "<h1 style='text-align:center;'>🏥 AI Smart Healthcare</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Your simple digital healthcare management system"
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    left, center, right = st.columns([1, 1.4, 1])

    with center:
        st.subheader("🔐 Login")

        role = st.selectbox(
            "Login as",
            ["Patient", "Doctor"]
        )

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if (
                role == "Doctor"
                and username == "doctor"
                and password == "doctor123"
            ):
                st.session_state.logged_in = True
                st.session_state.role = "Doctor"
                st.session_state.username = username
                st.rerun()

            elif (
                role == "Patient"
                and username == "patient102"
                and password == "patient123"
            ):
                st.session_state.logged_in = True
                st.session_state.role = "Patient"
                st.session_state.username = username
                st.session_state.patient_id = "102"
                st.rerun()

            else:
                st.error("Invalid username or password.")

        st.info(
            "Doctor demo: doctor / doctor123\n\n"
            "Patient demo: patient102 / patient123"
        )


# ==========================================
# 7. DOCTOR OVERVIEW
# ==========================================

def doctor_overview():
    patients = get_patients()
    appointments = get_appointments()
    medicines = get_medicines()
    upcoming = [a for a in appointments if len(a) == 6 and a[5] == "Upcoming"]
    st.markdown("""
    <div class="hero-panel">
      <div class="hero-kicker">Doctor workspace · Overview</div>
      <div class="hero-title">Good day, Doctor 👋</div>
      <div class="hero-copy">Here is your clinic snapshot. Review patient activity and manage today's care from one place.</div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total patients", len(patients), help="Registered patient records")
    c2.metric("All appointments", len(appointments))
    c3.metric("Upcoming", len(upcoming))
    c4.metric("Medicine items", len(medicines))
    left,right = st.columns([1.65,1], gap="large")
    with left:
        st.markdown("<div class='section-label'>RECENT ACTIVITY</div>", unsafe_allow_html=True)
        st.subheader("Recent appointments")
        if appointments:
            names = {p[0]:p[1] for p in patients if len(p)==5}
            rows = [{"Patient":names.get(a[1],"Unknown"),"Doctor":a[2],"Date":a[3],"Time":a[4],"Status":a[5]} for a in appointments[-8:][::-1] if len(a)==6]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No appointments yet. Open Appointments to create the first booking.")
    with right:
        st.markdown("<div class='section-label'>QUICK SUMMARY</div>", unsafe_allow_html=True)
        st.subheader("Clinic at a glance")
        st.markdown(f"<div class='info-panel'><div class='small'>Registered patients</div><div class='big'>{len(patients)}</div><div class='hint'>Patient records in your system</div></div>", unsafe_allow_html=True)
        st.write("")
        st.markdown(f"<div class='info-panel'><div class='small'>Appointments needing attention</div><div class='big'>{len(upcoming)}</div><div class='hint'>Currently marked as upcoming</div></div>", unsafe_allow_html=True)
        st.write("")
        st.caption("Use the navigation panel to manage patients, appointments and medicine inventory.")


# ==========================================
# 8. PATIENT MANAGEMENT
# ==========================================

def patient_management():
    heading(
        "Patient Management",
        "Register and view patient records."
    )

    tab1, tab2 = st.tabs([
        "➕ Register Patient",
        "📋 View Patients"
    ])

    with tab1:
        with st.form("patient_form", clear_on_submit=True):
            name = st.text_input("Patient Name")

            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=18
            )

            gender = st.selectbox(
                "Gender",
                ["Female", "Male", "Other"]
            )

            disease = st.text_input("Reason for visit")

            submitted = st.form_submit_button("Register Patient")

            if submitted:
                if not name.strip() or not disease.strip():
                    st.error("Please enter the patient name and reason for visit.")
                else:
                    new_id = max(
                        102,
                        next_record_id(get_patients()) - 1
                    ) + 1

                    save_record(
                        PATIENT_FILE,
                        [
                            new_id,
                            name.strip(),
                            age,
                            gender,
                            disease.strip()
                        ]
                    )

                    st.success(
                        f"Patient registered successfully. ID: {new_id}"
                    )
                    st.rerun()

    with tab2:
        patients = get_patients()

        if patients:
            df = records_to_dataframe(
                patients,
                ["Patient ID", "Name", "Age", "Gender", "Reason for Visit"]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No patient records found.")


# ==========================================
# 9. APPOINTMENT MANAGEMENT
# ==========================================



# ==========================================
# APPOINTMENT MANAGEMENT
# ==========================================

def appointment_management():
    heading(
        "Appointment Management",
        "Book appointments for new or existing patients and manage bookings."
    )

    tab1, tab2 = st.tabs([
        "📅 Book Appointment",
        "📋 Manage Appointments"
    ])

    patients = [
        p for p in get_patients()
        if len(p) == 5
    ]

    # ======================================
    # TAB 1: BOOK APPOINTMENT
    # ======================================

    with tab1:
        st.subheader("Book an Appointment")

        booking_type = st.radio(
            "Select patient type",
            ["New Patient", "Existing Patient"],
            horizontal=True,
            key="booking_patient_type"
        )

        with st.form("appointment_form"):

            patient_id = None
            new_name = ""
            new_age = 18
            new_gender = "Not specified"
            new_reason = ""

            # Existing patient
            if booking_type == "Existing Patient":

                if patients:
                    patient_options = {
                        f"{p[0]} - {p[1]}": p[0]
                        for p in patients
                    }

                    selected_patient = st.selectbox(
                        "Select Patient",
                        list(patient_options.keys())
                    )

                    patient_id = patient_options[selected_patient]

                else:
                    st.warning(
                        "No patients registered yet. "
                        "Select New Patient to register one."
                    )

            # New patient
            else:
                st.markdown("### Register New Patient")

                new_name = st.text_input(
                    "Patient Full Name"
                )

                col1, col2 = st.columns(2)

                with col1:
                    new_age = st.number_input(
                        "Age",
                        min_value=0,
                        max_value=120,
                        value=18,
                        step=1
                    )

                with col2:
                    new_gender = st.selectbox(
                        "Gender",
                        [
                            "Not specified",
                            "Female",
                            "Male",
                            "Other"
                        ]
                    )

                new_reason = st.text_input(
                    "Reason for Visit"
                )

            st.markdown("### Appointment Details")

            doctor = st.selectbox(
                "Select Doctor",
                list(DOCTOR_SCHEDULES.keys())
            )

            appointment_date = st.date_input(
                "Appointment Date",
                value=date.today(),
                min_value=date.today()
            )

            available_slots = get_available_slots(
                doctor,
                appointment_date
            )

            if available_slots:
                appointment_time = st.selectbox(
                    "Available Time",
                    available_slots
                )
            else:
                appointment_time = None
                st.warning(
                    "No available slots. Please select another date."
                )

            submitted = st.form_submit_button(
                "Confirm Appointment",
                use_container_width=True
            )

            # ==================================
            # SAVE BOOKING
            # ==================================

            if submitted:

                clean_name = new_name.strip()
                clean_reason = new_reason.strip()

                if booking_type == "New Patient":

                    if not clean_name:
                        st.error(
                            "Please enter the patient's full name."
                        )

                    elif "|" in clean_name or "|" in clean_reason:
                        st.error(
                            "Please remove the | character "
                            "from the patient details."
                        )

                    elif appointment_time is None:
                        st.error(
                            "Please select a date with an available slot."
                        )

                    elif is_slot_booked(
                        doctor,
                        appointment_date,
                        appointment_time
                    ):
                        st.error(
                            "This time slot is already booked. "
                            "Please select another slot."
                        )

                    else:
                        current_patients = [
                            p for p in get_patients()
                            if len(p) == 5
                        ]

                        patient_id = str(
                            next_record_id(current_patients)
                        )

                        # Save the new patient
                        save_record(
                            PATIENT_FILE,
                            [
                                patient_id,
                                clean_name,
                                int(new_age),
                                new_gender,
                                clean_reason
                            ]
                        )

                        # Save the appointment
                        appointments = get_appointments()

                        appointment_id = next_record_id(
                            appointments
                        )

                        save_appointment_record(
                            appointment_id,
                            patient_id,
                            doctor,
                            appointment_date,
                            appointment_time,
                            "Upcoming"
                        )

                        st.success(
                            "Patient registered and appointment booked!"
                        )

                        st.info(
                            f"Patient ID: {patient_id}"
                        )

                        st.info(
                            f"Appointment ID: {appointment_id}"
                        )

                        st.rerun()

                else:
                    if patient_id is None:
                        st.error(
                            "Please register a patient first."
                        )

                    elif appointment_time is None:
                        st.error(
                            "Please select an available appointment time."
                        )

                    elif is_slot_booked(
                        doctor,
                        appointment_date,
                        appointment_time
                    ):
                        st.error(
                            "This time slot is already booked. "
                            "Please select another slot."
                        )

                    else:
                        appointments = get_appointments()

                        appointment_id = next_record_id(
                            appointments
                        )

                        save_appointment_record(
                            appointment_id,
                            patient_id,
                            doctor,
                            appointment_date,
                            appointment_time,
                            "Upcoming"
                        )

                        st.success(
                            "Appointment booked successfully!"
                        )

                        st.info(
                            f"Patient ID: {patient_id}"
                        )

                        st.info(
                            f"Appointment ID: {appointment_id}"
                        )

                        st.rerun()

    # ======================================
    # TAB 2: MANAGE APPOINTMENTS
    # ======================================

    with tab2:
        st.subheader("All Appointments")

        appointments = get_appointments()

        if not appointments:
            st.info("No appointments booked yet.")

        else:
            patient_names = {
                p[0]: p[1]
                for p in get_patients()
                if len(p) == 5
            }

            display_rows = []

            for a in appointments:
                display_rows.append({
                    "Appointment ID": a[0],
                    "Patient ID": a[1],
                    "Patient Name": patient_names.get(
                        a[1], "Unknown"
                    ),
                    "Doctor": a[2],
                    "Date": a[3],
                    "Time": a[4],
                    "Status": a[5]
                })

            st.dataframe(
                pd.DataFrame(display_rows),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### Update Appointment Status")

            selected_id = st.selectbox(
                "Select Appointment ID",
                [a[0] for a in appointments]
            )

            selected_appointment = next(
                a for a in appointments
                if a[0] == selected_id
            )

            statuses = [
                "Upcoming",
                "Completed",
                "Cancelled"
            ]

            current_status = (
                selected_appointment[5]
                if selected_appointment[5] in statuses
                else "Upcoming"
            )

            new_status = st.selectbox(
                "New Status",
                statuses,
                index=statuses.index(current_status)
            )

            if st.button(
                "Update Appointment Status",
                use_container_width=True
            ):
                updated_appointments = []

                for a in appointments:
                    if a[0] == selected_id:
                        a = list(a)
                        a[5] = new_status

                    updated_appointments.append(a)

                with open(
                    APPOINTMENT_FILE,
                    "w",
                    encoding="utf-8"
                ) as file:
                    for a in updated_appointments:
                        file.write(
                            "|".join(str(value) for value in a)
                            + "\n"
                        )

                st.success(
                    "Appointment status updated successfully!"
                )

                st.rerun()


# ==========================================
# 10. MEDICINE MANAGEMENT
# ==========================================

def medicine_management():
    heading(
        "Medicine Management",
        "Maintain a simple medicine inventory."
    )

    tab1, tab2 = st.tabs([
        "➕ Add Medicine",
        "💊 View Medicines"
    ])

    with tab1:
        with st.form("medicine_form", clear_on_submit=True):
            name = st.text_input("Medicine Name")

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=1
            )

            price = st.number_input(
                "Price per unit (₹)",
                min_value=0.0,
                value=10.0
            )

            submitted = st.form_submit_button("Save Medicine")

            if submitted:
                if not name.strip():
                    st.error("Please enter a medicine name.")
                else:
                    new_id = next_record_id(get_medicines())

                    save_record(
                        MEDICINE_FILE,
                        [new_id, name.strip(), quantity, price]
                    )

                    st.success("Medicine saved successfully.")
                    st.rerun()

    with tab2:
        medicines = get_medicines()

        if medicines:
            df = records_to_dataframe(
                medicines,
                ["Medicine ID", "Name", "Quantity", "Price (₹)"]
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            search = st.text_input("Search medicine")

            if search:
                matches = df[
                    df["Name"].str.contains(
                        search,
                        case=False,
                        na=False
                    )
                ]

                st.write("Search Results")

                st.dataframe(
                    matches,
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("No medicines found.")


# ==========================================
# 11. PATIENT PROFILE
# ==========================================

def patient_profile():
    patient_id = str(st.session_state.get("patient_id", "102"))
    patient = next((p for p in get_patients() if len(p)==5 and p[0]==patient_id), None)
    st.markdown("""
    <div class="hero-panel"><div class="hero-kicker">Patient space · Personal health</div>
    <div class="hero-title">Your health, all in one place</div>
    <div class="hero-copy">View your registered details and keep track of your care journey.</div></div>
    """, unsafe_allow_html=True)
    if patient:
        a,b = st.columns([1,2], gap="large")
        with a:
            st.markdown(f"<div class='info-panel'><div class='small'>Patient ID</div><div class='big'>#{patient[0]}</div><div class='hint'>Your unique patient reference</div></div>", unsafe_allow_html=True)
        with b:
            st.subheader(patient[1])
            st.caption("Registered patient profile")
            x,y = st.columns(2)
            with x:
                st.markdown(f"<div class='info-panel'><div class='small'>Age</div><div class='big'>{patient[2]}</div></div>", unsafe_allow_html=True)
            with y:
                st.markdown(f"<div class='info-panel'><div class='small'>Gender</div><div class='big'>{patient[3]}</div></div>", unsafe_allow_html=True)
            st.write("")
            st.markdown(f"<div class='info-panel'><div class='small'>Reason for visit</div><div class='big' style='font-size:18px'>{patient[4]}</div></div>", unsafe_allow_html=True)
    else:
        st.warning("Patient profile not found.")


# ==========================================
# 12. PATIENT APPOINTMENTS
# ==========================================

def patient_appointments():
    patient_id = str(st.session_state.get("patient_id", "102"))
    appointments = [a for a in get_appointments() if len(a)==6 and a[1]==patient_id]
    st.markdown("""
    <div class="hero-panel"><div class="hero-kicker">Patient space · Scheduling</div>
    <div class="hero-title">Appointments</div><div class="hero-copy">Review your bookings or schedule a visit with an available doctor.</div></div>
    """, unsafe_allow_html=True)
    upcoming = [a for a in appointments if a[5]=="Upcoming"]
    done = [a for a in appointments if a[5]=="Completed"]
    c1,c2,c3 = st.columns(3)
    c1.metric("Total bookings",len(appointments)); c2.metric("Upcoming",len(upcoming)); c3.metric("Completed",len(done))
    st.markdown("<div class='section-label'>YOUR BOOKINGS</div>",unsafe_allow_html=True)
    if appointments:
        df=records_to_dataframe(appointments,["Appointment ID","Patient ID","Doctor","Date","Time","Status"])
        st.dataframe(df.drop(columns=["Patient ID"]),use_container_width=True,hide_index=True)
    else:
        st.info("You do not have any appointments yet. Use the booking panel below to schedule your first visit.")
    st.markdown("<div class='section-label'>SCHEDULE A VISIT</div>",unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("Book a new appointment")
        with st.form("patient_booking_form",clear_on_submit=True):
            col1,col2=st.columns(2)
            with col1:
                doctor=st.selectbox("Choose doctor",list(DOCTOR_SCHEDULES.keys()))
            with col2:
                appointment_date=st.date_input("Choose date",min_value=date.today(),key="patient_appointment_date")
            available_slots=get_available_slots(doctor,appointment_date)
            appointment_time=st.selectbox("Available time",available_slots) if available_slots else None
            if not available_slots: st.warning("No slots are available for this doctor on the selected date.")
            submitted=st.form_submit_button("Confirm appointment",use_container_width=True)
            if submitted:
                if appointment_time is None: st.error("Choose a date with an available slot.")
                elif is_slot_booked(doctor,appointment_date,appointment_time): st.error("This slot is no longer available. Please try another date or time.")
                else:
                    new_id=next_record_id(get_appointments())
                    save_appointment_record(new_id,patient_id,doctor,appointment_date,appointment_time,"Upcoming")
                    st.success(f"Appointment booked successfully! ID: {new_id}")
                    st.rerun()


# ==========================================
# 13. SMART HEALTHCARE CHATBOT
# ==========================================

def healthcare_chatbot():
    st.subheader("🤖 Smart Healthcare Assistant")

    st.write(
        "Ask about your appointments, doctors, patient ID, "
        "or medicine inventory."
    )

    if "health_chat" not in st.session_state:
        st.session_state.health_chat = []

    # Read current saved records every time
    patients = get_patients()
    appointments = get_appointments()
    medicines = get_medicines()

    patient_id = str(st.session_state.get("patient_id", "102"))

    # Show previous conversation
    for message in st.session_state.health_chat:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input(
        "Ask about appointments, doctors, or medicines..."
    )

    if user_input:
        st.session_state.health_chat.append({
            "role": "user",
            "content": user_input
        })

        question = user_input.lower().strip()

        # Find the logged-in patient's records
        my_appointments = [
            a for a in appointments
            if len(a) == 6 and a[1] == patient_id
        ]

        my_patient = next(
            (
                p for p in patients
                if len(p) == 5 and p[0] == patient_id
            ),
            None
        )

        # 1. Appointment questions
        if any(word in question for word in [
            "appointment", "booked", "booking", "schedule"
        ]):

            if not my_appointments:
                reply = (
                    "You do not have any appointments recorded yet. "
                    "Open My Appointments to book one."
                )
            else:
                details = []

                for appointment in my_appointments:
                    details.append(
                        f"Appointment ID: {appointment[0]}\n"
                        f"Doctor: {appointment[2]}\n"
                        f"Date: {appointment[3]}\n"
                        f"Time: {appointment[4]}\n"
                        f"Status: {appointment[5]}"
                    )

                reply = (
                    "Here are your saved appointments:\n\n"
                    + "\n\n".join(details)
                )

        # 2. Doctor availability questions
        elif any(word in question for word in [
            "doctor", "doctors", "available", "availability"
        ]):

            doctors = [
                "Dr. Sharma",
                "Dr. Patel",
                "Dr. Deshmukh"
            ]

            # If a doctor and date/time are requested, check
            # existing appointment conflicts for the selected slot.
            requested_doctor = next(
                (
                    doctor for doctor in doctors
                    if doctor.lower() in question
                ),
                None
            )

            if requested_doctor:
                requested_date = next(
                    (
                        token for token in question.replace(",", " ").split()
                        if len(token) == 10
                        and token[4] == "-"
                        and token[7] == "-"
                    ),
                    None
                )

                requested_time = next(
                    (
                        time for time in [
                            "09:00 AM", "10:00 AM", "11:00 AM",
                            "12:00 PM", "02:00 PM", "03:00 PM",
                            "04:00 PM"
                        ]
                        if time.lower() in question
                    ),
                    None
                )

                if requested_date and requested_time:
                    conflict = any(
                        len(a) == 6
                        and a[2] == requested_doctor
                        and a[5] != "Cancelled"
                        and a[3] == requested_date
                        and a[4] == requested_time
                        for a in appointments
                    )

                    if conflict:
                        reply = (
                            f"{requested_doctor} already has an "
                            f"appointment on {requested_date} at "
                            f"{requested_time}. Please choose another slot."
                        )
                    else:
                        reply = (
                            f"No appointment is recorded for "
                            f"{requested_doctor} on {requested_date} "
                            f"at {requested_time}. However, this demo "
                            "does not have a real doctor duty roster, "
                            "so availability is not guaranteed."
                        )
                else:
                    reply = (
                        f"{requested_doctor} is configured in this demo. "
                        "To check a specific slot, ask with a date in "
                        "YYYY-MM-DD format and a time such as 10:00 AM. "
                        "Actual duty availability is not connected."
                    )
            else:
                reply = (
                    "Doctors configured in this demo:\n"
                    + "\n".join(f"- {doctor}" for doctor in doctors)
                    + "\n\nTheir real-time duty availability is not "
                    "connected to this application yet."
                )

        # 3. Patient ID
        elif "patient id" in question or "my id" in question:
            reply = f"Your patient ID is {patient_id}."

        # 4. Patient profile
        elif any(word in question for word in [
            "my profile", "my details", "my information"
        ]):

            if my_patient:
                reply = (
                    f"Name: {my_patient[1]}\n"
                    f"Patient ID: {my_patient[0]}\n"
                    f"Age: {my_patient[2]}\n"
                    f"Gender: {my_patient[3]}"
                )
            else:
                reply = "Your patient profile could not be found."

        # 5. Medicine inventory
        elif any(word in question for word in [
            "medicine", "medicines", "stock", "paracetamol"
        ]):

            search_term = question

            if "paracetamol" in question:
                search_term = "paracetamol"

            matches = [
                medicine for medicine in medicines
                if len(medicine) == 4
                and (
                    search_term == question
                    or search_term in medicine[1].lower()
                )
            ]

            if matches:
                reply = "Medicine inventory:\n\n" + "\n\n".join(
                    (
                        f"Name: {medicine[1]}\n"
                        f"Quantity: {medicine[2]}\n"
                        f"Price: ₹{medicine[3]} per unit"
                    )
                    for medicine in matches
                )
            else:
                reply = "No matching medicine was found in inventory."

        # 6. Greeting
        elif any(word in question for word in [
            "hello", "hi", "hey"
        ]):
            reply = (
                "Hello! I can check your saved appointments, "
                "show configured doctors, look up medicine stock, "
                "and display your patient ID."
            )

        # 7. Help
        elif "help" in question or "what can you do" in question:
            reply = (
                "You can ask questions such as:\n\n"
                "- When is my appointment?\n"
                "- Have I booked an appointment?\n"
                "- Is Dr. Sharma available on 2026-11-02 at 10:00 AM?\n"
                "- What is my patient ID?\n"
                "- Is Paracetamol available?\n"
                "- Show my profile."
            )

        else:
            reply = (
                "I couldn't match that question to the available "
                "records. Try asking about appointments, doctors, "
                "patient ID, or medicine inventory."
            )

        st.session_state.health_chat.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()

    if st.button("Clear Chat"):
        st.session_state.health_chat = []
        st.rerun()


# ==========================================
# 14. VOICE HEALTHCARE ASSISTANT
# ==========================================

def voice_healthcare_bot():
    st.subheader("🎙️ Voice Healthcare Assistant")
    st.write("Record a question about your appointments, doctors, or medicines.")
    st.info("Voice recognition needs the SpeechRecognition package and an internet connection for Google speech recognition.")
    audio = st.audio_input("Record your question")
    if audio is not None:
        if st.button("Convert speech to text and answer", key="voice_process"):
            try:
                import speech_recognition as sr
                import io
                recognizer = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio.getvalue())) as source:
                    recorded_audio = recognizer.record(source)
                question = recognizer.recognize_google(recorded_audio)
                st.write("**You said:**", question)
                q = question.lower()
                answer = "I can help with appointment status, doctor schedules, and medicine stock. Please ask a more specific question."
                pid = str(st.session_state.get("patient_id", "102"))
                appointments = get_appointments()
                if any(word in q for word in ["appointment", "booking", "booked", "status"]):
                    mine = [a for a in appointments if len(a) >= 6 and str(a[1]) == pid and a[5].lower() != "cancelled"]
                    if mine:
                        answer = "Your appointments: " + "; ".join(f"{a[2]} on {a[3]} at {a[4]}, status {a[5]}" for a in mine)
                    else:
                        answer = "I could not find an active appointment for your patient ID."
                elif "doctor" in q or "available" in q:
                    answer = "Configured doctors are " + ", ".join(DOCTOR_SCHEDULES.keys()) + ". Availability depends on the selected date and open slots shown in My Appointments."
                elif "medicine" in q or "paracetamol" in q or "stock" in q:
                    meds = get_medicines()
                    matches = [m for m in meds if any(word in m[1].lower() for word in q.split() if len(word) > 3)]
                    answer = "; ".join(f"{m[1]}: quantity {m[2]}, price ₹{m[3]}" for m in matches) if matches else "I could not find a matching medicine in the inventory."
                st.success(answer)
                try:
                    from gtts import gTTS
                    import tempfile
                    import os
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                        audio_path = tmp.name
                    gTTS(text=answer, lang="en").save(audio_path)
                    with open(audio_path, "rb") as f:
                        st.audio(f.read(), format="audio/mp3")
                    os.remove(audio_path)
                except Exception:
                    st.caption("Spoken response unavailable. Read the text answer above.")
            except ImportError:
                st.error("Install the voice packages first: pip install SpeechRecognition gTTS")
            except Exception as exc:
                st.error(f"Could not process the recording: {exc}. Please try recording again.")


# ==========================================
# 14. WEBCAM FACE DETECTION
# ==========================================

def face_detection():
    st.subheader("📷 Face Detection")

    st.write(
        "Take a picture with your webcam to check "
        "whether a face is visible."
    )

    if not FACE_MODEL.exists():
        st.error(
            "Face detection model not found. Save "
            "haarcascade_frontalface_default.xml "
            "in the same folder as app.py."
        )

        st.markdown(
            "[Download the OpenCV face detection model]"
            "(https://raw.githubusercontent.com/opencv/opencv/master/"
            "data/haarcascades/haarcascade_frontalface_default.xml)"
        )
        return

    # Check that the required OpenCV function exists
    if not hasattr(cv2, "CascadeClassifier"):
        st.error(
            "Your OpenCV installation does not include "
            "CascadeClassifier. Check your OpenCV installation."
        )
        return

    face_cascade = cv2.CascadeClassifier(str(FACE_MODEL))

    if face_cascade.empty():
        st.error("The face detection model could not be loaded.")
        return

    image_file = st.camera_input("Take a picture")

    if image_file is not None:
        image_bytes = image_file.getvalue()

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR
        )

        if image is None:
            st.error("Could not read the captured image.")
            return

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        if len(faces) > 0:
            st.success(f"Detected {len(faces)} face(s)!")
        else:
            st.warning("No face detected. Try taking another picture.")

        image_rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        st.image(
            image_rgb,
            caption="Face Detection Result",
            use_container_width=True
        )

    st.caption(
        "This feature detects faces in a photo. It does not "
        "identify people or diagnose medical conditions."
    )


# ==========================================
# 15. DOCTOR DASHBOARD
# ==========================================

def doctor_dashboard():
    with st.sidebar:
        st.markdown("<div style='font-size:12px;letter-spacing:2px;color:#55d9eb;font-weight:800'>AI SMART HEALTHCARE</div><h2 style='margin-top:4px'>CareDesk</h2>",unsafe_allow_html=True)
        st.caption("DOCTOR WORKSPACE")
        st.divider()
        selected_page=st.radio("WORKSPACE",["Overview","Patients","Appointments","Medicines"],label_visibility="collapsed",key="doctor_navigation")
        st.divider()
        st.caption("Signed in as Doctor")
        if st.button("↪  Log out",use_container_width=True):
            st.session_state.clear(); st.rerun()
    if selected_page=="Overview": doctor_overview()
    elif selected_page=="Patients": patient_management()
    elif selected_page=="Appointments": appointment_management()
    elif selected_page=="Medicines": medicine_management()


# ==========================================
# 16. PATIENT DASHBOARD
# ==========================================

def patient_dashboard():
    with st.sidebar:
        st.markdown("<div style='font-size:12px;letter-spacing:2px;color:#55d9eb;font-weight:800'>AI SMART HEALTHCARE</div><h2 style='margin-top:4px'>CareDesk</h2>",unsafe_allow_html=True)
        st.caption("PATIENT PORTAL")
        st.divider()
        selected_page=st.radio("YOUR HEALTH",["My Profile","My Appointments","Healthcare Assistant","Voice Bot","Face Detection"],label_visibility="collapsed",key="patient_navigation")
        st.divider()
        st.caption("Your personal healthcare space")
        if st.button("↪  Log out",use_container_width=True):
            st.session_state.clear(); st.rerun()
    if selected_page=="My Profile": patient_profile()
    elif selected_page=="My Appointments": patient_appointments()
    elif selected_page=="Healthcare Assistant":
        st.markdown("<div class='hero-panel'><div class='hero-kicker'>Patient tools · Chat support</div><div class='hero-title'>Healthcare Assistant</div><div class='hero-copy'>Ask about your saved appointments, configured doctors, patient ID and medicine inventory.</div></div>",unsafe_allow_html=True)
        healthcare_chatbot()
    elif selected_page=="Voice Bot":
        st.markdown("<div class='hero-panel'><div class='hero-kicker'>Patient tools · Voice support</div><div class='hero-title'>Voice Assistant</div><div class='hero-copy'>Speak a question and hear a response from your demo healthcare records.</div></div>",unsafe_allow_html=True)
        voice_healthcare_bot()
    elif selected_page=="Face Detection":
        st.markdown("<div class='hero-panel'><div class='hero-kicker'>Patient tools · Camera</div><div class='hero-title'>Face Detection</div><div class='hero-copy'>Use your webcam to detect a visible face in a captured image.</div></div>",unsafe_allow_html=True)
        face_detection()


# ==========================================
# 17. MAIN FUNCTION
# ==========================================

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()

    elif st.session_state.role == "Doctor":
        doctor_dashboard()

    elif st.session_state.role == "Patient":
        patient_dashboard()

    else:
        st.session_state.clear()
        st.rerun()


# ==========================================
# 18. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()
