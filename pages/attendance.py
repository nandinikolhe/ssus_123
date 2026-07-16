
import streamlit as st

from Database.Mongodb import (
    students_collection,
    attendance_collection
)

st.title("📅 Attendance Management")

students = list(
    students_collection.find()
)

if not students:

    st.warning(
        "No students available"
    )

    st.stop()
    
student_names = []

for student in students:

    full_name = (
        student["first_name"]
        + " "
        + student["last_name"]
    )

    student_names.append(full_name)

selected_student = st.selectbox(
    "Select Student",
    student_names
)

attendance_date = st.date_input(
    "Attendance Date"
)

status = st.selectbox(

    "Status",

    [
        "Present",
        "Absent"
    ]
)

if st.button("Save Attendance"):

    attendance_collection.insert_one({

        "student_name":
        selected_student,

        "date":
        str(attendance_date),

        "status":
        status

    })

    st.success(
        "Attendance Saved"
    )
    
st.subheader(
    "Attendance Records"
)

records = list(
    attendance_collection.find()
)

for record in records:

    st.write(

        record["student_name"],

        "|",

        record["date"],

        "|",

        record["status"]
    )
    
st.subheader(
    "Attendance Summary"
)

for student in student_names:

    total = attendance_collection.count_documents({

        "student_name":
        student

    })

    present = attendance_collection.count_documents({

        "student_name":
        student,

        "status":
        "Present"

    })

    if total > 0:

        percentage = (
            present / total
        ) * 100

        st.write(

            f"{student}: "
            f"{round(percentage,2)}%"
        )
        
        
        
        
        
        
        
        
        
        
        
