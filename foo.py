import random


game_state = [
    "It's your turn to make a move. Enter your command.",
    "Computer is about to make a move. Press Enter to continue...",
    "The game is over. It's a draw!",
    "The game is over. The computer won!",
    "The game is over. You won!",
]
status = []


def generate_set():
    domino_set = [[i, j] for i in range(7) for j in range(7)]
    for i in domino_set:
        if i[::-1] in domino_set[domino_set.index(i) + 1 :]:
            domino_set.remove(i[::-1])
    random.shuffle(domino_set)

    return domino_set


def draw_snake(snake):
    if len(snake) > 6:
        print(*snake[:3], "...", *snake[-3:], sep="", end="\n")
    else:
        print(*snake, sep="", end="\n")


def board(stock_p, comp_p, d_snake, player_p):
    print(70 * "=")
    print(f"Stock size: {len(stock_p)}")
    print(f"Computer pieces: {len(comp_p)}")

    draw_snake(d_snake)

    print("Your pieces:")
    for i in player_p:
        print(f"{player_p.index(i) + 1}:{i}")

    player_move(d_snake, stock_p, player_p, comp_p)


def game_over(d_snake, player_p, comp_p):
    global status
    if len(d_snake) == 8 and d_snake[0][0] == d_snake[:-1][1]:
        if len([j for i in d_snake for j in i if j == d_snake[0][0]]) == 8:
            status = game_state[2]
    elif not comp_p:
        status = game_state[3]
    elif not player_p:
        status = game_state[4]


def player_move(d_snake, stock_p, player_p, comp_p):
    global status

    game_over(d_snake, player_p, comp_p) # Check for game end conditions
    print(f"Status: {status}")
    curr_player = comp_p if "Computer" in status else player_p

    while True:
        if status.endswith("!"):
            break
        try:
            if "Computer" in status:
                status = game_state[0]
                usr_inp = input()
                if usr_inp == "":
                    move = random.randint(-len(comp_p), len(comp_p))
            else:
                move = int(input())
                if abs(move) > len(player_p):
                    print("Invalid input. Please try again.")
                    continue
                elif move == 0:
                    player_p.append(stock_p.pop())
                    status = game_state[1]
                    board(stock_p, comp_p, d_snake, player_p)

                status = game_state[1]
            if 0 < move:
                d_snake.append(curr_player.pop(move - 1))
                board(stock_p, comp_p, d_snake, player_p)
            else:
                d_snake.insert(0, curr_player.pop(abs(move + 1)))
                board(stock_p, comp_p, d_snake, player_p)
        except:
            print("Invalid input. Please try again.")
            continue


def main():
    global status

    domino_set = generate_set()  # Generate domino set
    stock_p = domino_set[:14]  # 14 stock elements
    comp_p = domino_set[14:21]  # 7 or 6 computer elements
    player_p = domino_set[21:]  # 6 or 7 domino elements
    # Create list of doubles from computer and player pieces.
    domino_snake = [i for i in comp_p + player_p if i[0] == i[1]]

    if domino_snake:
        if max(domino_snake) in comp_p:
            domino_snake = [comp_p.pop(comp_p.index(max(domino_snake)))]
            status = game_state[0]
        else:
            domino_snake = [player_p.pop(player_p.index(max(domino_snake)))]
            status = game_state[1]
    else:
        main()

    board(stock_p, comp_p, domino_snake, player_p)


main()
