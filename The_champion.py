import os
import random
import time
from typing import NoReturn


def cin(
    text: str,
    kimsg: str = "\n[Error] KeyboardInterrupt detected. The program will now exit.",
    stop: bool = True,
    rich: bool = False
) -> str | None | NoReturn:
    """Custom input() with KeyboardInterrupt handling.

    Args:
        text (str): Prompt message.
        kimsg (str, optional): Message on KeyboardInterrupt. Defaults to "".
        stop (bool, optional): Whether to exit on KeyboardInterrupt. Defaults to True.
        rich (bool, optional): Use rich module for input. Defaults to False.
    """
    try:
        if rich and imi:
            from rich.console import Console
            console = Console()
            return console.input(text)
        else:
            return input(text)
    except KeyboardInterrupt:
        print(kimsg)
        if stop:
            exit(None)
    except Exception as e:
        print(f"[Error] Unexpected error in 'cin': {e}")
        exit(None)

imi = False
try:
    from rich import box
    from rich.columns import Columns
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    imi = True
    cin(
        "[Notice] For the best experience, please maximize your terminal window.\n"
        "If you encounter visual issues, consider temporarily uninstalling 'rich' and report the problem to the maintainer.\n"
        "Press Enter to continue. ",
        rich=True
    )
    console = Console()
    console.rule("[bold purple]The Champion")
except ModuleNotFoundError:
    cin("[Info] Installing the 'rich' module via pip is recommended for enhanced visuals (optional). ")
except ImportError:
    print("[Info] Installing the 'rich' module via pip is recommended for enhanced visuals (optional). (ImportError)")
except Exception as e:
    print(f"[Error] An unexpected error occurred during initialization: {e}")

# ===========
class Data:
    """(json) Data management class

    Args:
        file (str): Path to .json file. If not provided, data is stored in memory only.
    """

    def __init__(self, file: str = None):
        import json
        if file is None:
            self.data = {}
            self.path = ""
        else:
            if not os.path.exists(file):
                with open(file, "w") as f:
                    f.write("{\n\n}")
                    f.flush()
                    os.fsync(f.fileno())
                self.data = {}
            else:
                try:
                    with open(file, "r") as f:
                        self.data = json.load(f)
                except json.decoder.JSONDecodeError:
                    print("[Error] Invalid JSON data. Please delete 'the_champion_data.json' in the project directory and try again.")
                    exit(None)
                except Exception as e:
                    print(f"[Error] Unexpected error in Data class: {e}")
            self.file = open(file, mode="r+", encoding="utf-8")
            self.path = file

    def __repr__(self):
        return f"Data('{self.path}')"

    def __str__(self):
        return f"Data: {self.data}\nData file: {self.path}"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        return iter(list(self.data.keys()))

    def add(self, data: dict) -> None:
        """Add or update keys in the data."""
        for key in data:
            self.data[key] = data[key]

    def delete(self, key: str | list[str]) -> None:
        """Delete a key in data. Supports nested dictionaries."""
        if isinstance(key, str):
            self.data.pop(key, None)
        elif isinstance(key, list) and key:
            current = self.data
            for k in key[:-1]:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return
            if isinstance(current, dict):
                current.pop(key[-1], None)

    def get(self) -> dict:
        """Return the data dictionary."""
        return self.data

    def write(self) -> None:
        """Save the data to the JSON file."""
        if self.path == "":
            return
        import json
        json.dump(self.data, open(self.path, mode="w", encoding="utf-8"), indent=4)
# ===========

def options(options: list, title: str = None, prompt: str = "> ") -> int | NoReturn:
    """Display a list of options and prompt the user to choose.

    Args:
        title (str): Title for the options.
        options (list): List of option strings.
        prompt (str, optional): Input prompt. Defaults to "> ".
    """
    choices = []
    if imi:
        table = Table(title=title, box=box.MINIMAL)
        table.add_column("Choice", justify="center", style="magenta")
        table.add_column("Description", justify="left", style="green")
        for n, option in enumerate(options):
            table.add_row(str(n + 1), option)
            choices.append(str(n + 1))
        console.print(table)
        v = cin(prompt)
    else:
        if title is not None:
            print(f"========== {title} ==========")
        for n, option in enumerate(options):
            print(f"{str(n + 1)}. {option}")
            choices.append(str(n + 1))
        v = cin(prompt)
    while (not v.isdigit()) or (v not in choices):
        print(f"[Error] Invalid choice. Please select from: {choices}")
        v = cin(prompt)
    return int(v)

