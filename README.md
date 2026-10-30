# 🏥 AI Smart Healthcare System

## 📌 Project Overview
AI Smart Healthcare is an educational healthcare management project designed to make basic healthcare services more accessible and organized.

The project contains two components:

- **Python Streamlit Web Application:** Provides a web-based healthcare interface with patient and doctor features, appointment management, medicine management, a health assistant, voice interaction, and face detection.
- **C Programming Application:** Demonstrates Data Structures and Algorithms through patient management, appointment booking, emergency patient handling, and medicine management.

> Note: The C application and Python web application are separate components in this repository. They are not described as directly integrated.

## ✨ Features

### Python Web Application
- Patient and doctor interface
- Appointment management
- Medicine management
- Healthcare chatbot
- Voice assistant
- Face detection using OpenCV

### C Programming Application
- Register and view patients
- Book and view appointments
- Emergency patient queue
- Medicine management
- Search medicine
- Basic health assistant

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| C | Healthcare management and DSA |
| Python | Application development |
| Streamlit | Web interface |
| OpenCV | Face detection |
| SpeechRecognition | Voice input |
| gTTS | Text-to-speech |
| Git and GitHub | Version control |

## 📂 Project Structure

```text
AI-Smart-Healthcare/
│
├── app.py
├── main.c
├── requirements.txt
├── build.sh
├── haarcascade_frontalface_default.xml
├── api/
└── .gitignore
```

*The `api/` folder may contain additional project files.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mujmulesam-max/AI-Smart-Healthcare.git
```

### 2. Open the Project Folder

```bash
cd AI-Smart-Healthcare
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Python Web Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 💻 Run the C Program

Make sure GCC is installed.

Compile:

```bash
gcc main.c -o healthcare.exe
```

Run on Windows:

```bash
.\healthcare.exe
```

## 🧠 Data Structures and Algorithms Used

- Structures (`struct`) for organizing patient, appointment, and medicine information.
- Arrays for storing records.
- Queue for emergency patient management.
- Searching techniques for locating records.
- File handling for storing information.

## 🎯 Project Objectives

- Develop a basic healthcare management application.
- Understand practical applications of C programming and DSA.
- Explore Python-based web application development.
- Demonstrate basic voice interaction and face detection.
- Improve understanding of software development and project organization.

## 🚀 Future Enhancements

- Connect the C and Python components through an API.
- Add a secure database.
- Improve authentication and authorization.
- Add online appointment notifications.
- Improve the healthcare assistant with medically validated information.
- Deploy the application for online access.

- ## 📸 Project Screenshots

### Login Page
<img width="1087" height="807" alt="login png" src="https://github.com/user-attachments/assets/ac14ce7b-420e-4b17-823e-7aeb7a2d70be" />

### Dashboard
<img width="1865" height="831" alt="dashboard png" src="https://github.com/user-attachments/assets/17c4ec52-07fb-49f5-9939-febd3d6ade4e" />

### Appointment Management
<img width="1861" height="827" alt="appointments png" src="https://github.com/user-attachments/assets/4face3e9-efc8-410d-96f6-a32a7b5389f4" />

### Healthcare Assistant
<img width="1532" height="762" alt="healthcare-assistant png" src="https://github.com/user-attachments/assets/01238745-55b3-47c4-aad9-4e31bc57bc0e" />

## ⚠️ Disclaimer

This project is developed for educational purposes. It is not a substitute for professional medical advice, diagnosis, or treatment. Face detection is not identity verification.

## 👩‍💻 Author
prepared by- Samiksha Mujmule
             Siddhi Pawar

**College:** Nutan Maharashtra Institute of Engineering and Technology

**Project:** AI Smart Healthcare System

