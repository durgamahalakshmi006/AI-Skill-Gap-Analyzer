import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load job skills dataset
jobs = pd.read_excel("job_skills.xlsx")

# Remove empty rows
jobs = jobs.dropna(subset=["Job_Role"])

# Page title
st.title("🎯 AI-Based Skill Gap Analyzer")
st.write("Analyze your skills and find the skills you need to learn.")

# Job role selection
target_role = st.selectbox(
    "Select your target job role:",
    jobs["Job_Role"].tolist()
)

# Skills input
user_input = st.text_input(
    "Enter your skills separated by commas:",
    placeholder="Example: Python, SQL, Excel"
)

# Analyze button
if st.button("Analyze Skills"):

    job = jobs[
        jobs["Job_Role"].str.lower() == target_role.lower()
    ]

    required_skills = job.iloc[0]["Required_Skills"].split(",")

    candidate_skills = [
        skill.strip().lower()
        for skill in user_input.split(",")
    ]

    required_skills = [
        skill.strip()
        for skill in required_skills
    ]

    # Find matching and missing skills
    matching_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill.lower() in candidate_skills:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Calculate percentage
    match_percentage = (
        len(matching_skills) / len(required_skills)
    ) * 100

    # Results
    st.subheader("📊 Analysis Result")

    st.write("### ✅ Matching Skills")
    for skill in matching_skills:
        st.write("✓", skill)

    st.write("### ❌ Missing Skills")
    for skill in missing_skills:
        st.write("✗", skill)

    st.metric(
        "Skill Match Percentage",
        f"{match_percentage:.1f}%"
    )

    # Recommendations
    st.subheader("💡 Recommendations")

    if missing_skills:
        st.write("You should learn:")
        for skill in missing_skills:
            st.write("→", skill)
    else:
        st.success(
            "Excellent! You have all the required skills."
        )

    # Chart
    st.subheader("📈 Skill Gap Chart")

    labels = ["Matching Skills", "Missing Skills"]
    values = [len(matching_skills), len(missing_skills)]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, values)
    ax.set_title("Skill Gap Analysis")
    ax.set_ylabel("Number of Skills")

    st.pyplot(fig)