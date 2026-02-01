# ♟️ Chess 2.0 — Bitboard Chess Game with AI

Chess 2.0 is a desktop chess game built using Python, featuring a fast **bitboard-based chess engine**, an **AI opponent powered by the Minimax algorithm**, and a modern graphical user interface.  
The game supports **Human vs Human** and **Human vs Bot** play, with full chess rules and smooth gameplay.

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

---

## 📦 Installation

### 1️⃣ Download or Clone the Project
```bash
git clone <repository-url>
cd <repository-name>
```

### 2️⃣ Install Required Python Libraries
```bash
pip install pygame customtkinter numpy pillow cython
```
