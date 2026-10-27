#include <stdio.h>
#include <string.h>

#define MAX_PATIENTS 100
#define MAX_APPOINTMENTS 100
#define MAX_MEDICINES 100
#define MAX_EMERGENCY 100

/* ================= STRUCTURES ================= */

struct Patient {
    int id;
    char name[50];
    int age;
    char gender[10];
    char disease[50];
};

struct Appointment {
    int appointmentId;
    int patientId;
    char doctorName[50];
    char date[20];
    char time[10];
};

struct Medicine {
    int medicineId;
    char name[50];
    int quantity;
    float price;
};

/* ================= GLOBAL VARIABLES ================= */

struct Patient patients[MAX_PATIENTS];
int patientCount = 0;

struct Appointment appointments[MAX_APPOINTMENTS];
int appointmentCount = 0;

struct Medicine medicines[MAX_MEDICINES];
int medicineCount = 0;

int emergencyQueue[MAX_EMERGENCY];
int front = 0;
int rear = -1;
int emergencyCount = 0;

/* ================= PATIENT MANAGEMENT ================= */

void addPatient() {
    if (patientCount >= MAX_PATIENTS) {
        printf("\nPatient storage is full!\n");
        return;
    }

    struct Patient *p = &patients[patientCount];

    p->id = patientCount + 1;

    printf("\nEnter patient name: ");
    scanf(" %49[^\n]", p->name);

    printf("Enter age: ");
    if (scanf("%d", &p->age) != 1 || p->age < 0) {
        printf("Invalid age.\n");
        return;
    }

    printf("Enter gender: ");
    scanf(" %9[^\n]", p->gender);

    printf("Enter disease or health problem: ");
    scanf(" %49[^\n]", p->disease);

    patientCount++;

    printf("\nPatient registered successfully!\n");
    printf("Patient ID: %d\n", p->id);
}

void displayPatients() {
    int i;

    if (patientCount == 0) {
        printf("\nNo patient records found.\n");
        return;
    }

    printf("\n========== PATIENT RECORDS ==========\n");

    for (i = 0; i < patientCount; i++) {
        printf("\nPatient ID: %d\n", patients[i].id);
        printf("Name: %s\n", patients[i].name);
        printf("Age: %d\n", patients[i].age);
        printf("Gender: %s\n", patients[i].gender);
        printf("Disease: %s\n", patients[i].disease);
    }
}

/* ================= SEARCH PATIENT BY ID ================= */

void searchPatientById() {
    int searchId;
    int i;
    int found = 0;

    printf("\n========== SEARCH PATIENT ==========\n");
    printf("Enter Patient ID: ");

    if (scanf("%d", &searchId) != 1) {
        printf("Invalid input. Enter a numeric ID.\n");
        return;
    }

    for (i = 0; i < patientCount; i++) {
        if (patients[i].id == searchId) {
            printf("\nPatient Found!\n");
            printf("----------------------------\n");
            printf("Patient ID : %d\n", patients[i].id);
            printf("Name       : %s\n", patients[i].name);
            printf("Age        : %d\n", patients[i].age);
            printf("Gender     : %s\n", patients[i].gender);
            printf("Disease    : %s\n", patients[i].disease);
            printf("----------------------------\n");

            found = 1;
            break;
        }
    }

    if (!found) {
        printf("\nPatient with ID %d was not found.\n", searchId);
    }
}

/* ================= APPOINTMENT MANAGEMENT ================= */

