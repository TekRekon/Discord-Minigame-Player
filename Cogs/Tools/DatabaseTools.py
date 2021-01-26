import psycopg2


def fetchRankedStats(mode):
    # TODO implement stert point for this method
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    if mode == 'connect4':
        cur.execute("SELECT username, win_percent, wins, losses, user_id FROM playerconnect4stats ORDER BY win_percent DESC")
    else:
        cur.execute("SELECT username, win_percent, wins, losses, user_id FROM playertictactoestats ORDER BY win_percent DESC")

    rows = cur.fetchall()

    cur.close()
    con.close()

    scores = []
    for r in rows:
        if r[2] + r[3] > 9:
            scores.append([r[0], r[1], r[2], r[3], r[4]])

    return scores

def getPlayerStat(player_id, data, mode):
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    if mode == "connect4":
        cur.execute("SELECT username, wins, losses, win_percent FROM playerConnect4Stats WHERE user_id = %s", [player_id])
    else:
        cur.execute("SELECT username, wins, losses, win_percent FROM playertictactoestats WHERE user_id = %s", [player_id])
    user = cur.fetchall()

    cur.close()
    con.close()

    if data == "username":
        return user[0][0]
    if data == "wins":
        return user[0][1]
    elif data == "losses":
        return user[0][2]
    elif data == "win_rate":
        return user[0][3]
    elif data == 'all':
        return [user[0][0], user[0][1], user[0][2], user[0][3]]

def addPlayer(player_id, name, mode):
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()
    cont = False
    if mode == 'connect4':
        cur.execute("SELECT EXISTS(SELECT 1 FROM playerconnect4stats WHERE user_id = %s)", [player_id])
        player_exist = cur.fetchall()
        if not player_exist[0][0]:
            new_player = (
                "INSERT INTO playerConnect4Stats (user_id, username, wins, losses, win_percent) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            cont = True
    else:
        cur.execute("SELECT EXISTS(SELECT 1 FROM playertictactoestats WHERE user_id = %s)", [player_id])
        player_exist = cur.fetchall()
        if not player_exist[0][0]:
            new_player = (
                "INSERT INTO playertictactoestats (user_id, username, wins, losses, win_percent) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            cont = True

    if cont:
        data = (player_id, name, 0, 0, 0)

        cur.execute(new_player, data)

        con.commit()

    cur.close()
    con.close()


def editPlayerScore(player_id, won, mode):
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()
    if mode == 'connect4':
        cur.execute("SELECT wins, losses, win_percent FROM playerconnect4stats WHERE user_id = {0}".format(player_id))
    if mode == 'tictactoe':
        cur.execute("SELECT wins, losses, win_percent FROM playertictactoestats WHERE user_id = {0}".format(player_id))
    user = cur.fetchall()
    wins = user[0][0]
    losses = user[0][1]
    win_percent = user[0][2]
    if won:
        wins += 1
    else:
        losses += 1
    win_percent = round(wins/(wins+losses)*100, 2)

    if mode == 'connect4':
        cur.execute("UPDATE playerconnect4stats SET wins = {0}, losses = {1}, win_percent = {2} WHERE user_id = {3}", [wins, losses, win_percent, player_id])
    if mode == 'tictactoe':
        cur.execute("UPDATE playertictactoestats SET wins = {0}, losses = {1}, win_percent = {2} WHERE user_id = {3}".format(wins, losses, win_percent, player_id))

    con.commit()

    cur.close()
    con.close()

def updateConnect4Scores():
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    cur.execute("SELECT user_id, username, wins, losses, win_percent FROM playerConnect4Stats")
    x = cur.fetchall()
    for player in x:
        win_percent = round(player[2]/(player[2]+player[3])*100, 2)
        cur.execute("UPDATE playerconnect4stats SET win_percent = %s WHERE user_id = %s", [win_percent, player[0]])

    con.commit()
    cur.close()
    con.close()


