import json

with open('filtered-wordle-words.csv', 'r', encoding='utf-8') as f:
    with open('word_list.py', 'a', encoding="utf-8") as f_out:
        f_out.write('WORD_LIST = [\n')
        for _ in range(2309):
            word = f.readline().strip() # Bỏ dấu enter
            f_out.write(f"\"{word}\",\n")
        f_out.write("]\n")
            
with open('dictionary_vi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    word_list = [word for word in data.keys() if len(word) == 5 and " " not in word and "-" not in word]
    # thêm mà ko ghi dè file: https://www.w3schools.com/python/python_file_write.asp    
    with open('word_list_vn.py', 'a', encoding='utf-8') as f_out:
        f_out.write("VN_LIST = [\n")
        for word in word_list:
            f_out.write(f"\"{word}\",\n")
        f_out.write("]")