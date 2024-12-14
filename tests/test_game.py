"""
Test the game module.
Author: Wolf Paulus (wolf@paulus.com)
"""
from os import chdir
from game import select_word, word_match


def test_select_word():
    word = select_word('words.txt')
    assert word is not None
    assert 4 <= len(word) <= 7
    assert word.isalpha()
    assert word.islower()


def test_word_match():
    assert word_match("apple", "apple") == "apple"
    assert word_match("apple", "aplle") == "apple"
    assert word_match("apple", "p") == "_pp__"
    assert word_match('sweet', 'ethos') == 's_eet'
    assert word_match('hello', 'sleep') == '_ell_'
