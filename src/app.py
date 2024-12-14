"""
Word guessing game with Streamlit
Author: Wolf Paulus
"""
import json
import streamlit as st
import streamlit.components.v1 as components
from streamlit_server_state import server_state, server_state_lock
from game import select_word, word_match


def sync_server_state(file_path="server_state.json") -> None:
    """ Sync server state with file """
    with server_state_lock["server_state"]:
        try:
            if server_state:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(dict(server_state.items()), f)
            else:
                with open(file_path, encoding="utf-8") as f:
                    server_state.update(json.load(f))
        except OSError as e:
            st.error(f"Error: {e}")


def increment_game_count() -> None:
    """ Increment game count """
    with server_state_lock["server_state"]:
        server_state["game_count"] = server_state.get("game_count", 0) + 1
    sync_server_state()


def get_word() -> str:
    """ Get the word to guess and increment the game count if necessary """
    if not st.session_state.get("word", None):
        if not (w := select_word('words.txt')):
            st.stop()
        st.session_state["word"] = w
        st.session_state["guesses"] = []
        increment_game_count()
    return st.session_state.word


st.markdown("""<style>code {font-size:18pt !important;}</style>""", unsafe_allow_html=True)
st.title('Word Guessing Game')
st.subheader('Embry-Riddle Aeronautical University - CS 118 - Fall 2024', divider="blue")
st.write(F"Welcome to the word guessing game! {server_state.get("game_count", 0)} Games played so far.")
word = get_word()
word_length = len(word)
attempt_terms = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
attempt_terms[word_length - 1] = "last"

if st.session_state.get("guess", None):
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
