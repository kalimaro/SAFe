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

st.title("SAFe Mock Test")

num_questions = 15 # Set the desired number of questions here

# Load questions only once
if not st.session_state.questions:
    with open('safe_questions.csv', 'r', encoding='UTF8') as f:
        reader = csv.reader(f)
        questions_list = list(reader)
        shuffle(questions_list)
        st.session_state.questions = questions_list[:num_questions]
        st.session_state.correct_answers = [q[6] for q in st.session_state.questions]

# Quiz form
with st.form(key="safe_quiz"):
    for i, question in enumerate(st.session_state.questions):
        st.write(f"{i+1}) {question[1]}")
        num_options = len(question) - 2
        options = [chr(65 + j) for j in range(num_options)]
        for j in range(2, len(question)):
            st.write(question[j])
        st.session_state.responses[i] = st.selectbox("Enter response:", options, key=f"q{i}", index=None)

    submitted = st.form_submit_button("Submit")

# Results processing
if submitted:
    st.session_state.submitted = True

if st.session_state.submitted:
    correct_count = 0
    for i in range(len(st.session_state.questions)):
        correct_answer_index = ord(st.session_state.correct_answers[i]) - 65
        if ord(st.session_state.responses[i]) - 65 == correct_answer_index:
            correct_count += 1
            st.success(f"Question {i+1} is Correct! Your answer: {st.session_state.responses[i]}")
        else:
            st.error(f"Question {i+1} is Incorrect. Your answer: {st.session_state.responses[i]}") # Correct answer not shown

    score = (correct_count / len(st.session_state.questions)) * 100
    st.info(f"Your final score: {score:.2f}%")

    if st.button("Retake Quiz"):
        st.session_state.submitted = False
        st.session_state.responses = {}
        st.session_state.questions = []
        st.experimental_rerun()