# Data structure and file permission
if not os.path.exists("the_champion_data.json"):
    a = cin(
        "Do you allow this program to save a .json file to your computer?\n"
        "1. Yes\n"
        "2. No (data will not be saved after exit)\n"
        "> "
    )
    while a not in ["1", "2"]:
        a = cin("[Error] Invalid choice. Please enter 1 or 2.\n> ")
    if a == "2":
        d = Data()
        cin("[Warning] Data will be lost when the program stops. Press Enter to continue. ")
    elif a == "1":
        d = Data("the_champion_data.json")
else:
    d = Data("the_champion_data.json")
if "matches" not in d.data or not isinstance(d.data["matches"], list):
    d.data["matches"] = []

def menu():
    choice = options(
        title="Main Menu",
        options=["Play a New Match", "View Match History", "Save and Exit"]
    )
    if choice == 1:
        return "classic"
    if choice == 2:
        return "history"
    if choice == 3:
        return "exit"

def classic():
    print("========== New Match ==========")
    match_id = len(d.data["matches"]) + 1
    d.data["matches"].append({
        "id": match_id,
        "name": f"Match {match_id}",
        "teams": {}
    })
    teams = d.data["matches"][match_id - 1]["teams"]

    name1 = cin("Enter the name of the first team:\n> ")
    while not name1:
        name1 = cin("[Error] Team names cannot be empty or identical.\nEnter the name of the first team:\n> ")

    name2 = cin("Enter the name of the second team:\n> ")
    while (not name2) or (name2 == name1):
        name2 = cin("[Error] Team names cannot be empty or identical.\nEnter the name of the second team:\n> ")

    d.data["matches"][match_id - 1]["name"] = f"---- {name1} vs. {name2} ----"

    for t in ["a", "b"]:
        if f"team_{t}" not in teams:
            teams[f"team_{t}"] = {}

        if t == "a":
            print(f"--- Team: {name1} ---")
            teams[f"team_{t}"]["name"] = name1
        elif t == "b":
            print(f"--- Team: {name2} ---")
            teams[f"team_{t}"]["name"] = name2

        teams[f"team_{t}"]["players"] = []

        remaining_points = 100
        for i in ["first", "second", "third", "forth", "fifth"]:
            player_name = cin(f"Enter the {i} player's name: ")
            while not player_name:
                player_name = cin(f"[Error] Player name cannot be empty.\nEnter the {i} player's name: ")

            if i == "fifth":
                player_point = remaining_points
                print(f"[Info] The fifth player's ability points are automatically set to {player_point}.")
            else:
                player_point = cin(
                    f"Enter the {i} player's ability points (0-{remaining_points}): "
                )
                while (not player_point.isdigit()) or (not 0 <= int(player_point) <= remaining_points):
                    player_point = cin(
                        f"[Error] Ability points must be an integer from 0 to {remaining_points}.\n"
                        f"Enter the {i} player's ability points (0-{remaining_points}): "
                    )

            player_point = int(player_point)
            teams[f"team_{t}"]["players"].append({"name": player_name, "point": player_point})
            remaining_points -= player_point

    print(f"---- {name1} vs. {name2} ----")
    team_a = [0, 1, 2, 3, 4]
    team_b = [0, 1, 2, 3, 4]
    score_a = 0
    score_b = 0
    for i in range(5):
        p1 = random.choice(team_a)
        p2 = random.choice(team_b)
        player1 = teams["team_a"]["players"][p1]
        player2 = teams["team_b"]["players"][p2]
        print(f"{player1['name']} ({player1['point']}) vs {player2['name']} ({player2['point']})")
        time.sleep(0.1)
        if player1["point"] > player2["point"]:
            score_a += 1
            print(f"{player1['name']} wins! Current score: {score_a}-{score_b}")
        elif player1["point"] < player2["point"]:
            score_b += 1
            print(f"{player2['name']} wins! Current score: {score_a}-{score_b}")
        elif player1["point"] == player2["point"]:
            print(f"It's a draw. Current score: {score_a}-{score_b}")
        else:
            print("[Error] Unexpected result.")
        print("")
        team_a.remove(p1)
        team_b.remove(p2)
        time.sleep(0.3)

    if "result" not in d.data["matches"][match_id - 1]:
        d.data["matches"][match_id - 1]["result"] = []
    if score_a > score_b:
        d.data["matches"][match_id - 1]["result"].append({"winner": "team_a", "score": f"{score_a}-{score_b}"})
        print(f"\n[Result] Winner: {teams['team_a']['name']}")
    elif score_a < score_b:
        d.data["matches"][match_id - 1]["result"].append({"winner": "team_b", "score": f"{score_a}-{score_b}"})
        print(f"\n[Result] Winner: {teams['team_b']['name']}")
    elif score_a == score_b:
        d.data["matches"][match_id - 1]["result"].append({"winner": "draw", "score": f"{score_a}-{score_b}"})
        print("\n[Result] The match is a draw!")
    else:
        print("[Error] Unexpected result.")

    if cin("Would you like a rematch? (y/n)\n> ").lower() == "y":
        return "rematch", match_id
    cin("Press Enter to return to the main menu. ")
    return "menu"

