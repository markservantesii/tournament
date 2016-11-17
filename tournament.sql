-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create a new database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Connect to the database
\c tournament;

CREATE TABLE players (
    id serial primary key,
    name text
);

CREATE TABLE matches (
    id serial primary key,
    winner integer,
    loser integer
);

CREATE VIEW wins as
    SELECT players.id, count(matches.winner) as matcheswon
    FROM players LEFT JOIN matches
    ON players.id = matches.winner
    GROUP BY players.id;

CREATE VIEW totalmatches as
    SELECT players.id, count(matches.*) as num
    FROM players LEFT JOIN matches
    ON players.id = matches.winner
    OR players.id = matches.loser
    GROUP BY players.id;

-- standings
CREATE VIEW standings as
    SELECT players.*,
            wins.matcheswon as totalwins,
            totalmatches.num as allmatches
    FROM players
    left join wins on players.id = wins.id
    left join totalmatches on players.id = totalmatches.id
    ORDER BY totalwins DESC, allmatches DESC;

-- Views dealing with byes
/*
byes - finds all players that have received a bye
bye_queue - A view that mimics a priority queue
            with priority based on weakest player.
            It only includes players that haven't had
            a bye
next_bye - A view that mimics pop() method for the bye_queue.
            Gets the next player to receive a bye.
*/
CREATE VIEW byes as
    SELECT winner as bye FROM matches
    WHERE loser is NULL;

CREATE VIEW bye_queue as
    SELECT * FROM standings
    WHERE standings.id NOT in
    (SELECT * FROM byes)
    ORDER BY totalwins, allmatches;

CREATE VIEW next_bye as
    SELECT * FROM bye_queue
    LIMIT 1;

