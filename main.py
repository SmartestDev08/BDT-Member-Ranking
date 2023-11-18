starting_rating = 500
maximum_change = 32

def get_leaderboard():
    with open("leaderboard.txt", "r") as f:
        lb = f.read().splitlines()
        f.close()
    
    new_lb = {}
    
    for line in lb:
        
        line = line.replace("﻿", "")

        if "@" in line:
            division_1 = line.split("@")
            division_2 = division_1[1].split(" --> ")
            username = division_2[0]
            division_3 = division_2[1].split(" :")
            points = division_3[0]

            new_lb[username] = int(points)
    
    return new_lb

leaderboard = get_leaderboard()

def update_board():
    players_order = sorted(leaderboard.keys(), key = lambda x: leaderboard[x])[::-1]

    return players_order

def calculate_new_rating(p1, p2, r1, r2):

    def calculate_win_probability(r1, r2):
        return 1 / ( 1 + ( 10**( (r2 - r1) / 500 ) ) )

    prob1 = calculate_win_probability(r1, r2)
    prob2 = calculate_win_probability(r2, r1)

    win_points = ( p1 - p2 ) / 5

    if p1 > p2:
        win_points = ( p1 - p2 ) / 5

        new_r1 = r1 + ( win_points * ( maximum_change * (1 - prob1) ) )
        new_r2 = r2 + ( -win_points * ( maximum_change * (prob2) ) )
    else:
        win_points = ( p2 - p1 ) / 5
        
        new_r1 = r1 + ( -win_points * ( maximum_change * ( prob1 ) ) )
        new_r2 = r2 + ( win_points * ( maximum_change * ( 1 - prob2 ) ) )
    
    return (new_r1, new_r2)

def set_result(score, users):

    if users[0] not in leaderboard:
        leaderboard[users[0]] = starting_rating
    
    if users[1] not in leaderboard:
        leaderboard[users[1]] = starting_rating

    data = calculate_new_rating(score[0], score[1], leaderboard[users[0]], leaderboard[users[1]])

    leaderboard[users[0]] = int(data[0])
    leaderboard[users[1]] = int(data[1])

def write_leaderboard(order):

    def number_to_emoji(n):
        conversion = {
            "0": ":zero:",
            "1": ":one:",
            "2": ":two:",
            "3": ":three:",
            "4": ":four:",
            "5": ":five:",
            "6": ":six:",
            "7": ":seven:",
            "8": ":eight:",
            "9": ":nine:"
        }

        n = str(n)
        result = ""

        for c in n:
            result += conversion[c]
        
        return result

    with open("leaderboard.txt", "w") as f:
        f.write("**MEMBER RANKING**\n\n")
        
        f.write(f"> :first_place: @{order[0]} --> {leaderboard[order[0]]} :trophy:\n")
        f.write(f"> :second_place: @{order[1]} --> {leaderboard[order[1]]} :trophy:\n")

        if len(order) > 2:
            f.write(f"> :third_place: @{order[2]} --> {leaderboard[order[2]]} :trophy:\n")

            for i, n in enumerate(order):
                i = i + 1

                if i > 3:
                    f.write(f"> {number_to_emoji(i)} @{n} --> {leaderboard[n]} :trophy:\n")

        f.write("\n*read pinned message to know how to get here*")

score = input("Score: ")
score = score.split(" - ")
score = (int(score[0]), int(score[1]))

players = input("Players: ")
players = players.split(" - ")
players = (players[0], players[1])

set_result(score, players)

write_leaderboard(update_board())