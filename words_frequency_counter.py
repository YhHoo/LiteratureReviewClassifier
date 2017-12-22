word_string = 'it was the best of of of times it was the worst of times '
word_list = word_string.split()


def word_list_to_frequency_dict(word_list):
    word_freq = [word_list.count(p) for p in word_list]
    # by converting to dict, dict will only record the same item and values once
    # Hence prevent repeating pairs of info
    return dict(zip(word_list, word_freq))


word_freq = word_list_to_frequency_dict(word_list)
print("Word String:\n", word_string, '\n')
print('Frequency Dict:\n', [word_freq[index] for index in word_freq])

