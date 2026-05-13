# remove duplicate from a list
employee_ids=[101,102,103,101,104,102,105]

newemp_id=[]

for employee_ids in employee_ids:
    if employee_ids not in newemp_id:
        newemp_id.append(employee_ids)
print(newemp_id)