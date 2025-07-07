# 🏆 The Champion Game — Instructions

Welcome to **The Champion Game**! This guide will help you set up matches, understand the rules, and get the most out of every feature.

---

## 🚩 **Starting a New Match**

- **Teams:**  
  - *2 teams*, each with *5 players*.  
  - *Teams with the same name are treated as separate and unrelated, even across different matches.*
- **Ability Points:**  
  - Each player receives *ability points*.  
  - **Total per team:** *Exactly 100 points* — no more, no less.
- **Customization:**  
  - **Team names:**  
    - *Cannot be empty or just spaces.*
  - **Player names:**  
    - *Cannot be empty.*
  - **Ability points:**  
    - *Must total 100 per team.*

---

## 🔀 **Pairing & Scoring**

- **Pairing:**  
  - Players are *randomly paired* (one from each team).  
  - *Each player is paired once* — resulting in *5 pairs per match*.
- **Scoring:**  
  - For each pair:
    - The player with *more ability points* wins and earns **1 point** for their team.
    - If both have *equal points*, **no points** are awarded.
- **Match Outcome:**  
  - After all pairs, the team with the *higher score* wins the match.
  - If scores are *tied*, the match is a **draw**.
- **Rematch:**  
  - After any match, you can *choose to play a rematch* with the same teams.
  - The winning team will have their *overall score* increased by 1.

---

## 📜 **Viewing Match History**

- **Where:**  
  - Match history is stored *in memory* and in `the*champion*data.json`.
- **What’s Displayed:**  
  - **Match ID**
  - **Match Name** (e.g., *Team A vs. Team B*)
  - **Overall Score** (total matches won by each team)
- **Detailed View:**  
  - For any match, you can see:
    - Match ID
    - Match Name
    - Overall Score
    - *Players and their ability points for each team*
- **Rematch:**  
  - *Replay any match* using the same teams and players.

---

---
> The following are the program requirements (not just a feature overview):

## 🖥️ **Program Features**

- **Input Validation:**  
  - Ensures all names and ability points follow the rules.
  - *Invalid input? You’ll be prompted to try again.*
- **Match & Pairing:**  
  - Randomizes pairs, ensures each player is paired once, and calculates results.
- **History:**  
  - View all previous matches and their details.
- **Exit:**  
  - Quit the program at any time.

---

## 💾 **Saving & Loading Data**

- All match data is *automatically saved* and can be *loaded* from `the*champion*data.json`.

---

## 📊 **Display & Statistics**

- **Pair Results:**  
  - See the outcome of *every individual pair* as the match is played.
  - Note: Pair results are not stored in match history; only the overall match result is saved.
- **Team Stats:**  
  - View the *overall score* for both teams within each match session (including rematches).
  - *There are no global stats across different matches, even if team names are the same.*
- **Match History:**  
  - *Accurate and detailed* records of every match.

---

## 🛠️ **Code Structure & Standards**

- **Functions:**  
  - Code is organized into *clear, logical functions*.
- **Naming:**  
  - *Descriptive variable and function names* throughout.
- **Style:**  
  - *Follows [PEP8](https://peps.python.org/pep-0008/) standards* for Python code.

---

*Enjoy playing The Champion Game!*
