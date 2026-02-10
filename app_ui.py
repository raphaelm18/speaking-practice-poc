import streamlit as st

# Import your existing analysis function (and task_context/prompt remain in app.py)
from app import analyze_speaking_sample

TASKS = {
    "Elephants Spraying Water": {
        "image": "assets/elephants.jpg",
        "task_context": (
            "The student is describing a picture of elephants outdoors near a muddy water area.\n"
            "The picture shows one large adult elephant standing near the edge of the water.\n"
            "The adult elephant is spraying water sideways with its trunk, and the water splashes through the air.\n"
            "Two smaller elephants are nearby; one is standing close to the adult elephant and appears to be getting sprayed.\n"
            "The ground looks wet and muddy, suggesting the elephants may be cooling off or playing with water.\n"
            "The main focus of the picture is the elephants, their size differences, and the water being sprayed."
        ),
    },

    "Playground Monkey Bars": {
        "image": "assets/playground.jpg",
        "task_context": (
            "The student is describing a picture of children playing on a playground.\n"
            "The picture shows a girl hanging from yellow monkey bars, holding on with one hand while lifting her legs.\n"
            "She appears to be in motion and concentrating on climbing across the bars.\n"
            "In the background, other children are playing near playground equipment such as swings and climbing structures.\n"
            "The ground is covered with wood chips, and trees surround the play area.\n"
            "The main focus of the picture is the girl on the monkey bars, her movement, and the active playground setting."
        ),
    },

    "Meal Time Group Eating Together": {
        "image": "assets/meal.jpg",
        "task_context": (
            "The student is describing a picture of people sitting together at a table during a meal.\n"
            "The picture shows a group of adults and children seated around a table, eating food and talking with one another.\n"
            "Plates of food and drinks are on the table, and the people appear to be smiling and engaged in conversation.\n"
            "The setting looks like a shared mealtime, possibly at home or in a classroom or community space.\n"
            "The main focus of the picture is the people eating together, their interactions, and the shared meal."
        ),
    },
}


st.set_page_config(page_title="Speaking Practice POC", layout="centered")
st.title("Speaking & Listening Practice POC")
task_name = st.selectbox("Choose a task:", list(TASKS.keys()))
task = TASKS[task_name]

st.image(task["image"], use_container_width=True)
st.caption("Prompt: Look at the picture and describe what is happening.")
st.caption("Teacher-facing prototype for evaluating oral language using a structured rubric.")
#import os
#st.write("cwd:", os.getcwd())
#s.path.exists("assets"))
#st.write("assets contents:", os.listdir("assets"))
#st.write("image exists:", os.path.exists("assets/elephants.jpg"))
#st.image("assets/elephants.jpg", caption="DEBUG elephant", use_container_width=True)
#st.write("assets contents:", os.listdir("assets"))
#st.caption("Prompt: Look at the picture and describe what is happening.")

default_text = "I see two elephants at the zoo. One elephant is spraying water. The other elephant is smaller."

transcript = st.text_area(
    "Paste student transcript:",
    value=default_text,
    height=180,
    help="Paste what the student said (transcribed text).",
)

if st.button("Analyze", type="primary"):
    if not transcript.strip():
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("Analyzing..."):
            result = analyze_speaking_sample(transcript.strip())
        st.subheader("Teacher-Readable Summary & Rubric")
        st.markdown(result)