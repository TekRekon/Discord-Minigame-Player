import math

nodesExplored = 0

# bitboards = [0, 0]
# height = [0, 7, 14, 21, 28, 35, 42]
# counter = 0
# prevMoves = []
# firstPlayer = None
#
#
# def makeMove(col):
#     global counter
#     global height
#     global bitboards
#     move = 1 << height[col]
#     height[col] += 1
#     bitboards[counter & 1] ^= move
#     prevMoves.append(col)
#     counter += 1
#
#
# def undoMove():
#     global counter
#     global height
#     global bitboards
#     counter -= 1
#     col = prevMoves[counter]
#     height[col] -= 1
#     move = 1 << height[col]
#     bitboards[counter & 1] ^= move
#
#
# def isWin(bitboard):
#     directions = [1, 7, 6, 8]
#     for direction in directions:
#         bb = bitboard & (bitboard >> direction)
#         if bb & (bb >> (2 * direction)) != 0:
#             return True
#     return False
#
#
# def listValidMoves():
#     moves = []
#     TOP = 0b01000000100000010000001000000100000010000001000000
#     for i in range(0, 7):
#         if ((TOP & (1 << height[i])) == 0):
#             moves.append(i)
#     return moves
#
#
# def encrypt(string, length):
#     return ' '.join(string[i:i+length] for i in range(1, len(string), length))
#
#
# for n in bitboards:
#     bit = '{:064b}'.format(n)
#     print(encrypt(str(bit), 7))
# print(prevMoves)

# class Main {
# public static void main(String[] args) {
# long move = 1L << 0;
# for(int i = 0; i < Long.numberOfLeadingZeros((long)move); i++) {
# System.out.print('0');
# }
# System.out.println(Long.toBinaryString((long)move));
# System.out.println(move);
# }
# }

def convert(emoji):
    if emoji == 'X':
        return '🔴'
    elif emoji == 'O':
        return '🔵'
    elif emoji == '🔵':  # Blue
        return 'O'
    elif emoji == '🔴':  # Red
        return 'X'
    elif emoji == '⚪':  # White
        return ' '
    elif emoji == ' ':
        return '⚪'
    else:
        return emoji


def getValidLocations(board, playerPiece, botPiece):
    validMoves = []
    badMoves = []
    for i in range(0, 7):
        column = [row[i] for row in board]
        for n in reversed(range(0, 6)):
            if list(column)[n] == ' ':

                # Single turn win anticipation
                board[n][i] = botPiece
                if checkBoardWin(board) == botPiece:
                    validMoves = [[n, i]]
                    board[n][i] = ' '
                    return validMoves, True

                # Single turn loss anticipation
                board[n][i] = playerPiece
                if checkBoardWin(board) == playerPiece:
                    validMoves = [[n, i]]
                    board[n][i] = ' '
                    return validMoves, True

                # Double turn loss anticipation
                board[n][i] = botPiece
                for k in range(0, 7):
                    column = [row[k] for row in board]
                    for j in reversed(range(0, 6)):
                        if list(column)[j] == ' ':
                            board[j][k] = playerPiece
                            if checkBoardWin(board) == playerPiece:
                                badMoves.append([n, i])
                            board[j][k] = ' '
                            break
                if [n, i] not in badMoves:
                    # Toward-Middle-of-Board Based Move Ordering #
                    for k in range(0, len(validMoves)+1):
                        if k+1 >= len(validMoves)+1:
                            validMoves.append([n, i])
                            break
                        if abs(i - 3) <= abs(validMoves[k][1] - 3):
                            validMoves.insert(k, [n, i])
                            break
                board[n][i] = ' '
                break

    if (len(validMoves)) == 0:
        return badMoves, False

    # Heuristic-Based Move Ordering (Doesn't rlly work) #
    # sortedValidMoves = []
    # sortedMoveValues = []
    # for move in validMoves:
    #     board[move[0]][move[1]] = botPiece
    #     currentHeuristic = boardHeuristic(board, botPiece, playerPiece)
    #     for i in range(0, len(sortedMoveValues)+1):
    #         if i+1 >= len(sortedMoveValues)+1:
    #             sortedMoveValues.append(currentHeuristic)
    #             sortedValidMoves.append(move)
    #             break
    #         if currentHeuristic <= sortedMoveValues[i]:
    #             sortedMoveValues.insert(i, currentHeuristic)
    #             sortedValidMoves.insert(i, move)
    #             break
    #     board[move[0]][move[1]] = ' '


    return validMoves, False


