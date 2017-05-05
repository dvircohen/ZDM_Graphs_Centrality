import os

import pandas as pd



def is_in_range(words_list, i):
    return 0 <= i < len(words_list)


def get_context_of_word(word_list, index_of_word, window_size=2):
    current_context = []
    for i in range(window_size):
        i += 1
        if is_in_range(word_list, index_of_word - i):
            current_context.append(word_list[index_of_word - i])
        if is_in_range(word_list, index_of_word + i):
            current_context.append(word_list[index_of_word + i])
    return '^'.join(current_context)


def wevi_parser(random_walks_df, window_size):
    df = random_walks_df
    words = []
    contexts_to_words = []
    for current_sentence in df["String"]:
        list_current_words = current_sentence.split()
        for index, word in enumerate(list_current_words):
            contexts_to_words.append(get_context_of_word(list_current_words, index, window_size) + "|" + word)
    output_contexts_string = ','.join(contexts_to_words)
    return output_contexts_string
