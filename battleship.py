#This is a program that designs a game called battleship. Player will play against 3 different Ai and choose a spot to fire until all the ships are sunk.
import random #import random module
import sys #import sys module
def make_board(width, height):
    """
    make the board for the game
    @width: the width for the board, column
    @height: the height for the board, row
    @return: the board
    """
    board = [] #empty list first
    for num_row in range(height): #add rows
        row = ['*'] * width #add columns
        board.append(row)
    return board

def get_ship(file):
    """
    get the ship pairs from the file
    @file: the file containning the ships
    @return: the ship list with the ship pairs
    """
    with open(file) as ship: #open the file
        content = ship.readlines() 
        ship_placement = [] #empty list
        for line in content:
            symbol, row1, col1, row2, col2 = line.split() #unpack them
            row1 = int(row1) #make them int
            col1 = int(col1)
            row2 = int(row2)
            col2 = int(col2)
            ship_placement.append([symbol, row1, col1, row2, col2]) #add ship pairs
        return ship_placement

def check_ship_overlap(used_pairs, row1, col1, row2, col2, overlap):
    """
    check if ships overlap with given order pairs for ships
    @used_pairs: list containing used order pairs for ships
    @row1: the starting row for ship
    @row2: the ending row for ship
    @col1: the staring col for ship
    @col2: the ending col for ship
    @overlap: list containing overlapped ordered pairs
    @return: true if not overlap
    """
    if row1 == row2: #if ship is horizontal
        if col1 <= col2: #if staring col is the first col number
            for num_col in range(col1, col2 + 1): #iterate over all the order pairs of the ship getting pass
                if (row1, num_col) in used_pairs: #check if it is already used before
                    overlap.append((row1, num_col))#add it to overlap list
                    return False
            for num_col in range(col1, col2 + 1): #not used before and add all the pairs to used list
                used_pairs.append((row1, num_col))
        else: #if staring col is the second col number
            for num_col in range(col2, col1 + 1):
                if (row1, num_col) in used_pairs:
                    overlap.append((row1, num_col))
                    return False
            for num_col in range(col2, col1 +1):
                used_pairs.append((row1, num_col))
    elif col1 == col2: #if ship is vertical
        if row1 <= row2: #if staring row is the first row number
            for num_row in range(row1, row2 + 1):
                if (num_row, col1) in used_pairs:
                    overlap.append((num_row, col1))
                    return False
            for num_row in range(row1, row2 +1):
                used_pairs.append((num_row, col1))
        else: #if staring row is the second row number
            for num_row in range(row2, row1 + 1):
                if (num_row, col1) in used_pairs:
                    overlap.append((num_row, col1))
                    return False
            for num_row in range(row2, row1 +1):
                used_pairs.append((num_row, col1))
            
    return True

def check_ship_placement(board, ship_placement, error):
    """
    check if ship are placed in the right way
    @board: the board
    @ship_placement: list for ship pairs
    @error: list for ship placement error
    @return: True if valid ship placements
    """
    symbol_list = []
    start_row_col = []
    end_row_col = []
    row = len(board)
    col = len(board[0])
    valid_pairs = []
    overlap = []
    for num_row in range(row): #add all the valid pairs in the board to the list
        for num_col in range(col):
            valid_pairs.append((num_row, num_col))
    for ship in ship_placement: 
        symbol_list.append(ship[0]) #find each symbol for ship to the symbol list
        start_row_col.append((ship[1],ship[2])) #find all the staring rol and col number
        end_row_col.append((ship[3],ship[4])) #find all the ending rol and col number
    for symbol in symbol_list:
        if symbol == 'x' or symbol == 'X' or symbol == 'o' or symbol == 'O' or symbol == '*': #symbol can't be x, X, O, o or *
            return False
        if symbol_list.count(symbol) > 1: #can't have same symbol for multiple ships
            error.append('Error symbol %s is already in use. Terminating game' % symbol) #raised error
            return False
    used_pairs = []
    for placement_pair1, placement_pair2, symbol in zip(start_row_col, end_row_col, symbol_list): #get starting order pair and ending order pair respectively for the ship
        row1, col1 = placement_pair1 #unpacking
        row2, col2 = placement_pair2
        if (row1, col1) not in valid_pairs or (row2, col2) not in valid_pairs: #ship must be on the board
            error.append('Error %s is placed outside of the board. Terminating game.' % symbol) #raise error
            return False
        if row1 != row2 and col1 != col2: #ship can not be placed diagonally
            error.append('Ships cannot be placed diagonally. Terminating game.')
            return False
        if not check_ship_overlap(used_pairs, row1, col1, row2, col2, overlap):#check if ships are overlapped
            overlap_ship = overlap[0]
            error.append('There is already a ship at location %d, %d. Terminating game.' % (overlap_ship[0], overlap_ship[1])) #raise error
            return False
    return True

