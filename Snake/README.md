# 🐍 Snake Game in Python (Terminal Version)

This is a simple terminal-based implementation of the classic **Snake** game using Python. It was inspired by [Robert Heaton's blog post](https://robertheaton.com/2018/12/02/programming-project-5-snake/).

## 📜 Description

Guide a snake through a grid to eat apples and grow longer. The game ends if the snake runs into itself. The game runs entirely in the terminal and updates the screen by printing the board state every frame.

This project is a great exercise in:
- Game loops
- Real-time input handling
- Collision detection
- Grid-based logic and rendering
- Topological game space (e.g., torus, Klein bottle, RP²)

## 🎮 Features

- Snake moves in real-time based on arrow or WASD key input
- Apples spawn at random, non-overlapping locations
- The snake grows after eating an apple
- Game over when the snake bites itself
- Three space topologies:
  - **Torus** (wraps around edges)
  - **Klein bottle**
  - **Real projective plane (RP²)**

## 🚀 How to Run

### Requirements

- Python 3.x
- `keyboard` module

### Installation

Install the required module with pip:

```bash
pip install keyboard