def convertBoard(board, simple):
    if simple:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in ['🔵', '🔴', '⚪']:
                    board[i][j] = convert(board[i][j])

    else:
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] in ['X', 'O', ' ']:
                    board[i][j] = convert(board[i][j])


def getPosValue(i, j):
    multipier = 2
    if i == 5 or i == 0:
        if j == 3:
            return 7*multipier
        if j == 2 or j == 4:
            return 5*multipier
        if j == 1 or j == 5:
            return 4*multipier
        else:
            return 3*multipier

    if i == 4 or i == 1:
        if j == 3:
            return 10*multipier
        if j == 2 or j == 4:
            return 8*multipier
        if j == 1 or j == 5:
            return 6*multipier
        else:
            return 4*multipier

    else:
        if j == 3:
            return 13*multipier
        if j == 2 or j == 4:
            return 11*multipier
        if j == 1 or j == 5:
            return 8*multipier
        else:
            return 5*multipier


def boardHeuristic(board, bot_mark, p_mark):
    pScore = 0
    botScore = 0
    for n, list in enumerate(board):
        for i, cell in enumerate(list):
            if cell in ['X', 'O']:
                pieceValue = 0

                # Single Piece Value
                pieceValue += getPosValue(n, i)

                if i < 4:
                    # (3) horizontal holes
                    if board[n][i + 1] == ' ' and board[n][i] == board[n][i + 2] == board[n][i + 3]:
                        pieceValue += 200
                    elif board[n][i + 2] == ' ' and board[n][i] == board[n][i + 1] == board[n][i + 3]:
                        pieceValue += 200

                    # (3) horizontal
                    if board[n][i] == board[n][i + 1] == board[n][i + 2]:
                        if i != 3:
                            if board[n][i + 3] == ' ':
                                pieceValue += 200
                        if i != 0:
                            if board[n][i - 1] == ' ':
                                pieceValue += 200

                    if n > 2:
                        # (3) up right holes
                        if board[n - 1][i + 1] == ' ' and board[n][i] == board[n - 2][i + 2] == board[n - 3][i + 3]:
                            pieceValue += 200
                        elif board[n - 2][i + 2] == ' ' and (board[n][i] == board[n - 1][i + 1] == board[n - 3][i + 3]):
                            pieceValue += 200

                        # (3) up right
                        if board[n][i] == board[n - 1][i + 1] == board[n - 2][i + 2]:
                            if n != 5 and i != 0:
                                if board[n + 1][i - 1] == ' ':
                                    pieceValue += 200
                            if board[n - 3][i + 3] == ' ':
                                pieceValue += 200

                        # (3) up left
                        if board[n][i] == board[n - 1][i - 1] == board[n - 2][i - 2]:
                            if n != 5 and i != 6:
                                if board[n + 1][i + 1] == ' ':
                                    pieceValue += 200
                            if board[n - 3][i - 3] == ' ':
                                pieceValue += 200

                if i > 2 and n > 2:
                    # (3) up left holes
                    if board[n - 1][i - 1] == ' ' and board[n][i] == board[n - 2][i - 2] == board[n - 3][i - 3]:
                        pieceValue += 200
                    elif board[n - 2][i - 2] == ' ' and board[n][i] == board[n - 1][i - 1] == board[n - 3][i - 3]:
                        pieceValue += 200

                # (3) vertical
                if n < 4 and board[n][i] == board[n + 1][i] == board[n + 2][i]:
                    if n != 0:
                        if board[n - 1][i] == ' ':
                            pieceValue += 180

                # if n > 0:
                #     if i < 6:
                #         # (2) up right
                #         if board[n][i] == board[n - 1][i + 1]:
                #             if n != 1 and i != 5:
                #                 if board[n - 2][i + 2] == ' ':
                #                     pieceValue += 50
                #             if n != 5 and i != 0:
                #                 if board[n + 1][i - 1] == ' ':
                #                     pieceValue += 50

                    # if i > 0:
                    #     # (2) up left
                    #     if board[n][i] == board[n - 1][i - 1]:
                    #         if n != 1 and i != 1:
                    #             if board[n - 2][i - 2] == ' ':
                    #                 pieceValue += 50
                    #             if i != 6 and n != 5:
                    #                 if board[n + 1][i + 1] == ' ':
                    #                     pieceValue += 50

                # if n < 5:
                #     # (2) vertical
                #     if board[n][i] == board[n + 1][i]:
                #         if n > 0:
                #             if board[n - 1][i] == ' ':
                #                 pieceValue += 25

                # if i < 6:
                #     # (2) horizontal
                #     if board[n][i] == board[n][i + 1]:
                #         if i != 5:
                #             if board[n][i + 2] == ' ':
                #                 pieceValue += 50
                #         if i != 0:
                #             if board[n][i - 1] == ' ':
                #                 pieceValue += 50

                if cell == bot_mark:
                    botScore += pieceValue
                elif cell == p_mark:
                    pScore += pieceValue
    return botScore - pScore