def AI_ship_placements(board, ship_placement):
    """
    make the list for the AI ship placements
    @board: the board
    @ship_placement: the list for the player ship placements
    @return: the list for the AI ship placements
    """
    row = len(board) #find the number of row for the board
    col = len(board[0]) #find the number of col for the board
    used_pairs = [] #list for used placements
    AI_ship_placement = []
    symbol_and_shiplen = {} #dictionary for the symbol and the ship length of each ship
    overlap = [] #overlap list
    for ship in ship_placement: #make the symbol and shiplength dictionary
        symbol, row1, col1, row2, col2 = ship #unpack
        ship_len = ((row1 - row2) ** 2 + (col1 - col2) ** 2) ** (1/2) #calculate ship length
        ship_len = int(ship_len) #make it int 
        symbol_and_shiplen[symbol] = ship_len #add it to dictionary
    for symbol in sorted(symbol_and_shiplen.keys()): #sort the symbols and we are using the same symbol for AI ships
        ship_len = symbol_and_shiplen[symbol] #find the shiplength for the ship
        direction = random.choice(['vert', 'horz']) #decide the direction of the ship
        if direction == 'vert':
            AI_row1 = random.randint(0, row - ship_len -1) #have to make it inside the board, row first and then col
            AI_col1 = random.randint(0, col - 1)
            AI_col2 = AI_col1
            AI_row2 = AI_row1 + ship_len
        elif direction == 'horz':
            AI_row1 = random.randint(0, row - 1) #have to make it inside the board, row first and then col
            AI_col1 = random.randint(0, col- ship_len - 1)
            AI_row2 = AI_row1
            AI_col2 = AI_col1 + ship_len
        while not check_ship_overlap(used_pairs, AI_row1, AI_col1, AI_row2, AI_col2, overlap): #check if it overlaps with other ships
            direction = random.choice(['vert', 'horz']) #find the direction again
            if direction == 'vert':
                AI_row1 = random.randint(0, row - ship_len -1) #find row and col again
                AI_col1 = random.randint(0, col - 1)
                AI_col2 = AI_col1
                AI_row2 = AI_row1 + ship_len
            elif direction == 'horz':
                AI_row1 = random.randint(0, row - 1)
                AI_col1 = random.randint(0, col- ship_len - 1)
                AI_row2 = AI_row1
                AI_col2 = AI_col1 + ship_len
        AI_ship_placement.append([symbol, AI_row1, AI_col1, AI_row2, AI_col2]) #add it to the AI ship list
    return AI_ship_placement
        
def display_board(board, AI_board):
    """
    display the board the AI board
    @board: player board
    @AI_board: AI board
    """
    print('Scanning Board') #print AI board
    print(' ', end = '')
    for col_num in range(len(AI_board[0])):
        print('', col_num, end= '')
    print()
    for row_num, row in enumerate(AI_board):
        print(row_num, ' '.join(row))
    print()
    print('My Board') 
    print(' ', end = '')  #print player board
    for col_num in range(len(board[0])):
        print('', col_num, end= '')
    print()
    for row_num, row in enumerate(board):
        print(row_num, ' '.join(row))
    print()
    
def game_over(ship_list, AI_ship_list):
    """
    check if game is over
    @ship_list: the list containing all the ship order pairs for player
    @AI_ship_list: the list containing all the ship order pairs for AI
    @return: true if over
    """
    if player_win(AI_ship_list) or AI_win(ship_list): #either player wins or AI wins
        return True
    else:
        return False
    
def player_win(AI_ship_list):
    """
    check if player wins
    @AI_ship_list: the list containing all the ship order pairs for AI
    @return: true if player wins
    """
    for ship in AI_ship_list: #all the ship order pairs are destroyed
        if not ship == []:
            return False
    else:
        return True

def AI_win(ship_list):
    """
    check if AI wins
    @ship_list: the list containing all the ship order pairs for player
    """
    for ship in ship_list: #all the ship order pairs are destroyed
        if not ship == []:
            return False
    else:
        return True
    
def symbols(ship_placement):
    """
    make a list for all the symbols for each ship
    @ship_placement: list for all the ship information
    @return: the symbol for ship list
    """
    symbol = []
    for ship in ship_placement: #add symbol to list
        symbol.append(ship[0])
    return symbol

