import streamlit as st

from Database.Mongodb import(
    students_collection,
    bmi_collection
)

st.title("BMI Calculator")

# Load Students
students=list(
    students_collection.find()
)

if not students:
    
    st.warning(
        "No students available. Please register students first."
    )
    
    st.stop()
    
#Students Dropdown
student_names=[]

for student in students:
    
    full_name=(
        student["first_name"]
        +" "
        +student["last_name"]
    )
    
    student_names.append(full_name)
    
selected_student=st.selectbox(
    "Select Student",
    student_names    
)

#BMI INPUTS

height=st.number_input(
    "Height(metres)",
    min_value=0.5,
    max_value=3.0,
    value=1.70,
    step=0.01    
) 

weight=st.number_input(
    "Weight(kg)",
    min_value=1,
    max_value=300,
    value=70
)

# Calculate BMI
if st.button("Calculate BMI"):

    bmi = weight / (height * height)

    if bmi < 18.5:
        category = "Underweight"

    elif bmi < 25:
        category = "Normal"

    elif bmi < 30:
        category = "Overweight"

    else:
        category = "Obese"

    # Show Results
    st.metric(
        "BMI Score",
        round(bmi, 2)
    )

    st.success(
        f"Category: {category}"
    )

    # Save to MongoDB
    bmi_collection.insert_one({

        "student_name":
        selected_student,

        "height":
        height,

        "weight":
        weight,

        "bmi":
        round(bmi, 2),

        "category":
        category

    })

    st.success(
        "BMI Report Saved Successfully"
    )

# View Reports
st.subheader("BMI Reports")

reports = list(
    bmi_collection.find()
)

if reports:

    for report in reports:

        st.write(

            f"{report['student_name']} | "
            f"BMI: {report['bmi']} | "
            f"{report['category']}"
        )

else:

    st.info(
        "No BMI Reports Found"
    )

# Summary
st.subheader("BMI Summary")

st.metric(
    "Total BMI Reports",
    len(reports)
)