def minimax(board, depth, isMaximizing, bot_mark, p_mark, alpha, beta):
    global nodesExplored
    result = checkBoardWin(board)
    # print(f'{board[0]} \n {board[1]} \n {board[2]} \n {board[3]} \n {board[4]} \n {board[5]}')
    if result == 'TIE':
        return 0
    elif result == bot_mark:
        return 100000000000000000000000000000
    elif result == p_mark:
        return -100000000000000000000000000000
    elif depth == 0:
        return boardHeuristic(board, bot_mark, p_mark)

    nodesExplored += 1

    if isMaximizing:
        bestScore = -math.inf
        moves, bool = getValidLocations(board, p_mark, bot_mark)
        for move in moves:
            board[move[0]][move[1]] = bot_mark
            bestScore = max(bestScore, minimax(board, depth - 1, not isMaximizing, bot_mark, p_mark, alpha, beta))
            alpha = max(alpha, bestScore)
            board[move[0]][move[1]] = ' '
            if beta <= alpha:
                break
        return bestScore
    else:
        bestScore = math.inf
        moves, bool = getValidLocations(board, p_mark, bot_mark)
        for move in moves:
            board[move[0]][move[1]] = p_mark
            bestScore = min(bestScore, minimax(board, depth - 1, not isMaximizing, bot_mark, p_mark, alpha, beta))
            beta = min(beta, bestScore)
            board[move[0]][move[1]] = ' '
            if beta <= alpha:
                break
        return bestScore


def bestMove(board, botMark, pMark, depth):
    global nodesExplored
    bestScore = -math.inf
    bestMove = []
    moves, shortened = getValidLocations(board, pMark, botMark)
    for move in moves:
        board[move[0]][move[1]] = botMark
        score = minimax(board, depth, False, botMark, pMark, -math.inf, math.inf)
        board[move[0]][move[1]] = ' '
        if score > bestScore:
            bestScore = score
            bestMove = [move[0], move[1]]
    return bestMove, shortened, nodesExplored


def checkBoardWin(board):
    for n, list in enumerate(board):
        for i, cell in enumerate(list):
            if cell in ['X', 'O']:
                if i < 4 and n > 2 and (board[n][i] == board[n - 1][i + 1] == board[n - 2][i + 2] == board[n - 3][i + 3]):
                    return cell
                if i > 2 and n > 2 and (board[n][i] == board[n - 1][i - 1] == board[n - 2][i - 2] == board[n - 3][i - 3]):
                    return cell
                if n < 3 and (board[n][i] == board[n + 1][i] == board[n + 2][i] == board[n + 3][i]):
                    return cell
                if i < 4 and (board[n][i] == board[n][i + 1] == board[n][i + 2] == board[n][i + 3]):
                    return cell
                if n == 0 and ' ' not in board[n]:
                    return 'TIE'
    return 'NO_END'
