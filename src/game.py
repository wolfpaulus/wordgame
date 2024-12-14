"""
    Word guesing game
"""
from random import randint
from typing import Tuple, Union


def select_word(file_path: str) -> Union[str, None]:
    """ Picks a random word from a file that is 4-7 characters long, alphabetic, and lowercase.
        :param file_path: the path to the file containing the words.
        :param history: a list of previously selected words.
        return: the random word or None if an error occurs.
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            words = file.read().split('\n')
    except OSError as e:
        print(f"Error: {e}")
        return None
    valid_words = [w for w in words if 4 <= len(w) <= 7 and w.isalpha() and w.islower()]
    if not valid_words:
        print("No valid words found.")
        return None
    return valid_words[randint(0, len(valid_words) - 1)]


def word_match(word: str, guess: str) -> str:
    """Return a string with the guessed characters in the word, and underscores for the unguessed characters."""
    return ''.join([c if c in guess else '_' for c in word])


def play() -> None:
    """ Play the word guessing game
        The player has to guess a random word from a file.
        The player has as many attempts as the length of the word.
    """
    print("Welcome to the word guessing game!")
    while True:
        word = select_word('words.txt')
        if not word:
            exit(1)
        length = len(word)
        print(f"Try to guess the word. It's {length} characters long.")
        print(f"You may guess up to {length} times. Good Luck!\n")
        for i in range(length):
            guess = input(f"\n{i+1}. Enter your guess: ").lower()
            if len(guess) != length or not guess.isalpha():
                print(f"Invalid guess. Please enter a {length}-letter word.")
                continue
            match = word_match(word, guess)
            if match == word:
                print("Congratulations! You guessed correctly!")
                break
            print(match)
        else:
            print(f"Sorry, you did not guess the word. The word was '{word}'.")
        if input("\nPlay again? (yes/no): ").strip().lower() != 'yes':
            print("\nThanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    assert word_match('sweet', 'ethos') == 's_eet'
    assert word_match('hello', 'sleep') == '_ell_'
    play()
