import streamlit as st
import requests
import random as r

SCORE_TXT = 'highest_score.txt'

st.set_page_config(page_title='Test your knowledge quiz!', page_icon='random',
                   menu_items={
                       'Get Help': 'mailto:danioshi@gmail.com',
                       'Report a bug': "mailto:danioshi@gmail.com",
                       'About': "# Made by Daniel Osorio. This app uses *The Trivia API*."
                   }
                   )


@st.cache_data
def get_questions(placeholder=0) -> list:
    placeholder += 1
    response = requests.get('https://the-trivia-api.com/api/questions')
    response.raise_for_status()
    # st.success('The API call was successful')
    return response.json()


def get_highest_score(placeholder=0):
    placeholder += 1
    try:
        with open(SCORE_TXT) as file:
            highest_score_name, highest_score_questions, highest_score = file.read().split('/')
    except FileNotFoundError:
        highest_score_name, highest_score_questions, highest_score = '', 0, 0
    return highest_score_name, highest_score_questions, highest_score


def check_score():
    highest_score_name, highest_score_questions, highest_score = get_highest_score()
    if st.session_state.correct > float(highest_score):
        try:
            with open(SCORE_TXT, 'w') as file:
                u_name = st.session_state.user_name.replace('/', '-')
                file.write(f'{u_name}/{st.session_state.count}/{st.session_state.correct}')
                st.success(f'You made a new highest score with {st.session_state.correct}!')
        except FileNotFoundError:
            pass


def check_answer(answer=''):
    st.session_state.count += 1
    if answer == st.session_state.correct_answer:
        st.success(f'Correct! {answer}')
        st.session_state.correct += 1
        check_score()
    else:
        st.error(f'Incorrect! The right answer was {st.session_state.correct_answer}')


st.title('Test your knowledge!')

user_name = st.text_input('What is your name?', max_chars=50, key='user_name')
if user_name:
    st.header(f'Welcome, {user_name}!')
    if 'count' not in st.session_state:
        st.session_state.count = 0
    if 'correct' not in st.session_state:
        st.session_state.correct = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = get_questions()
    if st.session_state.count > 0 and st.session_state.count % len(st.session_state.questions) == 0:
        st.session_state.questions = get_questions(st.session_state.count)

    question = st.session_state.questions[st.session_state.count % len(st.session_state.questions)]

    st.session_state.correct_answer = question['correctAnswer']
    answers = question['incorrectAnswers'] + [st.session_state.correct_answer]
    r.shuffle(answers)

    st.write(question['question'])
    st.button(answers[0], on_click=check_answer, kwargs=dict(answer=answers[0]))
    st.button(answers[1], on_click=check_answer, kwargs=dict(answer=answers[1]))
    st.button(answers[2], on_click=check_answer, kwargs=dict(answer=answers[2]))
    st.button(answers[3], on_click=check_answer, kwargs=dict(answer=answers[3]))

    st.write(f'Score: {st.session_state.correct} out of {st.session_state.count} questions.')
    hs_name, hs_questions, hs = get_highest_score()
    if hs:
        st.markdown(f'Highest score by: **{hs_name}**, with **{hs}** correct out of **{hs_questions}** questions.')