def destory_ship(symbol_copy, symbol_list, ship_list):
    """
    check if there is a ship being destroyed
    @symbol_copy: a copy for the symbol list for ship
    @symbol_copy: symbol list for ship
    @ship_list: the list containing all the ship order pairs
    @return: -1 if not destroyed, the index number for the ship in the symbol list
    """
    for num_ship, ship in enumerate(ship_list):
        symbol = symbol_list[num_ship]
        if symbol in symbol_copy and ship == []: #make sure it will not show up again for the ship that is already sunk
            symbol_copy.remove(symbol) #use copy so we dont make change to the symbol list
            return num_ship
    else:
        return -1
        
def check_if_hit(ship_list, move):
    """
    check if a move hit a ship
    @ship_list: the list containing all the ship order pairs
    @move: the move made by player or AI
    @return: true if hit
    """
    for ship in ship_list: 
        if move in ship:
            ship.remove(move)
            return True
    else:
        return False

def ship_pair_lists(ship_placement):
    """
    make a list containing all the order pairs for the ships
    @ship_placement: the list containing the ships information
    @return: the list containing allt he order pairs for the ships 
    """
    ship_list = [] #empty at first
    for ship in ship_placement:
        symbol, row1, col1, row2, col2 = ship #unpack
        placed_pairs= []
        if row1 == row2: #if ship is horizontal
           if col1 <= col2: #if the first col number is smaller
               for num_col in range(col1, col2 + 1): #go over all the pairs between the first one and the last one
                   placed_pairs.append((row1, num_col))
               ship_list.append(placed_pairs) #add it to list
           else:
               for num_col in range(col2, col1 + 1): #if the last col number is smaller
                   placed_pairs.append((row1, num_col))
               ship_list.append(placed_pairs)
        elif col1 == col2: #if ship is vertical
           if row1 <= row2: #if the first row number is smaller
               for num_row in range(row1, row2 + 1):
                   placed_pairs.append((num_row, col1))
               ship_list.append(placed_pairs)
           else: #if the last row number is smaller
               for num_row in range(row2, row1 + 1):
                   placed_pairs.append((num_row, col1))
               ship_list.append(placed_pairs)
    return ship_list
            
def valid_move(board, move):
    """
    check if player makes a valid move
    @board: the board for AI
    @move: player move
    @return: true if valid move
    """
    move = move.split() #split the move
    board_row = len(board) #find the number of row
    board_col = len(board[0])#find the number col
    if len(move) != 2: #move has to have 2 elements
        return False
    (row, col) = move #unpack
    if not row.isdigit(): #row has to be a integer
        return False
    if not col.isdigit(): #col has to be a integer
        return False
    row = int(row) #safe to convert them into int
    col = int(col)
    if row not in range(board_row) or col not in range(board_col): #has to be on the board
        return False
    if board[row][col] != '*': #has to be a spot that has not been hit yet
        return False
    return True

def get_move(board):
    """ 
    get player move
    @board: the board of AI
    @return: the move in tuple
    """
    move = '' #make sure to go in the while loop to get a valid move
    while not valid_move(board, move):
        move = input('Enter row and column to fire on separated by a space: ') #ask for input again if not valid
    (row, col) = move.split() #unpack
    row = int(row) #safe to convert int
    col = int(col)
    return (row, col)
    
def make_move(move, board, piece):
    """
    make the move on the board
    @move: move of AI or player
    @board: the board of AI or player
    @piece: 'X' for hit, 'O' for miss
    """
    row, col= move #unpack
    board[row][col] = piece #make the change on the board
    
def get_AI_move_3(valid_spots, ship_list):
    """  
    get AI move if AI is cheater mode
    @valid_spots: list containing all the available spots for firing
    @ship_list: the list containing all the ship order pairs
    @return: the move for AI 3
    """
    AI_move = ''
    for spots in valid_spots: #go over all the available spots row by row
        for ship in ship_list: #go over all the order pairs for ship
            if spots in ship: #if matched
                AI_move = spots 
                break #just want the first matched move
        if AI_move == spots:
            break
    return AI_move

def get_AI_move_2(destroy_list):
    """
    get AI move if AI is second mode
    @destroy_list: the list for available spots for destroy mode
    @return: the move for AI 3 in destroy mode
    """
    AI_move = destroy_list[0] #get the first element as move
    return AI_move
    
