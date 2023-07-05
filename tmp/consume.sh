#!/bin/bash
# echo ""
# echo ""

# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/departments.csv \
#     --data-urlencode "Tabla=departments" \
#     https://rbwdwmrim8.execute-api.us-east-2.amazonaws.com/prod/
# echo ""

# echo ""


# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/jobs.csv \
#     --data-urlencode "Tabla=jobs" \
#     https://rbwdwmrim8.execute-api.us-east-2.amazonaws.com/prod/
# echo ""
# echo ""


# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/hired_employees_0.csv \
#     --data-urlencode "Tabla=hired_employees" \
#     https://rbwdwmrim8.execute-api.us-east-2.amazonaws.com/prod/
# echo ""
# echo ""

# curl -X POST \
#     -H "Content-Type: text/csv; charset=utf-8" \
#     --data-binary @tmp/hired_employees_2.csv \
#     --data-urlencode "Tabla=hired_employees" \
#     https://rbwdwmrim8.execute-api.us-east-2.amazonaws.com/prod/ 

echo "Running for hired employees"
echo ""
curl -X GET \
    -H "Content-Type: application/json" \
    https://rbwdwmrim8.execute-api.us-east-2.amazonaws.com/prod/test?requirements=employees
echo ""

echo "Running for hired ids"
echo ""
curl -X GET \
    -H "Content-Type: text/csv" \
    https://rbwdwmrim8.execute-api.us-east-2.amazonaws.com/prod/test?requirements=ids
echo ""
echo ""
