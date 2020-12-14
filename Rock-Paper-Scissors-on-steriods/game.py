# Write your code here
from enum import Enum
import random


class Outcome(Enum):
    """
    Outcome Enum class
    """
    WIN = 100
    DRAW = 50
    LOST = 0


def get_result(user_input: str, comp_input: str, game_win_dict: dict) -> Outcome:
    """
    Prints result based on user and computer's random input

    Args:
        user_input (str): User input
        comp_input (str): Computer's random input
        game_win_dict (dict): dictionary of character values with key as list of characters the value character can win

    Returns:
        Outcome: win , draw or lost
    """

    # Both players made same choice
    if comp_input == user_input:
        print(f"There is a draw ({user_input})")
        return Outcome.DRAW
    elif comp_input in game_win_dict[user_input]:
        print(f"Sorry, but the computer chose {comp_input}")
        return Outcome.LOST
    else:
        print(f"Well done. The computer chose {comp_input} and failed")
        return Outcome.WIN


def build_game_dict(chars: list):
    """
    Builds the game dictionary. Contains list of characters that can win the value character
    Args:
        chars (list): list of characters in the game

    Returns:
        dict: Game winning dictionary.
    """
    # half of the characters can win the value character
    value_len = int(len(chars) / 2)
    game_win_dict = {}
    for char_index, char in enumerate(chars):
        game_win_dict[char] = []

        start_index = char_index + 1
        if start_index >= len(chars):
            start_index = 0
        end_index = char_index + value_len
        if end_index >= len(chars):
            end_index = end_index - len(chars)

        for i in range(start_index, start_index + value_len):
            curr_i = i
            if i >= len(chars):
                curr_i = i - len(chars)
            game_win_dict[char].append(chars[curr_i])
    return game_win_dict


def main():
    """
    Entry point of the game

    Returns:
         None
    """

    game_chars = ['rock', 'paper', 'scissors']
    game_options = ['!exit', '!rating']
    random.seed(2021)
    user_name = input("Enter your name: ").lower()
    print(f"Hello, {user_name}")
    user_chars = input("Enter your game characters separated by comma. Rock, Paper, Scissors will be used by default.\n")
    user_chars = user_chars.split(',')
    if len(user_chars) > 0 and len(user_chars[0]) > 0:
        game_chars = user_chars

    game_win_dict = build_game_dict(game_chars)
    print(game_win_dict)
    print("okay, let's start.")
    user_score = 0
    add_user = True
    # list of user ratings
    ratings = []
    # index of current user in the ratings list
    user_index = -1
    try:
        with open('rating.txt', 'r') as f:
            ratings = f.readlines()
            for curr_index, rating in enumerate(ratings):
                rating = rating.strip('\n')
                user, score = rating.split(' ')
                if user.lower() == user_name:
                    user_index = curr_index
                    user_score = int(score)
                    add_user = False
                    break
    except FileNotFoundError:
        file = open('rating.txt', 'w')
        file.close()
    if add_user:
        print(f"Welcome to ROCK, PAPER, SCISSORS {user_name} !")
        with open('rating.txt', 'a+') as f:
            user_rating_info = f"{user_name} 0\n"
            f.write(user_rating_info)
            ratings.append(user_rating_info)
    while True:
        comp_pick = game_chars[random.randint(0, len(game_chars)-1)]
        user_input = input().lower()
        if user_input not in game_chars and user_input not in game_options:
            print("Invalid input")
            continue
        if user_input == '!rating':
            print(user_score)
            continue
        if user_input == '!exit':
            print("Bye!")
            break
        add_points = get_result(user_input, comp_pick, game_win_dict).value
        print("Evaluating points...")
        # update points
        if add_points != 0:
            user_score = user_score + add_points
            ratings[user_index] = f"{user_name} {user_score}\n"
            with open('rating.txt', 'w') as f:
                f.writelines(ratings)
        print(f"Your new rating is {user_score}")


if __name__ == '__main__':
    main()