def add_destroy_list(AI_move, destroy_list, valid_spots):
    """
    add 4 spots to the destroy list for destroy mode if hit
    @AI_move: AI move
    @destroy_list: the list for available spots for destroy mode
    @valid_spots: list containing all the available spots for firing
    """
    row, col = AI_move #unpack the move
    if (row - 1, col) not in destroy_list: #check if the order pair has already been added, cant have 2 same order pair
        destroy_list.append((row - 1, col))
    if (row + 1, col) not in destroy_list:
        destroy_list.append((row + 1, col))
    if (row, col - 1) not in destroy_list:
        destroy_list.append((row, col - 1))
    if (row, col + 1) not in destroy_list:
        destroy_list.append((row, col + 1))
    for spots in destroy_list.copy(): #and the order pair has also to be on the board
        if spots not in valid_spots:
            destroy_list.remove(spots) #if not remove it
            

def get_AI_move_1(valid_spots):
    """
    get  AI move if AI is simple
    @valid_spots: list containing all the available spots for firing
    @return: the move for AI 1
    """
    AI_move = random.choice(valid_spots) #random choose a move in the valid spots
    valid_spots.remove(AI_move) #remove it after firing it
    return AI_move

def valid_int(number):
    """
    check if it is a valid integer
    @number: the element that will be checked
    @return: true if valid integer
    """
    number = number.strip() #strip whitespace
    if len(number)== 0: #cant be empty string
        return False
    else:
        return (number.isdigit() or (number.startswith('-') and number[1:].isdigit())) #all number and negative number is also ok

