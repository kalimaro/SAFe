
import streamlit as st
import csv
from random import shuffle

# Session state initialization
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = []
if 'num_questions' not in st.session_state:
    st.session_state.num_questions = 10  # Default number of questions

st.title("SAFe Mock Test")

# Number of questions selection
st.session_state.num_questions = st.slider("Select Number of Questions:", min_value=5, max_value=20, value=st.session_state.num_questions, step=1)

# Load questions only once
if not st.session_state.questions:
    with open('safe_questions.csv', 'r', encoding='UTF8') as f:  # Replace with your CSV file
        reader = csv.reader(f)
        questions_list = list(reader)
        shuffle(questions_list)
        st.session_state.questions = questions_list[:st.session_state.num_questions]
        st.session_state.correct_answers = [q[6] for q in st.session_state.questions]  # Assuming correct answer is in the 7th column (index 6)

# Quiz form
with st.form(key="safe_quiz"):
    for i, question in enumerate(st.session_state.questions):
        st.write(f"{i+1}) {question[1]}")  # Question text (assuming it's in the 2nd column)
        num_options = len(question) - 2 # Calculate the number of options dynamically
        options = [chr(65 + j) for j in range(num_options)] # Generate option labels (A, B, C, ...)
        for j in range(2, len(question)):  # Options (adjust range if needed)
            st.write(question[j])
        st.session_state.responses[i] = st.selectbox("Enter response:", options, key=f"q{i}", index=None)

    submitted = st.form_submit_button("Submit")

# Results processing
if submitted:
    st.session_state.submitted = True

if st.session_state.submitted:
    correct_count = 0
    for i in range(len(st.session_state.questions)):
        correct_answer_index = ord(st.session_state.correct_answers[i]) - 65 # Convert correct answer (A, B, C...) to index (0, 1, 2...)
        if ord(st.session_state.responses[i]) - 65 == correct_answer_index: # Compare selected option index with correct answer index
            correct_count += 1
            st.success(f"Question {i+1} is Correct! Your answer: {st.session_state.responses[i]}")
        else:
            st.error(f"Question {i+1} is Incorrect. Your answer: {st.session_state.responses[i]}, Correct answer: {st.session_state.correct_answers[i]}")

    score = (correct_count / len(st.session_state.questions)) * 100
    st.info(f"Your final score: {score:.2f}%")

    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.responses = {}
        st.session_state.questions = [] # Clear questions to allow reloading
        st.experimental_rerun()
