
mini_glossary = ['ml_glossary_all2.txt']
temp = []
for files in mini_glossary:
    with open(files, 'r') as f:
        for word in f:
            # write all words in lowercase
            temp.append(word.lower())
print('Extraction Completed !')
# save all extracted to another files
with open('ml_glossary_all2X.txt', 'w') as f:
    for word in temp:
        f.write(word)
print('Saving Completed !')