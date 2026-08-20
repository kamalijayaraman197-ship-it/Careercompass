import streamlit as st
import pandas as pd

# =====================================================
# PAGE
# =====================================================

st.set_page_config(
    page_title="Career Compass AI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Career Compass AI")

st.write(
    "Personalized career guidance and learning pathways "
    "for students and working learners after 12th."
)

st.info(
    "Career Compass AI is a guidance tool. It does not "
    "replace professional career counselling or official "
    "college/admission information."
)

# =====================================================
# LOAD DATA
# =====================================================

try:
    data = pd.read_csv("careers.csv")

except FileNotFoundError:

    st.error(
        "❌ careers.csv not found. Keep careers.csv "
        "and app.py in the same folder."
    )

    st.stop()

# =====================================================
# STUDENT PROFILE
# =====================================================

st.header("🎓 Step 1: Your Profile")

col1, col2 = st.columns(2)

with col1:

    stream = st.selectbox(
        "Your 12th Stream",
        [
            "Science - Mathematics + Computer Science",
            "Science - Mathematics + Biology",
            "Commerce",
            "Arts / Humanities"
        ]
    )

    subjects = st.multiselect(
        "📚 Subjects you are interested in",
        [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Biology",
            "Computer Science",
            "Accountancy",
            "Economics",
            "Business Studies",
            "English",
            "Design"
        ]
    )

with col2:

    interests = st.multiselect(
        "❤️ Your interests",
        [
            "Programming",
            "Artificial Intelligence",
            "Technology",
            "Data Analysis",
            "Cybersecurity",
            "Web Development",
            "Medicine",
            "Healthcare",
            "Biology",
            "Business",
            "Finance",
            "Entrepreneurship",
            "Design",
            "Robotics",
            "Electronics",
            "Research"
        ]
    )

    strengths = st.multiselect(
        "💪 Your strengths",
        [
            "Logical Thinking",
            "Problem Solving",
            "Mathematics",
            "Creativity",
            "Communication",
            "Leadership",
            "Curiosity",
            "Patience",
            "Empathy",
            "Analytical Thinking"
        ]
    )

# =====================================================
# EDUCATION PREFERENCES
# =====================================================

st.header("🏫 Step 2: Education Preferences")

college_preference = st.selectbox(
    "Preferred College Type",
    [
        "Government College",
        "Private College",
        "Any College"
    ]
)

scholarship = st.selectbox(
    "Interested in scholarships / financial aid?",
    [
        "Yes",
        "No",
        "I want to explore options"
    ]
)

learning_budget = st.selectbox(
    "💰 Budget for Additional Learning Resources",
    [
        "Mostly Free Resources",
        "Low-Cost Resources",
        "Flexible Budget"
    ]
)

st.caption(
    "This budget refers to additional learning resources, "
    "not college tuition fees."
)

# =====================================================
# SKILLS
# =====================================================

skills = st.multiselect(
    "💻 Existing skills (optional)",
    [
        "Python",
        "Excel",
        "HTML",
        "JavaScript",
        "Programming",
        "Design",
        "None"
    ]
)

# =====================================================
# ANALYZE
# =====================================================

