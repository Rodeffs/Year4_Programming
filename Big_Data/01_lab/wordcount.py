'''
map:
    text -> list(word, 1)
shuffle:
    list(word, 1) -> list(word, [value1, value2, ...])
reduce:
    list(word, [value1, value2, ...]) -> list(word, count)
'''

import os
import re

dir_path = r"C:\Users\user\Downloads\data"

def reader(dir_path: str) :
    for entry_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, entry_name)
        if os.path.isfile(full_path):
            with open(full_path, mode='r', encoding='utf-8') as f:
                yield f.read()

def mapper(text: str):
    for word in re.split(r'\W+', text):
        yield word, 1

def shuffler(lst):
    prev_word = None
    buffer = []
    is_new = True
    for word, value in lst:

        if is_new:
            buffer = [value,]
        
        if word == prev_word or prev_word is None:
            prev_word = word
            buffer.append(value)
            is_new = False
        else:
            prev_word = word
            is_new = True
            yield prev_word, buffer
            
    yield prev_word, buffer

'''
def reducer(lst):
    for word, values in lst:
        yield word, sum(values)
'''

def reducer(lst):
    for word, values in lst:
        yield -sum(values), word


def main():
    all_mapped_words = []
    for text in reader(dir_path):
        mapped_words = list(mapper(text))
        all_mapped_words.extend(mapped_words)

    # for word, values in shuffler(sorted(all_mapped_words)):
        #print(word, values)

    # print(sorted(all_mapped_words)[:1000])

    for count, word in sorted(reducer(shuffler(sorted(all_mapped_words)))):
        print(word, ":", -count)
    


if __name__ == '__main__':
    main()
