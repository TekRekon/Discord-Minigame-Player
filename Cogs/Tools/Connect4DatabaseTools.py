import psycopg2


def fetchRankedStats():
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    cur.execute("SELECT user_id, username, wins, losses FROM playerConnect4Stats")
    rows = cur.fetchall()

    cur.close()
    con.close()

    player_scores = []
    for r in rows:
        games_sum = r[2] + r[3]
        if games_sum < 10:
            continue
        win_percent = round(r[2]/games_sum*100, 2)

        # print(f"ID: {r[0]}, NAME: {r[1]}, WINS: {r[2]}, LOSS: {r[3]}")

        for i, tuple in enumerate(player_scores):
            if win_percent >= tuple[1]:
                player_scores.insert(i, (r[1], win_percent, r[0]))
                break
        else:
            player_scores.append((r[1], win_percent, r[0]))

    return player_scores

def getPlayerStat(player_id, data):
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    cur.execute("SELECT user_id, username, wins, losses FROM playerConnect4Stats WHERE user_id = %s", [player_id])
    user = cur.fetchall()

    cur.close()
    con.close()

    if data == "wins":
        return user[0][2]
    elif data == "losses":
        return user[0][3]
    elif data == "name":
        return user[0][1]
    elif data == "win_rate":
        return user[0][2]/(user[0][2]+user[0][3])


def addPlayer(player_id, name):
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    cur.execute("SELECT user_id FROM playerConnect4Stats")
    rows = cur.fetchall()

    if player_id not in [i[0] for i in rows]:
        new_player = (
            "INSERT INTO playerConnect4Stats (user_id, username, wins, losses) "
            "VALUES (%s, %s, %s, %s)"
        )

        data = (player_id, name, 0, 0)

        cur.execute(new_player, data)

        con.commit()

    cur.close()
    con.close()


def editPlayerScore(player_id, won):
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()
    if won:
        cur.execute("UPDATE playerConnect4Stats SET wins = wins + 1 WHERE user_id = %s", [player_id])
    else:
        cur.execute("UPDATE playerConnect4Stats SET losses = losses + 1 WHERE user_id = %s", [player_id])

    con.commit()

    cur.close()
    con.close()


