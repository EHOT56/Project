import time

from classes import AssaultCube
from pprint import pprint
import requests


if __name__ == "__main__":
    ac = AssaultCube()

    while True:
        json = {"map": ac.map, "players": []}
        for player in ac.entity_list:
            json["players"].append({
                "name": player.name,
                "pos": list(player.position),
                "health": player.health,
                "team": player.team
            })

        response = requests.post("http://127.0.0.1:5000/session/EHOT/update", json=json)
        time.sleep(0.05)

    # In Game Position(70.0, 64.0) - левый, верхний угол
    # In Game Position (70.0, 165.0) - левый, нижний угол
    # In Game Position (195.0, 165.0) - правый, нижний угол
    # In Game Position (195.0, 64.0) - правый, верхний угол
