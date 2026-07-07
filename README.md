# 🏁 KANJO: Scrap Yard Heroes

*A persistent street racing RPG built with Python.*

---

## Overview

**KANJO: Scrap Yard Heroes** is a persistent single-player and multiplayer street racing RPG where every player begins with nothing more than a forgotten project car pulled from a rundown scrapyard.

Build your reputation from the ground up by defeating AI racers, challenging powerful boss drivers, upgrading your garage, collecting legendary cars, and eventually competing against other players as you climb the underground Kanjo scene.

Every race earns money, reputation, and experience—but also puts wear on your car. Managing your garage is just as important as winning races.

---

# Current Features

* 🚗 Random starter car
* 🏚️ Garage system
* 💰 Economy system
* ⚡ Daily energy system
* 🎁 Daily login rewards
* 🏆 Boss races
* 🤖 AI racing
* 🚘 Scrap Yard Dealer
* 🔄 Multiple owned cars
* 🔑 Active car switching
* 🌧️ Daily world events
* 🏅 Reputation rank progression
* 🎖️ Achievement system
* 📊 Career statistics
* 🏁 Multiple leaderboards
* 🖥️ Desktop game interface (Pygame)

---

# Planned Features

* Online PvP racing
* Discord bot integration
* Crew system
* Crew garages
* Used parts marketplace
* Auction house
* Barn finds
* Junkyard searches
* Story mode
* Rival drivers
* Dynamic police encounters
* Drift battles
* Touge races
* Highway races
* Drag racing
* Circuit racing
* Vehicle classes
* Engine swaps
* Visual customization
* Performance tuning
* Seasonal championships
* Limited-time events
* Global leaderboards
* Trading between players
* Daily challenges
* Weekly challenges
* Prestige system
* Mouse-driven interface
* Animated menus
* Sound effects
* Original soundtrack

---

# Gameplay Loop

1. Create your driver.
2. Receive a random scrap yard starter car.
3. Race AI opponents.
4. Earn money and reputation.
5. Upgrade your vehicle.
6. Repair damage and maintain your car.
7. Expand your garage.
8. Purchase additional vehicles.
9. Defeat Boss Racers.
10. Unlock achievements and climb the leaderboards.
11. Become a Kanjo Legend.

---

# World Events

Every real-world day, a new world event is generated that affects every player.

Examples include:

* Heavy Rain
* Police Crackdown
* Street Festival
* Heat Wave
* Dense Fog
* Clear Streets

Each event can modify:

* Race payouts
* Reputation rewards
* Vehicle grip
* Vehicle wear

---

# Car Management

Vehicles have persistent condition values including:

* Body Condition
* Tire Wear
* Oil Condition
* Engine Wear
* Upgrade Level
* Reliability

Ignoring maintenance will make races progressively more difficult.

---

# Progression

Players progress through reputation ranks:

* Scrap Rookie
* Oil Burner
* Backroad Menace
* Kanjo Runner
* Expressway Regular
* Midnight Threat
* Street Veteran
* Scrap Yard Hero
* Expressway King
* Kanjo Legend

---

# Achievements

Earn permanent achievements for milestones such as:

* Creating your first driver
* Winning your first race
* Defeating your first Boss
* Reaching reputation milestones
* Expanding your garage
* Building a car collection

---

# Requirements

## Operating System

* Windows 10 or newer
* Linux (should work)
* macOS (should work)

---

## Python

Python **3.12** or **3.13** is recommended.

Python 3.14 may have compatibility issues with some libraries until they are updated.

---

## Required Packages

Install the required package:

```bash
python -m pip install pygame-ce
```

If you add more libraries later, you can install everything with:

```bash
python -m pip install -r requirements.txt
```

---

# Project Structure

```text
KANJO-Scrap-Yard-Heroes/
│
├── assets/
│   └── background.png
│
├── data/
│
├── systems/
│
├── ui/
│
├── database.py
├── config.py
├── main.py
└── README.md
```

---

# Running the Game

Clone the repository:

```bash
git clone <repository-url>
```

Open the project folder:

```bash
cd KANJO-Scrap-Yard-Heroes
```

Install the dependencies:

```bash
python -m pip install pygame-ce
```

Launch the game:

```bash
python main.py
```

---

# Contributing

Suggestions, bug reports, balance feedback, and feature ideas are always welcome. As the project grows, contributions from the community will help expand the world of **KANJO: Scrap Yard Heroes**.

---

# License

This project is currently in active development. A formal open-source or custom license will be added before the first public release.

---

## Created By

**PizzaGuy024**

*"Every legend starts as scrap."*