if st.button(
    "🚀 Find My Career Path",
    use_container_width=True
):

    if len(subjects) == 0:

        st.warning(
            "Please select at least one subject."
        )

        st.stop()

    if len(interests) == 0:

        st.warning(
            "Please select at least one interest."
        )

        st.stop()

    # -------------------------------------------------
    # LOWERCASE INPUT
    # -------------------------------------------------

    student_subjects = [
        x.lower()
        for x in subjects
    ]

    student_interests = [
        x.lower()
        for x in interests
    ]

    student_strengths = [
        x.lower()
        for x in strengths
    ]

    results = []

    # =================================================
    # CAREER MATCHING
    # =================================================

    for _, row in data.iterrows():

        required_subjects = [
            x.strip().lower()
            for x in row["required_subjects"].split(";")
        ]

        career_interests = [
            x.strip().lower()
            for x in row["interests"].split(";")
        ]

        career_strengths = [
            x.strip().lower()
            for x in row["strengths"].split(";")
        ]

        # ---------------------------------------------
        # SUBJECT SCORE
        # ---------------------------------------------

        matched_subjects = [
            subject
            for subject in required_subjects
            if subject in student_subjects
        ]

        if len(required_subjects) > 0:

            subject_score = (
                len(matched_subjects)
                /
                len(required_subjects)
            ) * 100

        else:

            subject_score = 0

        # ---------------------------------------------
        # INTEREST SCORE
        # ---------------------------------------------

        interest_matches = 0

        for student_interest in student_interests:

            for career_interest in career_interests:

                if (
                    student_interest in career_interest
                    or
                    career_interest in student_interest
                ):

                    interest_matches += 1
                    break

        interest_score = min(
            interest_matches * 25,
            100
        )

        # ---------------------------------------------
        # STRENGTH SCORE
        # ---------------------------------------------

        strength_matches = 0

        for student_strength in student_strengths:

            for career_strength in career_strengths:

                if (
                    student_strength in career_strength
                    or
                    career_strength in student_strength
                ):

                    strength_matches += 1
                    break

        strength_score = min(
            strength_matches * 25,
            100
        )

        # ---------------------------------------------
        # FINAL SCORE
        # ---------------------------------------------

        final_score = (
            subject_score * 0.35
            +
            interest_score * 0.45
            +
            strength_score * 0.20
        )

        results.append({

            "career": row["career"],

            "score": final_score,

            "matched_subjects":
                matched_subjects,

            "description":
                row["description"],

            "education":
                row["education_path"],

            "skills":
                row["skills_to_learn"],

            "resources":
                row["free_resources"],

            "resource_types":
                row["resource_types"],

            "certificate":
                row["certificate_note"],

            "interest_score":
                interest_score,

            "subject_score":
                subject_score,

            "strength_score":
                strength_score
        })

    # =================================================
    # SORT
    # =================================================

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    # =================================================
    # TOP CAREERS
    # =================================================

    st.success(
        "✅ Career analysis completed!"
    )

    st.header("🏆 Top Career Recommendations")

    for number, result in enumerate(
        results[:3],
        start=1
    ):

        st.subheader(
            f"{number}. {result['career']}"
        )

        st.progress(
            min(
                result["score"] / 100,
                1.0
            )
        )

        st.write(
            f"### 🎯 Career Fit: "
            f"{result['score']:.0f}%"
        )

        st.write(
            f"**Why:** {result['description']}"
        )

        st.write(
            f"🎓 **Education:** "
            f"{result['education']}"
        )

        if result["matched_subjects"]:

            st.write(
                "📚 **Matching subjects:** "
                +
                ", ".join(
                    result["matched_subjects"]
                )
            )

        st.divider()

    # =================================================
    # BEST CAREER
    # =================================================

    best = results[0]

    st.header("🌟 Your Strongest Career Match")

    st.success(
        f"**{best['career']}** — "
        f"{best['score']:.0f}% career fit"
    )

    # =================================================
    # EXPLAINABLE SCORE
    # =================================================

    st.header("🧠 Why This Career?")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "❤️ Interest Match",
            f"{best['interest_score']:.0f}%"
        )

    with c2:

        st.metric(
            "📚 Subject Match",
            f"{best['subject_score']:.0f}%"
        )

    with c3:

        st.metric(
            "💪 Strength Match",
            f"{best['strength_score']:.0f}%"
        )

    st.caption(
        "Scoring: Interests 45% | Subjects 35% | Strengths 20%"
    )

    # =================================================
    # EDUCATION PATH
    # =================================================

    st.header("🎓 Education Path")

    st.write(
        f"12th → {best['education']} → "
        "Skills → Projects → Internship → Career"
    )

    # =================================================
    # SKILLS
    # =================================================

    st.header("📚 Skills You Can Learn")

    skills_to_learn = [
        x.strip()
        for x in best["skills"].split(";")
    ]

    for number, skill in enumerate(
        skills_to_learn,
        start=1
    ):

        st.write(
            f"**{number}.** {skill}"
        )

    # =================================================
    # LEARNING RESOURCES
    # =================================================

    st.header("🌐 Accessible Learning Resources")

    st.write(
        "These are resource providers identified in "
        "our prototype for this career. Before using a "
        "course, verify its current availability, cost "
        "and certificate policy on the provider's official site."
    )

    resources = [
        x.strip()
        for x in best["resources"].split(";")
    ]

    resource_types = [
        x.strip()
        for x in best["resource_types"].split(";")
    ]

    for number, resource in enumerate(
        resources,
        start=1
    ):

        if len(resource_types) >= number:

            resource_type = resource_types[number - 1]

        else:

            resource_type = "Learning Resource"

        st.write(
            f"### {number}. {resource}"
        )

        st.write(
            f"📖 Focus: {resource_type}"
        )

        if learning_budget == "Mostly Free Resources":

            st.success(
                "🟢 Prioritize free/open learning "
                "options from this provider."
            )

        elif learning_budget == "Low-Cost Resources":

            st.info(
                "🟡 Check free options first, then "
                "consider affordable courses."
            )

        else:

            st.info(
                "🔵 You can consider both free and "
                "paid options."
            )

    # =================================================
    # CERTIFICATE
    # =================================================

    st.header("🏆 Certificate Information")

    st.write(
        best["certificate"]
    )

    st.caption(
        "Career Compass AI does not claim that all "
        "resources provide free certificates. "
        "Certificate availability depends on the "
        "individual provider and course."
    )

    # =================================================
    # ROADMAP
    # =================================================

    st.header("🗺️ Step-by-Step Learning Roadmap")

    roadmaps = {

        "AI and Data Science": [
            "Learn Python",
            "Learn Mathematics and Statistics",
            "Learn SQL",
            "Learn Data Analysis",
            "Learn Machine Learning",
            "Build AI projects",
            "Create a portfolio",
            "Look for internships or suitable career opportunities"
        ],

        "Computer Science Engineering": [
            "Learn programming",
            "Learn Data Structures",
            "Learn Algorithms",
            "Learn DBMS",
            "Learn Computer Networks",
            "Build software projects",
            "Learn Git and GitHub",
            "Build a portfolio"
        ],

        "Cybersecurity": [
            "Learn networking fundamentals",
            "Learn Linux",
            "Learn cybersecurity fundamentals",
            "Learn security concepts",
            "Practice in legal labs",
            "Build cybersecurity projects",
            "Create a portfolio"
        ],

        "Data Analytics": [
            "Learn Excel",
            "Learn SQL",
            "Learn Statistics",
            "Learn Python",
            "Learn Pandas",
            "Learn data visualization",
            "Build real-world projects",
            "Create a portfolio"
        ],

        "Web Development": [
            "Learn HTML",
            "Learn CSS",
            "Learn JavaScript",
            "Learn Git and GitHub",
            "Learn frontend development",
            "Learn backend development",
            "Build websites",
            "Create a portfolio"
        ],

        "Software Development": [
            "Learn programming",
            "Learn Data Structures",
            "Learn Algorithms",
            "Learn databases",
            "Learn Git",
            "Build applications",
            "Build a portfolio"
        ]
    }

    if best["career"] in roadmaps:

        for number, step in enumerate(
            roadmaps[best["career"]],
            start=1
        ):

            st.write(
                f"**Step {number}:** {step}"
            )

    else:

        st.write(
            "A detailed roadmap for this career "
            "will be added in the next version."
        )

    # =================================================
    # TOP 5 COMPARISON
    # =================================================

    st.header("📊 Compare Top Career Options")

    comparison = pd.DataFrame({

        "Career": [
            x["career"]
            for x in results[:5]
        ],

        "Career Fit %": [
            round(x["score"])
            for x in results[:5]
        ],

        "Education": [
            x["education"]
            for x in results[:5]
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    # =================================================
    # ACCESSIBILITY MESSAGE
    # =================================================

    st.header("🌍 Our Vision")

    st.write(
        "Our long-term goal is to make career guidance "
        "and learning opportunities more accessible to "
        "students and working learners, including people "
        "from rural, remote, hill and tribal communities."
    )

    st.write(
        "Future versions can integrate verified free "
        "learning resources, scholarships, certificate "
        "courses, continuously updated career information "
        "and resources from reliable providers around "
        "the world."
    )

    st.info(
        "🎯 You do not need to be enrolled in college to "
        "use Career Compass AI or explore the learning "
        "resources. However, some careers and professions "
        "require formal degrees, licenses or other "
        "qualifications."
    )