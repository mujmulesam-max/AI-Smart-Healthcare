
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <ctype.h>

#define MAX_PATIENTS 100

struct Patient {
    int id;
    char name[50];
    int age;
    char gender[10];
    char disease[50];
};

struct Patient patients[MAX_PATIENTS];
int patientCount = 0;

int loadPatients(void) {
    FILE *fp = fopen("patients.txt", "r");
    if (fp == NULL) return 1;

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
    return 1;
}

int savePatients(void) {
    FILE *fp = fopen("patients.txt", "w");
    if (fp == NULL) return 0;

    for (int i = 0; i < patientCount; i++) {
        if (fprintf(fp, "%d|%s|%d|%s|%s\n",
                    patients[i].id,
                    patients[i].name,
                    patients[i].age,
                    patients[i].gender,
                    patients[i].disease) < 0) {
            fclose(fp);
            return 0;
        }
    }

    return fclose(fp) == 0;
}

int safeField(const char *s, size_t maxLen) {
    size_t n = strlen(s);
    if (n == 0 || n >= maxLen) return 0;

    for (size_t i = 0; i < n; i++) {
        if (s[i] == '|' || s[i] == '\n' || s[i] == '\r')
            return 0;
    }
    return 1;
}

int parsePositiveInt(const char *s, int *out) {
    char *end;
    long value = strtol(s, &end, 10);

    if (s[0] == '\0' || *end != '\0' ||
        value <= 0 || value > INT_MAX) return 0;

    *out = (int)value;
    return 1;
}

int main(int argc, char *argv[]) {
    if (!loadPatients()) {
        fprintf(stderr, "Could not load patient records.\n");
        return 1;
    }

    if (argc == 3 && strcmp(argv[1], "search") == 0) {
        int searchId;

        if (!parsePositiveInt(argv[2], &searchId)) {
            fprintf(stderr, "Invalid patient ID.\n");
            return 2;
        }

        for (int i = 0; i < patientCount; i++) {
            if (patients[i].id == searchId) {
                printf("{\"found\":true,\"id\":%d,"
                       "\"name\":\"%s\",\"age\":%d,"
                       "\"gender\":\"%s\",\"disease\":\"%s\"}\n",
                       patients[i].id, patients[i].name,
                       patients[i].age, patients[i].gender,
                       patients[i].disease);
                return 0;
            }
        }

        printf("{\"found\":false}\n");
        return 0;
    }

    if (argc == 6 && strcmp(argv[1], "add") == 0) {
        int age;

        if (patientCount >= MAX_PATIENTS) {
            fprintf(stderr, "Patient storage is full.\n");
            return 3;
        }

        if (!safeField(argv[2], sizeof(patients[0].name)) ||
            !safeField(argv[4], sizeof(patients[0].gender)) ||
            !safeField(argv[5], sizeof(patients[0].disease)) ||
            !parsePositiveInt(argv[3], &age) || age > 150) {
            fprintf(stderr, "Invalid patient fields.\n");
            return 2;
        }

        int maxId = 0;
        for (int i = 0; i < patientCount; i++) {
            if (patients[i].id > maxId) maxId = patients[i].id;
        }

        if (maxId == INT_MAX) {
            fprintf(stderr, "No patient IDs remain.\n");
            return 3;
        }

        struct Patient p;
        p.id = maxId + 1;
        p.age = age;

        strcpy(p.name, argv[2]);
        strcpy(p.gender, argv[4]);
        strcpy(p.disease, argv[5]);

        /* Save through a temporary file before replacing records. */
        patients[patientCount] = p;
        patientCount++;

        if (!savePatients()) {
            patientCount--;
            fprintf(stderr, "Could not save patient records.\n");
            return 4;
        }

        printf("{\"created\":true,\"id\":%d}\n", p.id);
        return 0;
    }

    printf("Patient records loaded: %d\n", patientCount);
    printf("Commands: search ID | add NAME AGE GENDER DISEASE\n");
    return 0;
}
