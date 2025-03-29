"""
Word guessing game with Streamlit
Author: Wolf Paulus
"""
import streamlit as st
import streamlit.components.v1 as components
from game import select_word, word_match


def get_word() -> str:
    """ Get the word to guess, cleans up the session state for `guesses` if needed """
    if not st.session_state.get("word", None):
        if not (w := select_word('words.txt')):
            st.stop()
        st.session_state["word"] = w
        st.session_state["guesses"] = []
    return st.session_state.word


st.set_page_config(page_title="Word Game", page_icon=":game_die:")
html = "<style>code {font-size:18pt !important;}</style>"
st.markdown(html, unsafe_allow_html=True)
html = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'
st.markdown(html, unsafe_allow_html=True)
st.title("Word Guessing Game")
word = get_word()
word_length = len(word)
attempt_terms = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
attempt_terms[word_length - 1] = "last"

if st.session_state.get("guess", None):  # if there is a new guess
    st.session_state.guesses.append(st.session_state.get("guess").lower())
    st.session_state.guess = None

st.write(f"A word has been selected. It's {word_length} characters long. Let's play!")
st.write(f"You may guess up to {word_length} times. Good Luck!\n")
for i, guess in enumerate(st.session_state.guesses, start=1):  # enumerate all guesses
    match = word_match(st.session_state.word, guess)
    st.code(f"{i}. {guess} : {match if len(guess) == word_length else 'Invalid Guess'}")
    if guess == st.session_state.word:  # successfull guess
        st.write("Congratulations! You guessed correctly! :tada:")
        st.button("Play Again", on_click=st.session_state.clear())
        break
    elif match == st.session_state.word:  # successfull guess, kind of
        st.write("Lucky you! You kind of guessed correctly! :tada:")
        st.button("Play Again", on_click=st.session_state.clear())
        break
    elif i == word_length:  # out of guesses
        st.markdown(f"Sorry, you have run out of guesses. The word was: **{st.session_state.word}**")
        st.button("Play Again", on_click=st.session_state.clear())
        break
else:
    attmpt = attempt_terms[len(st.session_state.guesses)]
    st.text_input(f"Enter your {attmpt} guess:", max_chars=word_length, key="guess")
    components.html(
        """
<script>
var txtflds = Array.from(window.parent.document.querySelectorAll('input[type=text]'));
txtflds[txtflds.length-1].focus();
</script>
""", height=0, width=0)

link = '<a href="https://github.com/wolfpaulus/wordgame" target="_blank">Source Code</a>'
st.write(f'<i class="fa-brands fa-github"> {link} </i>', unsafe_allow_html=True)