def game_play():
    """
    the main program for the game
    """
    seed = input('Enter the seed: ') #ask for the seed 
    while not valid_int(seed):  # keep asking if not valid seed
        seed = input('Enter the seed: ')
    seed = int(seed) #safe to convert int
    random.seed(seed) #set the random seed
    width = input('Enter the width of the board: ') #ask for the width for the board
    while not (valid_int(width) and int(width) > 0): #keep asking if not valid width
        width = input('Enter the width of the board: ')
    height = input('Enter the height of the board: ') #ask for the height for the board
    while not (valid_int(height) and int(height) > 0): #keep asking if not valid height
        height = input('Enter the height of the board: ')
    width = int(width) #safe to convert int
    height = int(height)
    board = make_board(width, height) #make board for player
    AI_board = make_board(width, height) #make board for AI
    file = input('Enter the name of the file containing your ship placements: ') #ask for the file
    AI = input('Choose your AI.\n1. Random\n2. Smart\n3. Cheater\n Your choice: ') #ask for the AI mode
    while AI not in ['1', '2', '3']: #if not valid AI mode keep asking
        AI = input('Choose your AI.\n1. Random\n2. Smart\n3. Cheater\n Your choice: ')
    ship_placement = get_ship(file) #get ship placements for player
    error = []
    if not check_ship_placement(board, ship_placement, error): #check if valid ship placements, if not terminate the program
        for errors in error:
            print(errors)
        sys.exit(0)
    AI_ship_placement = AI_ship_placements(board, ship_placement) #get ship placements for AI
    turn = random.randint(0, 1) #decide the first turn
    ship_list = ship_pair_lists(ship_placement)#get all the order pairs for player's ships
    AI_ship_list = ship_pair_lists(AI_ship_placement)#get all the order pairs for AI's ships
    symbol_list = symbols(ship_placement) #get the list of symbols for player's ships
    AI_symbol_list = sorted(symbol_list) #get the list of symbols for AI's ships
    symbol_copy = symbol_list.copy() #get a copy of it
    AI_symbol_copy = AI_symbol_list.copy()#get a copy of it for future use
    destroy_list = []
    valid_spots = []
    for num_row in range(height): #add all the valid spots to the list
        for num_col in range(width):
            valid_spots.append((num_row, num_col))
    for ship in AI_ship_placement: #print the location of AI ships
            print('Placing ship from %d,%d to %d,%d.' % (ship[1], ship[2], ship[3], ship[4]))
    for ship, symbol in zip(ship_list, symbol_list): #display all the ships in player's board
            for ship_pair in ship:
                board[ship_pair[0]][ship_pair[1]] = symbol
    if turn == 0: #if player plays first
        display_board(board, AI_board) #display boards
    while not game_over(ship_list, AI_ship_list): #while game is still on
        if turn == 1: #if it's AI's turn
            if AI == '1': #if it is AI 1
                AI_move = get_AI_move_1(valid_spots) #get move
                if check_if_hit(ship_list, AI_move): #check if hit
                    num_ship = destory_ship(symbol_copy, symbol_list, ship_list) # check if ships are destroyed
                    if not num_ship == -1:
                        print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                        print('You sunk my %s' % symbol_list[num_ship])
                        piece = 'X'
                        make_move(AI_move, board, piece)#update the board
                    else: # if no ships being destroyed
                        print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                        print('Hit!')
                        piece = 'X'
                        make_move(AI_move, board, piece) #update board
                else: #if not hit
                    print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                    print('Miss!')
                    piece = 'O'
                    make_move(AI_move, board, piece)#update board
            elif AI == '2': # if it's AI 2
                if destroy_list == []: #if AI is in hunt mode
                    AI_move = get_AI_move_1(valid_spots) #get move like AI 1
                    if check_if_hit(ship_list, AI_move): #check if hit
                        add_destroy_list(AI_move, destroy_list, valid_spots) #hit and then add spots to destroy list and start destroy mode
                        num_ship = destory_ship(symbol_copy, symbol_list, ship_list) #check if ships are destroyed
                        if not num_ship == -1:
                            print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #prnt results
                            print('You sunk my %s' % symbol_list[num_ship])
                            piece = 'X'
                            make_move(AI_move, board, piece) #make move to the board
                        else: #no ships being destroyed
                            print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                            print('Hit!')
                            piece = 'X'
                            make_move(AI_move, board, piece) #make move to the board
                    else: #if miss
                        print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                        print('Miss!')
                        piece = 'O'
                        make_move(AI_move, board, piece)#update board
                else: #if AI is in hunt mode
                    AI_move = get_AI_move_2(destroy_list) #get move from the destroy list
                    destroy_list.remove(AI_move)#remove the move from destroy list avoing getting the same move next turn
                    if AI_move in valid_spots: #check if it is valid move
                        valid_spots.remove(AI_move) 
                    if check_if_hit(ship_list, AI_move): #check if hit
                        add_destroy_list(AI_move, destroy_list, valid_spots) #hit continue to add to destroy list
                        num_ship = destory_ship(symbol_copy, symbol_list, ship_list) #check if ships being destroyed
                        if not num_ship == -1: #ships being destroyed
                            print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                            print('You sunk my %s' % symbol_list[num_ship])
                            piece = 'X'
                            make_move(AI_move, board, piece)#update board
                        else: # no ships being destroyed
                            print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                            print('Hit!')
                            piece = 'X'
                            make_move(AI_move, board, piece) #update board
                    else: #if miss
                        print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #pritn results
                        print('Miss!')
                        piece = 'O'
                        make_move(AI_move, board, piece) #update board
            elif AI == '3': #if AI is cheater
                AI_move = get_AI_move_3(valid_spots, ship_list)#get move from ship_list
                if check_if_hit(ship_list, AI_move):#check if hit
                    num_ship = destory_ship(symbol_copy, symbol_list, ship_list)#check if ships are destroyed
                    if not num_ship == -1: 
                        print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                        print('You sunk my %s' % symbol_list[num_ship])
                        piece = 'X'
                        make_move(AI_move, board, piece) #update board
                    else: # no ships being destroyed
                        print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1]))
                        print('Hit!')
                        piece = 'X'
                        make_move(AI_move, board, piece)#update board
                else: #if not hit
                    print('The AI fires at location (%d, %d)' % (AI_move[0], AI_move[1])) #print results
                    print('Miss!')
                    piece = 'O'
                    make_move(AI_move, board, piece)#update board
            display_board(board, AI_board) #display boards
        if turn == 0: #if its player's turn
            move = get_move(AI_board) #get move
            if check_if_hit(AI_ship_list, move): #check if hit
                num_ship = destory_ship(AI_symbol_copy, AI_symbol_list, AI_ship_list) #check if ships are destroyed
                if not num_ship == -1: 
                    print('You sunk my %s' % AI_symbol_list[num_ship])#print results
                    piece = 'X'
                    make_move(move, AI_board, piece)#update board
                else: #if no ships being destroyed
                    print('Hit!') #print results
                    piece = 'X'
                    make_move(move, AI_board, piece)#update board
            else: #if miss
                print('Miss!') #print results
                piece = 'O'
                make_move(move, AI_board, piece) #update board
            
        turn = (turn + 1) % 2 #change turn
    if player_win(AI_ship_list): #check who wins
                  display_board(board, AI_board)
                  print('You win!')
    elif AI_win(ship_list):
                  print('The AI wins.')
game_play() #run the program
