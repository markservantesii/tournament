#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players;")
    results = c.fetchone()
    return results[0]
    db.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM standings;")
    results = c.fetchall()
    #row[0] = id, row[1] = name, row[2] = wins, row[3]= matches
    standings = [(row[0],
                  row[1],
                  row[2],
                  row[3]) for row in results]
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

      To report a bye, mark the winner with the player id;
      Do not report a loser.
    """
    if not loser:
        loser=None
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO matches (winner,loser) VALUES (%s, %s)", (winner,loser))
    db.commit()
    db.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    bye = None
    db = connect()
    c = db.cursor()
    if countPlayers() % 2 == 1:
        c.execute("SELECT id,name FROM next_bye;")
        bye = c.fetchall()
    c.execute("SELECT id,name FROM standings;")
    results = c.fetchall()
    db.close()

    # row[0] = id
    ids = [row[0] for row in results]
    id1,id2 = ids[::2],ids[1::2]

    #row[1] =  name
    names = [row[1] for row in results]
    name1,name2 = names[::2], names[1::2]

    # If there are odd numbers of players,
    # 'pairings' won't include the last player
    # We append it at the end if we have a bye
    pairings = zip(id1,name1,id2,name2)
    # bye[0] = id, bye[1] = name
    if bye:
        pairings.append((bye[0],bye[1],None,None))

    return pairings







