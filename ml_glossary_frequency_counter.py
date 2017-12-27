
def specific_counter():
    pdf = 'Today Jackson is attending the meeting at Traders hotel'
    wanted = 'traders hotel'

    # lowercase every word in pdf text
    if wanted in pdf.lower():
        print('FOUND !')
    else:
        print('NOT FOUND =(')


def glossary_database():
    # extract all words from all mini glossaries
    mini_glossary = ['ml_glossary_1.txt', 'ml_glossary_2.txt', 'ml_glossary_3.txt']
    temp = []
    for files in mini_glossary:
        with open(files, 'r') as f:
            for word in f:
                # write all words in lowercase
                temp.append(word.lower())
    print('Extraction Completed !')

    # sort alphabetically
    temp.sort()

    # save all extracted to another files
    with open('ml_glossary_all.txt', 'w') as f:
        for word in temp:
            f.write(word)
    print('Saving Completed !')

glossary_database()

