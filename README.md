# Rush Hour Game 🛻🟥

A Python implementation of the classic **Rush Hour** puzzle game.

## 🎯 Goal

Help the red car (ID: `'X'`) reach the exit on the right edge of the board by moving other vehicles out of its way.

## 📦 Features

- Configurable 6x6 board
- Multiple car objects with direction and length
- Text-based interface
- Move validation
- Puzzle solver (optional advanced feature)

## 🚗 Vehicle Format

Each vehicle is defined by:

```python
{
  "id": "A",           # Unique ID (string)
  "row": 0,            # Starting row (0-indexed)
  "col": 2,            # Starting column (0-indexed)
  "dir": "H",          # 'H' for horizontal, 'V' for vertical
  "length": 2          # 2 or 3
}