def rematch(match_id: int = len(d.data["matches"])):
    print("---- " + d.data["matches"][match_id - 1]["name"] + " ----")
    teams = d.data["matches"][match_id - 1]["teams"]
    team_a = [0, 1, 2, 3, 4]
    team_b = [0, 1, 2, 3, 4]
    score_a = 0
    score_b = 0
    for i in range(5):
        p1 = random.choice(team_a)
        p2 = random.choice(team_b)
        player1 = teams["team_a"]["players"][p1]
        player2 = teams["team_b"]["players"][p2]
        print(f"{player1['name']} ({player1['point']}) vs {player2['name']} ({player2['point']})")
        time.sleep(0.1)
        if player1["point"] > player2["point"]:
            score_a += 1
            print(f"{player1['name']} wins! Current score: {score_a}-{score_b}")
        elif player1["point"] < player2["point"]:
            score_b += 1
            print(f"{player2['name']} wins! Current score: {score_a}-{score_b}")
        elif player1["point"] == player2["point"]:
            print(f"It's a draw. Current score: {score_a}-{score_b}")
        else:
            print("[Error] Unexpected result.")
        print("")
        team_a.remove(p1)
        team_b.remove(p2)
        time.sleep(0.3)

    if "result" not in d.data["matches"][match_id - 1]:
        d.data["matches"][match_id - 1]["result"] = []
    if score_a > score_b:
        d.data["matches"][match_id - 1]["result"].append({"winner": "team_a", "score": f"{score_a}-{score_b}"})
        print(f"\n[Result] Winner: {teams['team_a']['name']}")
    elif score_a < score_b:
        d.data["matches"][match_id - 1]["result"].append({"winner": "team_b", "score": f"{score_a}-{score_b}"})
        print(f"\n[Result] Winner: {teams['team_b']['name']}")
    elif score_a == score_b:
        d.data["matches"][match_id - 1]["result"].append({"winner": "draw", "score": f"{score_a}-{score_b}"})
        print("\n[Result] The match is a draw!")
    else:
        print("[Error] Unexpected result.")

    if cin("Would you like another rematch? (y/n)\n> ").lower() == "y":
        return "rematch", match_id
    cin("Press Enter to return to the main menu. ")
    return "menu"

