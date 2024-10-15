import customtkinter as ctk
from PIL import ImageTk
from sprites import *
from fen import *
import tkinter as tk
import pywinstyles


def count_bits(bit_board):
	c = 0
	while bit_board:
		bit_board &= bit_board - 1
		c += 1
	return c


def least_significant_bit_count(bit_board):
	return count_bits((bit_board & -bit_board) - 1)


class GameFrame(ctk.CTkFrame):


    def __init__(self, master):

        super().__init__(master)
        self.master = master
        self.configure(height = 620, width = 620)
        self.grid_propagate(False)
        self.board_canvas = ctk.CTkCanvas(self, width = 620, height = 620)
        #self.piece_canvas = ctk.CTkCanvas(self, width = 620, height = 620)
        #self.piece_canvas.place(x = 0, y = 0)
        self.board_image_label = ctk.CTkLabel(self.board_canvas, text = '', image = BoardImage, bg_color = 'transparent', fg_color = 'transparent')
        #pywinstyles.set_opacity(self.board_image_label)
        self.board_image_label.place(x = 0, y = 0)
        self.refresh_labels(list(generate_bitboards_from_board(fenString)[0]))
        self.place_image_labels()        
        self.board_canvas.place(x = 0, y = 0)        
    

    def refresh_labels(self, bitboards):

        bitboards = bitboards.copy()
        self.image_labels = [None for i in range(64)]
        
        for i in range(12):

            while bitboards[i]:

                square = least_significant_bit_count(bitboards[i])
                bitboards[i] ^= 1 << square
                self.image_labels[square] = ctk.CTkLabel(self.board_canvas, text = '', image = PieceImages[i], bg_color = 'transparent', fg_color = 'transparent')
                pywinstyles.set_opacity(self.image_labels[square], value = 0.7)
                

    def place_image_labels(self):

        for i in range(63, -1, -1):
            
            if self.image_labels[i] is not None:
                self.image_labels[i].place(x = i % 8 * 76.5 + 7, y = i // 8 * 75 + 10)
