import random
game_state = ["It's your turn to make a move. Enter your command.", "Computer is about to make a move. Press Enter to continue..."]
domino_snake = []
stock_pieces = []
player_pieces = []
computer_pieces = []
status = []


def generate_set():
    domino_set = [[i, j] for i in range(7) for j in range(7)]
    for i in domino_set:
        if i[::-1] in domino_set[domino_set.index(i) + 1:]:
            domino_set.remove(i[::-1])
    random.shuffle(domino_set)

    return domino_set


def end_game():  
    global status
    global computer_pieces
    global player_pieces

    if len(domino_snake) == 8 and domino_snake[0][0] == domino_snake[:-1][1]:
        if len([j for i in domino_snake for j in i if j == domino_snake[0][0]]) == 8:
            status = "The game is over. It's a draw!"
    elif not computer_pieces:
        status =  "The game is over. The computer won!"
    elif not player_pieces:
        status = "The game is over. You won!"

def player_move():
    global player_pieces
    global computer_pieces
    global domino_snake
    global stock_pieces
    global status
    end_game()
    print(f"Status: {status}")

    curr_player = computer_pieces if "Computer" in status else player_pieces

    while True:
        if status.endswith("!"):
            break 
        try:
            if "Computer" in status:
                status = game_state[0]
                usr_inp = input()
                if usr_inp == "":
                    move = random.randint(-len(computer_pieces), len(computer_pieces))
            else:
                move = int(input())
                if abs(move) > len(player_pieces):
                    print("Invalid input. Please try again.")
                    continue
                elif move == 0:
                    player_pieces.append(stock_pieces.pop())
                    game_display(stock_pieces, computer_pieces)
                    status = game_state[1]
                    player_move()
                
                status = game_state[1]

            if 0 <= move:
                # Decrese move to avoid index error
                domino_snake.append(curr_player.pop(move - 1))
                game_display(stock_pieces, computer_pieces)  # Display main board
                player_move()
            else:
                # Increase int(move) to avoid index error
                domino_snake.insert(0, curr_player.pop(abs(move + 1)))
                game_display(stock_pieces, computer_pieces)  # Display main board
                player_move()
          
        except:
            print("Invalid input. Please try again.")
            continue


def snake_display(snake):
    snake_str = ""
    if len(snake) > 6:
        snake.insert(3, "...")
        snake = snake[:4] + snake[-3:]
        for i in snake:
            snake_str = snake_str + str(i)
    else:
        snake_str = snake

    return snake_str


def game_display(stock_pieces, computer_pieces):
    print(f"""======================================================================
Stock size: {len(stock_pieces)}
Computer pieces: {len(computer_pieces)}
""")
    print("".join(str(i) for i in snake_display(domino_snake)))
    print("Your pieces:")

    for i in player_pieces:
        print(f"{player_pieces.index(i) + 1}:{i}")


def main():
    global player_pieces
    global computer_pieces
    global domino_snake
    global stock_pieces
    global status

    domino_set = generate_set()             # Generate domino set
    stock_pieces = domino_set[:14]          # 14 domino elements
    computer_pieces = domino_set[14:21]     # 7 or 6 domino elements
    player_pieces = domino_set[21:]         # 6 or 7 domino elements
    domino_snake = [i for i in computer_pieces + player_pieces if i[0] == i[1]]

    if domino_snake:
        if max(domino_snake) in computer_pieces:
            elem_index = computer_pieces.index(max(domino_snake))
            status = game_state[0]
            domino_snake = [computer_pieces.pop(elem_index)]
        else:
            elem_index = player_pieces.index(max(domino_snake))
            status = game_state[1]
            domino_snake = [player_pieces.pop(elem_index)]
    else:
        main()

    game_display(stock_pieces, computer_pieces)  # Display main board

    player_move()

main()
