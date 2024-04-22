from collections import Counter

def count_letters(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        letters = (char for char in text if char.isalpha() and char not in "āēšŗūīļķģšāžčņ")
        letter_count = Counter(letters)
        total_letters = sum(letter_count.values())
        letter_percentages = {letter: (count / total_letters * 100) for letter, count in letter_count.items()}
        return tuple(letter_percentages.items())

def display_frequencies(letter_percentages1, letter_percentages2):
    sorted_percentages1 = tuple(sorted(letter_percentages1, key=lambda x: x[1], reverse=True))
    sorted_percentages2 = tuple(sorted(letter_percentages2, key=lambda x: x[1], reverse=True))
    
    print("Latvian    English")
    for i in range(len(sorted_percentages1)):
        (letter1, percentage1) = sorted_percentages1[i]
        (letter2, percentage2) = sorted_percentages2[i]
        spaces1 = ' ' * (8 - len(letter1))
        spaces2 = ' ' * (8 - len(letter2))
        print(letter1 + ": {:.1f}%".format(percentage1) + spaces1 + "  " + letter2 + ": {:.1f}%".format(percentage2))

text_lv_percentages = count_letters('Text_lv.txt')
text_eng_percentages = count_letters('Text_eng.txt')

display_frequencies(text_lv_percentages, text_eng_percentages)