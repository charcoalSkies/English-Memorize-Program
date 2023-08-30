import subprocess
import random
import os

def read_word_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    word_dict = {}
    for line_no, line in enumerate(lines, start=1):
        try:
            eng, kor = line.strip().split(' | ')
        except ValueError:
            print(f"파일 {file_path}의 {line_no}번째 줄에 문제가 있습니다: {line.strip()}")
            continue

        kor_meanings = kor.split(', ')
        eng = eng.strip()
        
        if eng in word_dict:
            word_dict[eng].extend(kor_meanings)
        else:
            word_dict[eng] = kor_meanings
        
    return word_dict

def ask_day():
    day = input("어느 day의 단어를 테스트하시겠습니까? (예: 1, 2, 3, ...): ")
    return day

def check_answer(answer, correct_answers):
    normalized_answer = answer.replace(' ', '').lower()
    normalized_answer_parts = set(normalized_answer.replace(';', ',').split(','))

    for correct in correct_answers:
        normalized_correct = correct.replace(' ', '').lower()
        normalized_correct_parts = set(normalized_correct.replace(';', ',').split(','))

        stripped_answer_parts = {part.split('.')[-1] for part in normalized_answer_parts}
        stripped_correct_parts = {part.split('.')[-1] for part in normalized_correct_parts}

        if all(any(answer_part == correct_part.split('.')[-1] for correct_part in normalized_correct_parts)
               for answer_part in stripped_answer_parts):
            return True

    return False

wrong_answers_global = set()

def save_wrong_answers(word_dict, day):
    try:
        with open(f"/Users/mac/Dev/Project/RandomWord/wrong/eDay{day}.txt", 'w', encoding='utf-8') as f:
            for question in wrong_answers_global:
                f.write(f"{question} | {', '.join(word_dict[question])}\n")
        print(f"틀린 답이 'eDay{day}.txt' 파일에 저장되었습니다.\n")
        subprocess.run(["open", "/Users/mac/Dev/Project/RandomWord/wrong"])
    except Exception as e:
        print(f"틀린 답을 파일에 저장하는 중 오류가 발생했습니다: {e}")

def play_eng_to_kor(word_dict):
    wrong_answers = set()
    print("문법 문제 입니다.\n")
    
    for question in word_dict.keys():
        correct = word_dict[question]
        print(f"{question}")
        answer = input("답: ").strip()

        if check_answer(answer, correct):
            print("정답입니다!\n")
        else:
            print(f"정답은 {', '.join(correct)} 입니다.\n")
            wrong_answers.add(question)
            wrong_answers_global.update(wrong_answers)

    while wrong_answers:
        question = random.choice(list(wrong_answers))
        correct = word_dict[question]
        print(f"{question}")
        answer = input("답: ").strip()

        if check_answer(answer, correct):
            print("정답입니다!\n")
            wrong_answers.remove(question)
        else:
            print(f"정답은 {', '.join(correct)} 입니다.\n")

def play_game(file_path, day):
    word_dict = read_word_file(file_path)
    play_eng_to_kor(word_dict)
    if wrong_answers_global:
        save_wrong_answers(word_dict, day)

day = ask_day()
file_path = f'/Users/mac/Dev/Project/RandomWord/word/day{day}.txt'

if os.path.exists(file_path):
    play_game(file_path, day)
else:
    print(f"day{day}.txt 파일이 존재하지 않습니다.")