void bookAppointment() {
    int patientId;
    int i;
    int found = 0;

    if (appointmentCount >= MAX_APPOINTMENTS) {
        printf("\nAppointment storage is full!\n");
        return;
    }

    if (patientCount == 0) {
        printf("\nRegister a patient before booking an appointment.\n");
        return;
    }

    printf("\nEnter patient ID: ");
    if (scanf("%d", &patientId) != 1) {
        printf("Invalid patient ID.\n");
        return;
    }

    for (i = 0; i < patientCount; i++) {
        if (patients[i].id == patientId) {
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("Patient ID not found.\n");
        return;
    }

    struct Appointment *a = &appointments[appointmentCount];

    a->appointmentId = appointmentCount + 1;
    a->patientId = patientId;

    printf("Enter doctor name: ");
    scanf(" %49[^\n]", a->doctorName);

    printf("Enter appointment date (DD-MM-YYYY): ");
    scanf(" %19[^\n]", a->date);

    printf("Enter appointment time: ");
    scanf(" %9[^\n]", a->time);

    appointmentCount++;

    printf("\nAppointment booked successfully!\n");
    printf("Appointment ID: %d\n", a->appointmentId);
}

void displayAppointments() {
    int i;

    if (appointmentCount == 0) {
        printf("\nNo appointments found.\n");
        return;
    }

    printf("\n========== APPOINTMENTS ==========\n");

    for (i = 0; i < appointmentCount; i++) {
        printf("\nAppointment ID: %d\n",
               appointments[i].appointmentId);
        printf("Patient ID: %d\n",
               appointments[i].patientId);
        printf("Doctor: %s\n",
               appointments[i].doctorName);
        printf("Date: %s\n",
               appointments[i].date);
        printf("Time: %s\n",
               appointments[i].time);
    }
}

/* ================= SAVE APPOINTMENTS ================= */

void saveAppointments() {
    FILE *fp;
    int i;

    fp = fopen("appointments.txt", "w");

    if (fp == NULL) {
        printf("Error saving appointment records.\n");
        return;
    }

    for (i = 0; i < appointmentCount; i++) {
        fprintf(fp, "%d|%d|%s|%s|%s\n",
                appointments[i].appointmentId,
                appointments[i].patientId,
                appointments[i].doctorName,
                appointments[i].date,
                appointments[i].time);
    }

    fclose(fp);
    printf("Appointment records saved successfully!\n");
}

void loadAppointments() {
    FILE *fp;

    fp = fopen("appointments.txt", "r");

    if (fp == NULL) {
        printf("No saved appointment records found yet.\n");
        return;
    }

    appointmentCount = 0;

    while (appointmentCount < MAX_APPOINTMENTS &&
           fscanf(fp, "%d|%d|%49[^|]|%19[^|]|%9[^\n]\n",
                  &appointments[appointmentCount].appointmentId,
                  &appointments[appointmentCount].patientId,
                  appointments[appointmentCount].doctorName,
                  appointments[appointmentCount].date,
                  appointments[appointmentCount].time) == 5) {
        appointmentCount++;
    }

    fclose(fp);
    printf("%d appointment record(s) loaded.\n", appointmentCount);
}

/* ================= EMERGENCY QUEUE ================= */

void addEmergencyPatient() {
    int patientId;
    int i;
    int found = 0;

    if (emergencyCount >= MAX_EMERGENCY) {
        printf("\nEmergency queue is full!\n");
        return;
    }

    if (patientCount == 0) {
        printf("\nRegister a patient first.\n");
        return;
    }

    printf("\nEnter patient ID: ");
    if (scanf("%d", &patientId) != 1) {
        printf("Invalid patient ID.\n");
        return;
    }

    for (i = 0; i < patientCount; i++) {
        if (patients[i].id == patientId) {
            found = 1;
            break;
        }
    }

    if (!found) {
        printf("Patient ID not found.\n");
        return;
    }

    rear = (rear + 1) % MAX_EMERGENCY;
    emergencyQueue[rear] = patientId;
    emergencyCount++;

    printf("Patient added to emergency queue.\n");
}

void serveEmergencyPatient() {
    if (emergencyCount == 0) {
        printf("\nNo emergency patients waiting.\n");
        return;
    }

    printf("\nServing emergency patient ID: %d\n",
           emergencyQueue[front]);

    front = (front + 1) % MAX_EMERGENCY;
    emergencyCount--;

    if (emergencyCount == 0) {
        front = 0;
        rear = -1;
    }

    printf("Patient removed from the queue.\n");
}

void displayEmergencyQueue() {
    int i;
    int index;

    if (emergencyCount == 0) {
        printf("\nEmergency queue is empty.\n");
        return;
    }

    printf("\n========== EMERGENCY QUEUE ==========\n");

    for (i = 0; i < emergencyCount; i++) {
        index = (front + i) % MAX_EMERGENCY;

        printf("Position %d: Patient ID %d\n",
               i + 1, emergencyQueue[index]);
    }
}

/* ================= MEDICINE MANAGEMENT ================= */

void addMedicine() {
    if (medicineCount >= MAX_MEDICINES) {
        printf("\nMedicine storage is full!\n");
        return;
    }

    struct Medicine *m = &medicines[medicineCount];

    m->medicineId = medicineCount + 1;

    printf("\nEnter medicine name: ");
    scanf(" %49[^\n]", m->name);

    printf("Enter quantity: ");
    if (scanf("%d", &m->quantity) != 1 || m->quantity < 0) {
        printf("Invalid quantity.\n");
        return;
    }

    printf("Enter price: ");
    if (scanf("%f", &m->price) != 1 || m->price < 0) {
        printf("Invalid price.\n");
        return;
    }

    medicineCount++;

    printf("\nMedicine added successfully!\n");
    printf("Medicine ID: %d\n", m->medicineId);
}

void displayMedicines() {
    int i;

    if (medicineCount == 0) {
        printf("\nNo medicines found.\n");
        return;
    }

    printf("\n========== MEDICINE LIST ==========\n");

    for (i = 0; i < medicineCount; i++) {
        printf("\nMedicine ID: %d\n", medicines[i].medicineId);
        printf("Name: %s\n", medicines[i].name);
        printf("Quantity: %d\n", medicines[i].quantity);
        printf("Price: %.2f\n", medicines[i].price);
    }
}

void searchMedicine() {
    char searchName[50];
    int i;
    int found = 0;

    printf("\nEnter medicine name to search: ");
    scanf(" %49[^\n]", searchName);

    for (i = 0; i < medicineCount; i++) {
        if (strcmp(medicines[i].name, searchName) == 0) {
            printf("\nMedicine found!\n");
            printf("ID: %d\n", medicines[i].medicineId);
            printf("Name: %s\n", medicines[i].name);
            printf("Quantity: %d\n", medicines[i].quantity);
            printf("Price: %.2f\n", medicines[i].price);
            found = 1;
        }
    }

    if (!found) {
        printf("\nMedicine not found.\n");
    }
}

void updateMedicineStock() {
    int id;
    int newQuantity;
    int i;

    printf("\nEnter medicine ID: ");
    if (scanf("%d", &id) != 1) {
        printf("Invalid medicine ID.\n");
        return;
    }

    for (i = 0; i < medicineCount; i++) {
        if (medicines[i].medicineId == id) {
            printf("Medicine: %s\n", medicines[i].name);
            printf("Current quantity: %d\n", medicines[i].quantity);
            printf("Enter new quantity: ");

            if (scanf("%d", &newQuantity) != 1 ||
                newQuantity < 0) {
                printf("Invalid quantity.\n");
                return;
            }

            medicines[i].quantity = newQuantity;
            printf("Medicine stock updated successfully!\n");
            return;
        }
    }

    printf("Medicine ID not found.\n");
}

void saveMedicines() {
    FILE *fp;
    int i;

    fp = fopen("medicines.txt", "w");

    if (fp == NULL) {
        printf("Error saving medicine records.\n");
        return;
    }

    for (i = 0; i < medicineCount; i++) {
        fprintf(fp, "%d|%s|%d|%.2f\n",
                medicines[i].medicineId,
                medicines[i].name,
                medicines[i].quantity,
                medicines[i].price);
    }

    fclose(fp);
    printf("Medicine records saved successfully!\n");
}

void loadMedicines() {
    FILE *fp;

    fp = fopen("medicines.txt", "r");

    if (fp == NULL) {
        printf("No saved medicine records found yet.\n");
        return;
    }

    medicineCount = 0;

    while (medicineCount < MAX_MEDICINES &&
           fscanf(fp, "%d|%49[^|]|%d|%f\n",
                  &medicines[medicineCount].medicineId,
                  medicines[medicineCount].name,
                  &medicines[medicineCount].quantity,
                  &medicines[medicineCount].price) == 4) {
        medicineCount++;
    }

    fclose(fp);
    printf("%d medicine record(s) loaded.\n", medicineCount);
}

/* ================= PATIENT FILE STORAGE ================= */

void savePatients() {
    FILE *fp;
    int i;

    fp = fopen("patients.txt", "w");

    if (fp == NULL) {
        printf("Error saving patient records.\n");
        return;
    }

    for (i = 0; i < patientCount; i++) {
        fprintf(fp, "%d|%s|%d|%s|%s\n",
                patients[i].id,
                patients[i].name,
                patients[i].age,
                patients[i].gender,
                patients[i].disease);
    }

    fclose(fp);
    printf("Patient records saved successfully!\n");
}

void loadPatients() {
    FILE *fp;

    fp = fopen("patients.txt", "r");

    if (fp == NULL) {
        printf("No saved patient records found yet.\n");
        return;
    }

    patientCount = 0;

    while (patientCount < MAX_PATIENTS &&
           fscanf(fp, "%d|%49[^|]|%d|%9[^|]|%49[^\n]",
                  &patients[patientCount].id,
                  patients[patientCount].name,
                  &patients[patientCount].age,
                  patients[patientCount].gender,
                  patients[patientCount].disease) == 5) {
        patientCount++;
    }

    fclose(fp);
    printf("%d patient record(s) loaded.\n", patientCount);
}

/* ================= HEALTH ASSISTANT ================= */

void healthAssistant() {
    int choice;

    printf("\n========== HEALTH ASSISTANT ==========\n");
    printf("1. Healthy eating\n");
    printf("2. Exercise\n");
    printf("3. Sleep\n");
    printf("4. General health advice\n");
    printf("Enter your choice: ");

    if (scanf("%d", &choice) != 1) {
        printf("Invalid input.\n");
        return;
    }

    switch (choice) {
        case 1:
            printf("\nEat a balanced diet containing fruits, "
                   "vegetables, whole grains and protein.\n");
            printf("Drink enough water.\n");
            break;

        case 2:
            printf("\nChoose regular physical activity suitable "
                   "for your fitness level.\n");
            break;

        case 3:
            printf("\nMaintain a regular sleep schedule and "
                   "reduce screen use before bedtime.\n");
            break;

        case 4:
            printf("\nConsult a qualified healthcare professional "
                   "for personal medical advice.\n");
            printf("For emergencies, contact local emergency services.\n");
            break;

        default:
            printf("Invalid choice.\n");
    }
}

/* ================= MEDICINE SUBMENU ================= */

void medicineMenu() {
    int choice;

    do {
        printf("\n========== MEDICINE MANAGEMENT ==========\n");
        printf("1. Add Medicine\n");
        printf("2. View Medicines\n");
        printf("3. Search Medicine\n");
        printf("4. Update Medicine Stock\n");
        printf("5. Save Medicines\n");
        printf("6. Return to Main Menu\n");
        printf("Enter your choice: ");

        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Restart the application.\n");
            return;
        }

        switch (choice) {
            case 1: addMedicine(); break;
            case 2: displayMedicines(); break;
            case 3: searchMedicine(); break;
            case 4: updateMedicineStock(); break;
            case 5: saveMedicines(); break;
            case 6: printf("Returning to main menu...\n"); break;
            default: printf("Enter a number from 1 to 6.\n");
        }

    } while (choice != 6);
}

