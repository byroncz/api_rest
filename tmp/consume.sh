#!/bin/bash
# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/departments.csv \
#     --data-urlencode "Tabla=departments" \
#     https://isrxz9drcd.execute-api.us-east-2.amazonaws.com/prod/  


# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/jobs.csv \
#     --data-urlencode "Tabla=jobs" \
#     https://isrxz9drcd.execute-api.us-east-2.amazonaws.com/prod/  


# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/hired_employees_0.csv \
#     --data-urlencode "Tabla=hired_employees" \
#     https://isrxz9drcd.execute-api.us-east-2.amazonaws.com/prod/  

# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/hired_employees_1.csv \
#     --data-urlencode "Tabla=hired_employees" \
#     https://isrxz9drcd.execute-api.us-east-2.amazonaws.com/prod/  


curl -X GET \
    -H "Content-Type: text/csv; charset=utf-8" \
    --data-urlencode "Requirements=employees" \
    https://isrxz9drcd.execute-api.us-east-2.amazonaws.com/prod/  

curl -X GET \
    -H "Content-Type: text/csv; charset=utf-8" \
    --data-urlencode "Requirements=ids" \
    https://isrxz9drcd.execute-api.us-east-2.amazonaws.com/prod/  