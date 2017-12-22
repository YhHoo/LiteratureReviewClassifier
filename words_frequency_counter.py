# this code are retrieved and modified from https://programminghistorian.org/lessons/counting-frequencies
# Aims to create a script that will counts the freq of a words in a sentence.
# It will be further improved to count also 2 words (e.g. decision tree) or
# 3 words (e.g. recurrent neural network)as one

import stop_words as sw


# this function removes stop words fr a input list
def filter_stopwords(word_list_input, stop_words_input):
    return [w for w in word_list_input if w not in stop_words_input]


def word_list_to_frequency_dict(word_list_input):
    word_freq_list = [word_list_input.count(p) for p in word_list_input]
    # by converting to dict, dict will only record the same item and values once
    # Hence prevent repeating pairs of info
    return dict(zip(word_list_input, word_freq_list))


def sort_from_highest(word_f_dict):
    # interchange frequency and words in tuple
    temp = [(word_f_dict[key], key) for key in word_f_dict]
    temp.sort()
    temp.reverse()
    return temp


# Wrapper for the above 3 functions filter_stopwords, word_list_to_freq_dict and sort_from_highest
# Just input a string sentence like 'it was a good day indeed', it will return a list of tuples
# like [(4, 'ANN'), (3, 'decision'), ....]
def all_in_one(word_string_input, verbose=False):
    # split the word list into single words separated by space
    word_split_list = word_string_input.split()
    # filter stop words
    stop_word_filtered = filter_stopwords(word_split_list, sw.stopwords())
    # store into dictionary
    word_f_dict = word_list_to_frequency_dict(stop_word_filtered)
    # sorting by frequency
    sorted_list = sort_from_highest(word_f_dict)
    # data visualize
    if verbose:
        print('\nWords Sorted by Frequency:')
        for s in sorted_list:
            print(s)
    # return the sorted list of freq n words
    return sorted_list






