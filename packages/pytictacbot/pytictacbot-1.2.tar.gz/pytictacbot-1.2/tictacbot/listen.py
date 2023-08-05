from pynput import keyboard
import pyperclip
import pyautogui
from art import text2art
from colorama import init, Fore, Style
import os

this_file_path = os.path.dirname(os.path.abspath(__file__))
gutenberg = os.path.join(this_file_path, "gutenberg.txt")

init()

keys_pressed = []
remaining_letters = list("abcdefghijklmnopqrstuvwxyz")


def retrieve_best_word(
    str_to_search: str, remaining_letters: list[str]
) -> dict["word":str, "score":int] | None:
    if str_to_search.isalpha():
        str_to_search = str_to_search.lower()

        best_word = {"word": None, "score": -1}
        with open(gutenberg, "r", encoding="utf-8") as f:
            for word in f:
                if str_to_search in word:
                    score = len(set(word) & set(remaining_letters))
                    word_found = {"word": word.strip(), "score": score}
                    if best_word["score"] < word_found["score"]:
                        best_word = word_found
            return best_word


def print_new_section(init: bool):
    global remaining_letters
    if not init:
        print("\n")
        print("_" * 50)
    label_colored = Fore.YELLOW + "Remaining letters: \n" + Style.RESET_ALL
    remaining_letters_beautified = ""
    for letter in remaining_letters:
        letter_colored = Fore.LIGHTBLUE_EX + letter + Style.RESET_ALL
        remaining_letters_beautified += "[" + letter_colored + "] "
    print(label_colored + remaining_letters_beautified + "\n")
    print(Fore.YELLOW + "Keys pressed: " + Style.RESET_ALL)


def print_success_message():
    text = "Alphabet completed !"
    width = len(text) + 4
    border = "-" * width
    content = f"| {text} |"
    str = f"{border}\n{content}\n{border}"

    for i, char in enumerate(str):
        color = i % 6
        if color == 0:
            print(Fore.RED + char, end="")
        elif color == 1:
            print(Fore.YELLOW + char, end="")
        elif color == 2:
            print(Fore.GREEN + char, end="")
        elif color == 3:
            print(Fore.CYAN + char, end="")
        elif color == 4:
            print(Fore.BLUE + char, end="")
        elif color == 5:
            print(Fore.MAGENTA + char, end="")

    print(Style.RESET_ALL)


def update_remaining_letters(word_found: str):
    global remaining_letters
    remaining_letters = [
        letter for letter in remaining_letters if letter not in word_found
    ]
    if len(remaining_letters) == 0:
        print_success_message()
        remaining_letters = list("abcdefghijklmnopqrstuvwxyz")


def paste_word(word: str):
    print("\n" + Fore.YELLOW + "Pasting..." + Style.RESET_ALL)
    pyperclip.copy(word)
    pyautogui.press("backspace", presses=len(keys_pressed) + 1)
    pyautogui.hotkey("command", "v")
    print(Fore.GREEN + "Pasted !" + Style.RESET_ALL)


def escape():
    print(Fore.YELLOW + "Escaping..." + Style.RESET_ALL)
    keys_pressed.clear()
    print_new_section(init=False)


def search():
    print("\n" + Fore.YELLOW + "Searching..." + Style.RESET_ALL)
    global remaining_letters
    str_to_search = "".join(keys_pressed)
    best_word = retrieve_best_word(str_to_search, remaining_letters)

    if best_word and best_word["word"] and len(best_word["word"]):
        word_found: str = best_word["word"]
        word_score: int = best_word["score"]

        # Colorization start (really annoying to read)
        word_found_label_colored = Fore.YELLOW + "Found: " + Style.RESET_ALL

        word_found_colored = ""
        remaining_letters_found = ""

        word_found = word_found.replace(str_to_search, str_to_search.upper())
        for letter in word_found:
            if letter.isupper():
                underlined = "\033[4m"
                if letter.lower() in remaining_letters:
                    if letter.lower() not in remaining_letters_found:
                        word_found_colored += (
                            Fore.LIGHTBLUE_EX
                            + underlined
                            + letter.lower()
                            + Style.RESET_ALL
                        )
                        remaining_letters_found += letter.lower()
                    else:
                        word_found_colored += (
                            underlined + letter.lower() + Style.RESET_ALL
                        )
                else:
                    word_found_colored += underlined + letter.lower() + Style.RESET_ALL
            elif letter.lower() in remaining_letters:
                if letter.lower() not in remaining_letters_found:
                    word_found_colored += Fore.LIGHTBLUE_EX + letter + Style.RESET_ALL
                    remaining_letters_found += letter.lower()
                else:
                    word_found_colored += letter
            else:
                word_found_colored += letter

        score_label_colored = Fore.YELLOW + "Score: " + Style.RESET_ALL
        if word_score > 0:
            score_colored = Fore.LIGHTBLUE_EX + str(word_score) + Style.RESET_ALL
        else:
            score_colored = Fore.RED + str(word_score) + Style.RESET_ALL
        score = score_colored + "/" + str(len(remaining_letters))
        if word_score == len(remaining_letters):
            score = (
                Fore.GREEN
                + str(word_score)
                + "/"
                + str(len(remaining_letters))
                + Style.RESET_ALL
            )
        # Colorization end (really annoying to read)

        print(
            word_found_label_colored
            + word_found_colored
            + " - "
            + score_label_colored
            + score
        )
        update_remaining_letters(word_found.lower())
        paste_word(word_found.lower())
    else:
        print(Fore.RED + "Not found" + Style.RESET_ALL)
    keys_pressed.clear()
    print_new_section(init=False)


def on_press(key):
    try:
        key_char = key.char
        if not key_char.isalpha():
            return
        keys_pressed.append(key_char)
    except AttributeError:
        if key == keyboard.Key.esc:
            escape()
        if key == keyboard.Key.space:
            search()

    if len(keys_pressed):
        print("".join(keys_pressed))


listener = keyboard.Listener(on_press=on_press)

listener.start()

print(text2art("Tictacbot"))
print_new_section(init=True)

listener.join()
