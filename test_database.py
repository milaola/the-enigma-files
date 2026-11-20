
from database import create_player, complete_room, get_leaderboard


player_id = create_player("Test Player")

print("Player ID:", player_id)


complete_room(player_id)
complete_room(player_id)


players = get_leaderboard()

for player in players:
    print(player)
