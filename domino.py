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

def game_over(d_snake, player_p, comp_p):
    global status
    if not comp_p:
        print("Status:", game_state[3])
        exit()
    elif not player_p:
        print("Status:", game_state[4])
        exit()
    elif d_snake[0][0] == d_snake[-1][1]: 
        if len([j for i in d_snake for j in i if j == d_snake[0][0]]) == 8:
            print("Status:", game_state[2])
            exit()

def comp_count(s, c):
    count_elements = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for el in s + c:
        for i in el:
            for j in count_elements:
                if j == i:
                    count_elements[j] += 1
    return count_elements


def comp_scores(c, count):
    scores = {str(i): 0 for i in c}
    
    # Add total score for each pieces =>
    # count[int(piece[j])] => int(piece[j]) from '[0, 5]', piece[1] and piece[4] =>
    # score for count[0]; count[5] from  count{}
    for piece in scores:
        for j in range(1,5,3):
            scores[piece] += count[int(piece[j])] 

    scores = list(sorted(scores)) # Sort KEYs by score decrementally 
    scores.append(0) # 0 in case non of the pieces are valid
    
    return scores


def comp_move(d_snake, comp_p, stock_p):
    count = comp_count(d_snake, comp_p)
    scores = comp_scores(comp_p, count)

    for i in scores:
        if i == 0: 
            if stock_p:
                comp_p.append(stock_p.pop())
        else:
            f_elem, s_elem= int(i[1]), int(i[4])
            move = comp_p.index([f_elem,s_elem]) # Index of piece with highest score
            if d_snake[-1][1] == comp_p[move][0]:
                d_snake.append(comp_p.pop(move))
                break
            elif d_snake[-1][1] == comp_p[move][1]: # From left to right
                comp_p[move].insert(0, comp_p[move].pop(1))
                d_snake.append(comp_p.pop(move))
                break
            elif d_snake[0][0] == comp_p[move][1]:
                d_snake.insert(0, comp_p.pop(move))
                break
            elif (d_snake[0][0] == comp_p[move][0]):  # From right to left
                comp_p[move].append(comp_p[move].pop(0))
                d_snake.insert(0, comp_p.pop(move))
                break
       

    return stock_p, comp_p, d_snake


def next_move(d_snake, stock_p, player_p, comp_p):
    global status

    while True:
            if "Computer" in status:
                status = game_state[0]
                if input() == "":
                    move = comp_move(d_snake, comp_p, stock_p)
                else:
                    continue
                board(move[0], move[1], move[2], player_p)
                break
            else:
                try:
                    move = int(input())
                except ValueError: 
                    print("Invalid input. Please try again.")
                    continue
                if abs(move) > len(player_p):
                    print("Invalid input. Please try again.")
                    continue
                elif move == 0:
                    player_p.append(stock_p.pop())
                    status = game_state[1]
                    board(stock_p, comp_p, d_snake, player_p)
                else:
                    if 0 < move:
                        if d_snake[-1][1] == player_p[move - 1][0]:
                            d_snake.append(player_p.pop(move - 1))
                        elif d_snake[-1][1] == player_p[move - 1][1]: # From left to right
                            player_p[move - 1].insert(0, player_p[move - 1].pop(1))
                            d_snake.append(player_p.pop(move - 1))
                        else:
                            print("Illegal move. Please try again.")
                            continue
                        status = game_state[1]
                        board(stock_p, comp_p, d_snake, player_p)
                        break
                    elif 0 > move:
                        move = abs(move)
                        if d_snake[0][0] == player_p[move - 1][1]:
                            d_snake.insert(0, player_p.pop(move - 1))
                        elif d_snake[0][0] == player_p[move - 1][0]: # From right to left
                            player_p[move - 1].append(player_p[move - 1].pop(0))
                            d_snake.insert(0, player_p.pop(move - 1))
                        else:
                            print("Illegal move. Please try again.")
                            continue
                        status = game_state[1]
                        board(stock_p, comp_p, d_snake, player_p)
                        break


def draw_snake(snake):
    if len(snake) > 6:
        print(*snake[:3], "...", *snake[-3:], sep="", end="\n")
    else:
        print(*snake, sep="", end="\n")


def board(stock_p, comp_p, d_snake, player_p):
    global status
    print(70 * "=")
    print(f"Stock size: {len(stock_p)}")
    print(f"Computer pieces: {len(comp_p)}\n")

    draw_snake(d_snake)

    print("\nYour pieces:")
    for i in player_p:
        print(f"{player_p.index(i) + 1}:{i}")

    game_over(d_snake, player_p, comp_p) # Check for game end conditions

    print(f"Status: {status}")
    next_move(d_snake, stock_p, player_p, comp_p)


def main():
    global status

    domino_set = generate_set()  # Generate domino set
    stock_p = domino_set[:14]    # 14 stock elements
    comp_p = domino_set[14:21]   # 7 or 6 computer elements
    player_p = domino_set[21:]   # 6 or 7 domino elements
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
