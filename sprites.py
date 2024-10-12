from PIL import Image
import customtkinter as ctk


PieceImages = []

pieces = ['White-Pawn', 'White-Knight', 'White-Bishop', 'White-Rook', 'White-Queen', 'White-King', 'Black-Pawn', 'Black-Knight', 'Black-Bishop', 'Black-Rook', 'Black-Queen', 'Black-King']

for i in pieces:
	PieceImages += [
		ctk.CTkImage(
			light_image = Image.open(f'resources/Pieces/{i}.png').convert('RGBA'),
			dark_image = Image.open(f'resources/Pieces/{i}.png',).convert('RGBA'),
			size = (75, 75)
		)
		]
	print(Image.open(f'resources/Pieces/{i}.png').mode)

BoardImage = ctk.CTkImage(
	light_image = Image.open('resources/rect-8x8.png'),
	dark_image = Image.open('resources/rect-8x8.png'),
	size = (620, 620)
)