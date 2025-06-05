# 🥦 Veggies vs Fruits 🍅

**My personal project to emulate _Battle Cats_... but with vegetables and fruits!!! And possibly other weird things...**

A fun and quirky 2D tower defense-style game made with Python and Pygame. Defend your vegetable base from invading fruit enemies by spawning an army of veggie warriors. Progress through levels, unlock characters, and enjoy vibrant gameplay with charming hand-drawn units!

---

## 🎮 Gameplay Overview

- 🧠 **Strategy:** Deploy vegetable units to stop the wave of incoming fruit enemies before they destroy your base.
- 🥕 **Units:** Each vegetable unit has unique attack stats, abilities, and costs.
- 🍇 **Enemies:** Waves of fruit-themed enemies spawn over time and try to defeat your base.
- 🏰 **Bases:** Both teams have bases—destroy the enemy base to win, or defend yours to survive!
- 🎬 **Levels:** Structured level system with increasing difficulty and variety.

---

## 📦 Features

- 🧑‍🌾 Spawn up to 50 veggie units to defend your base
- 🔁 Game states: Play, Pause, Win, Game Over
- 🛡️ Custom base and enemy base logic
- 🍽️ Different unit types and attack behaviors
- 🔀 Multiple levels with spawning logic via `LevelManager`
- 🖱️ Clickable UI for deploying units or pausing/resuming
- 🎨 Pop-up overlays with blurred backgrounds for win/loss screens

---

## 🧰 Tech Stack

- **Python 3**
- **Pygame** (for game rendering, animation, input handling)
- Modular codebase: split into components like `unit_factory`, `level_manager`, `units`

---

## 🚀 Getting Started

### 🔧 Prerequisites

Make sure you have Python 3 and pip installed. Then install Pygame:

```bash
pip install pygame
