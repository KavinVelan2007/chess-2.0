# ♟️ **Chess 2.0** — Bitboard Chess Game with Optimal Move Generation using Minimax Algorithm

**Chess 2.0** is a desktop chess game built using Python, featuring a fast **bitboard-based chess engine**, an **AI opponent powered by the Minimax algorithm**, and a modern graphical user interface.  
The game supports **Human vs Human** and **Human vs Bot** play, with full chess rules and smooth gameplay.

We built as part of my 12th grade final project, focusing on algorithmic problem solving and game logic implementation.

---

## ✨ Features

- ♞ Complete implementation of chess rules  
  - Legal move generation  
  - Castling, en passant, promotion  
  - Check and checkmate detection  

- ⚡ High-performance chess engine  
  - Bitboard representation  
  - Magic bitboards for sliding pieces  
  - Cython-optimized move generation  

- 🤖 Built-in chess bot  
  - Minimax algorithm with alpha–beta pruning  
  - Searches up to **5 moves ahead**  
  - Play against the computer as Black  

- 🎨 Modern graphical interface  
  - Pygame-based chessboard rendering  
  - CustomTkinter GUI  
  - Multiple board and piece themes  
  - Light / Dark / System appearance modes  

- 💾 User accounts & preferences  
  - Sign In / Sign Up system  
  - Saved board and piece themes  
  - Save game progress using FEN  

- 📜 Move history panel  
  - Clean move notation  
  - Captures, castling, and promotions displayed  

---

## 🖥️ System Requirements

- Python **3.10 or newer**
- Windows or Linux (Windows recommended)
- Microsoft Visual Studio (>2024)

---

## 📦 Installation

### 1️⃣ Clone the Project
```bash
git clone https://github.com/KavinVelan2007/chess-2.0
cd chess-2.0
```

### 2️⃣ Install Required Python Libraries
```bash
pip install -r requirements.txt
```

### 3️⃣ Build the Cython File
```
python setup.py build_ext --inplace
```

### 4️⃣ Move the **root.py** to parent directory
```bash
move root.py ..
```

### 5️⃣ Execute **root.py**
```bash
python root.py
```

---

## __Contributors__
- **M. Kavin Velan** (@KavinVelan2007) 
- **G. Pranav** (@useless-coder-person)