/* ================= MAIN FUNCTION ================= */

int main() {
    int choice;

    printf("\n====================================\n");
    printf("      AI SMART HEALTHCARE APP\n");
    printf("====================================\n");

    printf("\nLoading saved records...\n");
    loadPatients();
    loadMedicines();
    loadAppointments();

    do {
        printf("\n====================================\n");
        printf("      AI SMART HEALTHCARE APP\n");
        printf("====================================\n");
        printf("1. Register Patient\n");
        printf("2. View All Patients\n");
        printf("3. Book Appointment\n");
        printf("4. View Appointments\n");
        printf("5. Add Emergency Patient\n");
        printf("6. Serve Next Emergency Patient\n");
        printf("7. View Emergency Queue\n");
        printf("8. Medicine Management\n");
        printf("9. Health Assistant\n");
        printf("10. Exit\n");
        printf("11. Save Patient Records\n");
        printf("12. Save Appointment Records\n");
        printf("13. Search Patient by ID\n");
        printf("====================================\n");
        printf("Enter your choice: ");

        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Restart the application.\n");
            break;
        }

        switch (choice) {
            case 1:
                addPatient();
                break;

            case 2:
                displayPatients();
                break;

            case 3:
                bookAppointment();
                break;

            case 4:
                displayAppointments();
                break;

            case 5:
                addEmergencyPatient();
                break;

            case 6:
                serveEmergencyPatient();
                break;

            case 7:
                displayEmergencyQueue();
                break;

            case 8:
                medicineMenu();
                break;

            case 9:
                healthAssistant();
                break;

            case 10:
                savePatients();
                saveMedicines();
                saveAppointments();
                printf("\nExiting AI Smart Healthcare App.\n");
                break;

            case 11:
                savePatients();
                break;

            case 12:
                saveAppointments();
                break;

            case 13:
                searchPatientById();
                break;

            default:
                printf("Invalid choice. Enter a number from 1 to 13.\n");
        }

    } while (choice != 10);

    return 0;
}