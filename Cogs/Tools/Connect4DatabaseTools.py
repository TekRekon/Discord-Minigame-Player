import psycopg2


def fetchStats():
    con = psycopg2.connect("postgres://tmneuvqnzogsxo:d15b738ee44cc1429e2cf014bf3c1df8448fea2b0155a4157e8e2a37dbc0d495@ec2-54-146-142-58.compute-1.amazonaws.com:5432/d3ad8vk1so3cfu")
    cur = con.cursor()

    cur.execute("SELECT user_id, username, wins, losses FROM playerConnect4Stats")
    rows = cur.fetchall()

    cur.close()
    con.close()

    return rows


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


