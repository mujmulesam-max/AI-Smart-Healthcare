
#!/usr/bin/env bash
set -e

gcc api/patient_api.c -o api/patient_api
chmod +x api/patient_api