def history():
    print("========== Match History ==========")
    if imi:
        panels = []
        for match in d.data["matches"]:
            team_a, team_b, draw = 0, 0, 0
            for result in match["result"]:
                winner = result["winner"]
                if winner == "team_a":
                    team_a += 1
                elif winner == "team_b":
                    team_b += 1
                elif winner == "draw":
                    draw += 1
            panels.append(Panel(
                f"Match ID: {match['id']}\n"
                f"[blue]{match['name']}[/blue]\n"
                f"[yellow]Overall score: {team_a}-{team_b} (draws: {draw})[/yellow]\n",
                expand=False
            ))
        console.print(Columns(panels))
    else:
        for match in d.data["matches"]:
            team_a, team_b, draw = 0, 0, 0
            for result in match["result"]:
                winner = result["winner"]
                if winner == "team_a":
                    team_a += 1
                elif winner == "team_b":
                    team_b += 1
                elif winner == "draw":
                    draw += 1
            print("--------")
            print(
                f"Match ID: {match['id']}\n"
                f"{match['teams']['team_a']['name']} vs. {match['teams']['team_b']['name']}\n"
                f"Overall score: {team_a}-{team_b} (draws: {draw})"
            )
            print("--------")
    if not d.data["matches"]:
        cin("No match data found.\n\nPress Enter to return to the main menu. ")
        return "menu"
    choice = cin(
        "\nEnter the ID of a match to view details.\n"
        "To rematch, enter the ID followed by 'r' (e.g., 2r).\n"
        "Enter 'm' to return to the main menu.\n"
        "> "
    )
    while (
        choice != "m"
        and not (choice.replace("r", "", 1).isdigit())
        or (choice.replace("r", "", 1).isdigit() and not 1 <= int(choice.replace("r", "", 1)) <= len(d.data["matches"]))
    ):
        choice = cin("[Error] Invalid input. Please try again.\n> ")
    if choice == "m":
        return "menu"
    if "r" in choice:
        return "rematch", int(choice.replace('r', ""))
    else:
        match = d.data["matches"][int(choice) - 1]
        team_a, team_b, draw = 0, 0, 0
        for result in match["result"]:
            winner = result["winner"]
            if winner == "team_a":
                team_a += 1
            elif winner == "team_b":
                team_b += 1
            elif winner == "draw":
                draw += 1
        players_a = ""
        for player in match["teams"]["team_a"]["players"]:
            players_a += f"{player['name']} | {player['point']}\n"

        players_b = ""
        for player in match["teams"]["team_b"]["players"]:
            players_b += f"{player['name']} | {player['point']}\n"

        results = ""
        for result in match["result"]:
            results += f"{result['winner']} | {result['score']}\n"

        if imi:
            console.print(Panel(
                f"Match ID: {match['id']}\n"
                f"[blue]{match['name']}[/blue]\n"
                f"[yellow]Overall score: {team_a}-{team_b} (draws: {draw})[/yellow]\n"
                f"[bold white]-- Team {match['teams']['team_a']['name']} --[/bold white]\n"
                "Player Name | Ability Points\n"
                f"{players_a}"
                f"[bold white]-- Team {match['teams']['team_b']['name']} --[/bold white]\n"
                "Player Name | Ability Points\n"
                f"{players_b}"
                "[bold green]-- Results --[/bold green]\n"
                f"{results}",
                expand=False
            ))
        else:
            print("------")
            print(
                f"Match ID: {match['id']}\n"
                f"{match['name']}\n"
                f"Overall score: {team_a}-{team_b} (draws: {draw})\n"
                f"-- Team {match['teams']['team_a']['name']} --\n"
                "Player Name | Ability Points\n"
                f"{players_a}"
                f"-- Team {match['teams']['team_b']['name']} --\n"
                "Player Name | Ability Points\n"
                f"{players_b}"
                "----- Results -----\n"
                f"{results}"
            )
            print("------")
    cin("\nPress Enter to return to the main menu. ")
    return "menu"

func_map = {
    "menu": menu,
    "classic": classic,
    "rematch": rematch,
    "history": history,
}
run = "menu"
arg = None
while run != "exit":
    if run is None:
        print("\n\n[Error] An unexpected error occurred. Returning to the main menu.")
        run = "menu"

    func = func_map.get(run)
    if func is None:
        print(f"\n\n[Error] Unknown command: {run}. Returning to the main menu.")
        run = "menu"
        continue

    try:
        if arg is None:
            result = func()
        else:
            result = func(arg)
    except Exception as e:
        print(f"[Error] Unexpected error while running the program: {e}\nThe program will now exit.")
        exit(None)

    if isinstance(result, tuple):
        run, arg = result
    else:
        run = result
        arg = None

d.write()
