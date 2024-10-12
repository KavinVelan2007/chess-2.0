from data import *
from utils import *
from numpy import uint64 as uint, zeros, array, uint32


class Board:

	def __init__(self, bitboards = BITBOARDS.copy(), board_data = data):
		self.bitboards = bitboards
		self.board_data = board_data


	def return_moves(self):

		bitboards = self.bitboards
		board_data = self.board_data

		WHITE_PAWNS = bitboards[0]
		WHITE_KNIGHTS = bitboards[1]
		WHITE_BISHOPS = bitboards[2]
		WHITE_ROOKS = bitboards[3]
		WHITE_QUEEN = bitboards[4]
		WHITE_KING = bitboards[5]

		BLACK_PAWNS = bitboards[6]
		BLACK_KNIGHTS = bitboards[7]
		BLACK_BISHOPS = bitboards[8]
		BLACK_ROOKS = bitboards[9]
		BLACK_QUEEN = bitboards[10]
		BLACK_KING = bitboards[11]

		WHITE_PIECES = (
			WHITE_BISHOPS
			| WHITE_KING
			| WHITE_KNIGHTS
			| WHITE_PAWNS
			| WHITE_QUEEN
			| WHITE_ROOKS
		)

		BLACK_PIECES = (
			BLACK_BISHOPS
			| BLACK_KING
			| BLACK_KNIGHTS
			| BLACK_PAWNS
			| BLACK_QUEEN
			| BLACK_ROOKS
		)

		ALL_PIECES = BLACK_PIECES | WHITE_PIECES


		moves = zeros(218, dtype = uint32)      
		count = 0

		def add_move(source, target, piece, promoted, promoted_piece, enpassant, castling):
			nonlocal moves, count

			moves[count] = uint32(source) | uint32(target << 6) | uint32(piece << 12) | uint32(promoted << 16) | uint32(promoted_piece << 17) | uint32(enpassant << 19) | uint32(castling << 20) 
			count += 1


		if board_data & uint32(1) == 0:


			while WHITE_PAWNS:

				curr_square = least_significant_bit_count(WHITE_PAWNS)
				WHITE_PAWNS ^= uint(1 << curr_square)
				attacks = WHITE_PAWN_ATTACKS[curr_square] & BLACK_PIECES

				if 8 <= curr_square <= 15:

					while attacks:
						to_square = least_significant_bit_count(attacks)
						attacks &= (attacks - uint(1))
						add_move(curr_square, to_square, 0, 1, 0, 0, 0)
						add_move(curr_square, to_square, 0, 1, 1, 0, 0)
						add_move(curr_square, to_square, 0, 1, 2, 0, 0)
						add_move(curr_square, to_square, 0, 1, 3, 0, 0)

					if uint(1 << (curr_square - 8)) & (~ALL_PIECES):
						add_move(curr_square, curr_square - 8, 0, 1, 0, 0, 0)
						add_move(curr_square, curr_square - 8, 0, 1, 1, 0, 0)
						add_move(curr_square, curr_square - 8, 0, 1, 2, 0, 0)
						add_move(curr_square, curr_square - 8, 0, 1, 3, 0, 0)

					
				else:

					while attacks:
						to_square = least_significant_bit_count(attacks)
						attacks ^= uint(1 << to_square)
						add_move(curr_square, to_square, 0, 0, 0, 0, 0)

					if uint(1 << (curr_square - 8)) & (~ALL_PIECES):

						if 48 <= curr_square <= 55 and uint(1 << (curr_square - 16)) & (~ALL_PIECES):
							add_move(curr_square, curr_square - 8, 0, 0, 0, 0, 0)
							add_move(curr_square, curr_square - 16, 0, 0, 0, 0, 0)

						else:
							add_move(curr_square, curr_square - 8, 0, 0, 0, 0, 0)

					if (board_data & uint32(1 << 5)) and (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == (curr_square - 9) or (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == curr_square - 7)):
						add_move(curr_square, ((board_data >> uint32(6) & uint32((1 << 6) - 1))), 0, 0, 0, 1, 0)


			while WHITE_KNIGHTS:
				curr_square = least_significant_bit_count(WHITE_KNIGHTS)
				WHITE_KNIGHTS ^= uint(1 << curr_square)
				
				moves_possible = KNIGHT_ATTACKS[curr_square] & (~WHITE_PIECES)

				while moves_possible:
					to_square = least_significant_bit_count(moves_possible)
					moves_possible ^= uint(1 << to_square)
					add_move(curr_square, to_square, 1, 0, 0, 0, 0)


			while WHITE_BISHOPS:
				curr_square = least_significant_bit_count(WHITE_BISHOPS)
				WHITE_BISHOPS ^= uint(1 << curr_square)
				attacks = BISHOP_ATTACKS[curr_square][
					(
						(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
						>> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
					)
				] & (~WHITE_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 2, 0, 0, 0, 0)


			while WHITE_ROOKS:
				curr_square = least_significant_bit_count(WHITE_ROOKS)
				WHITE_ROOKS ^= uint(1 << curr_square)
				attacks = ROOK_ATTACKS[curr_square][
					(
						(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
						>> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
					)
				] & (~WHITE_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 3, 0, 0, 0, 0)


			while WHITE_QUEEN:
				curr_square = least_significant_bit_count(WHITE_QUEEN)
				WHITE_QUEEN^= uint(1 << curr_square)
				attacks = BISHOP_ATTACKS[curr_square][
					(
						(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
						>> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
					)
				] & (~WHITE_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 4, 0, 0, 0, 0)

				attacks = ROOK_ATTACKS[curr_square][
					(
						(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
						>> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
					)
				] & (~WHITE_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 4, 0, 0, 0, 0)

			while WHITE_KING:
				curr_square = least_significant_bit_count(WHITE_KING)
				WHITE_KING ^= uint(1 << curr_square)
				attacks = KING_ATTACKS[curr_square] & (~WHITE_PIECES)
				
				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 5, 0, 0, 0, 0)

				if board_data & uint32(2) and not (ALL_PIECES & uint((1 << 62) + (1 << 61))) and not self.is_square_atacked(1, 61, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not self.is_square_atacked(1, 60, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
					add_move(curr_square, 62, 5, 0, 0, 0, 1)

				if board_data & uint32(4) and not (ALL_PIECES & uint((1 << 59) + (1 << 58) + (1 << 57))) and not self.is_square_atacked(1, 59, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not self.is_square_atacked(1, 60, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
					add_move(curr_square, 58, 5, 0, 0, 0, 1)



		else:


			while BLACK_PAWNS:
				curr_square = least_significant_bit_count(BLACK_PAWNS)
				BLACK_PAWNS ^= uint(1 << curr_square)
				attacks = BLACK_PAWN_ATTACKS[curr_square] & WHITE_PIECES

				if 56 <= curr_square <= 63:

					while attacks:
						to_square = least_significant_bit_count(attacks)
						attacks ^= uint(1 << to_square)
						add_move(curr_square, to_square, 6, 1, 0, 0, 0)
						add_move(curr_square, to_square, 6, 1, 1, 0, 0)
						add_move(curr_square, to_square, 6, 1, 2, 0, 0)
						add_move(curr_square, to_square, 6, 1, 3, 0, 0)

					if uint(1 << (curr_square + 8)) & (~ALL_PIECES):
						add_move(curr_square, curr_square + 8, 6, 1, 0, 0, 0)
						add_move(curr_square, curr_square + 8, 6, 1, 1, 0, 0)
						add_move(curr_square, curr_square + 8, 6, 1, 2, 0, 0)
						add_move(curr_square, curr_square + 8, 6, 1, 3, 0, 0)

				else:

					while attacks:
						to_square = least_significant_bit_count(attacks)
						attacks ^= uint(1 << to_square)
						add_move(curr_square, to_square, 6, 0, 0, 0, 0)

					if uint(1 << (curr_square + 8)) & (~ALL_PIECES):

						if 8 <= curr_square <= 15 and uint(1 << (curr_square + 16)) & (~ALL_PIECES):
							add_move(curr_square, curr_square + 8, 6, 0, 0, 0, 0)
							add_move(curr_square, curr_square + 16, 6, 0, 0, 0, 0)

						else:
							add_move(curr_square, curr_square + 8, 6, 0, 0, 0, 0)

					if (board_data & uint32(1 << 5)) and (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == (curr_square + 9) or (((board_data >> uint32(6)) & uint((1 << 6) - 1)) == curr_square + 7)):
						add_move(curr_square, ((board_data >> uint32(6) & uint32((1 << 6) - 1))), 6, 0, 0, 1, 0)


			while BLACK_KNIGHTS:
				curr_square = least_significant_bit_count(BLACK_KNIGHTS)
				BLACK_KNIGHTS ^= uint(1 << curr_square)
				
				moves_possible = KNIGHT_ATTACKS[curr_square] & (~BLACK_PIECES)

				while moves_possible:
					to_square = least_significant_bit_count(moves_possible)
					moves_possible ^= uint(1 << to_square)
					add_move(curr_square, to_square, 7, 0, 0, 0, 0)


			while BLACK_BISHOPS:
				curr_square = least_significant_bit_count(BLACK_BISHOPS)
				BLACK_BISHOPS ^= uint(1 << curr_square)
				attacks = BISHOP_ATTACKS[curr_square][
					(
						(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
						>> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
					)
				] & (~BLACK_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 8, 0, 0, 0, 0)


			while BLACK_ROOKS:
				curr_square = least_significant_bit_count(BLACK_ROOKS)
				BLACK_ROOKS ^= uint(1 << curr_square)
				attacks = ROOK_ATTACKS[curr_square][
					(
						(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
						>> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
					)
				] & (~BLACK_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 9, 0, 0, 0, 0)


			while BLACK_QUEEN:
				curr_square = least_significant_bit_count(BLACK_QUEEN)
				BLACK_QUEEN^= uint(1 << curr_square)
				attacks = BISHOP_ATTACKS[curr_square][
					(
						(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
						>> uint(64 - BISHOP_OCCUPANCY_BITS[curr_square]
					)
				] & (~BLACK_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 10, 0, 0, 0, 0)

				attacks = ROOK_ATTACKS[curr_square][
					(
						(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
						>> uint(64 - ROOK_OCCUPANCY_BITS[curr_square]
					)
				] & (~BLACK_PIECES)

				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 10, 0, 0, 0, 0)

			while BLACK_KING:
				curr_square = least_significant_bit_count(BLACK_KING)
				BLACK_KING ^= uint(1 << curr_square)
				attacks = KING_ATTACKS[curr_square] & (~BLACK_PIECES)
				
				while attacks:
					to_square = least_significant_bit_count(attacks)
					attacks ^= uint(1 << to_square)
					add_move(curr_square, to_square, 11, 0, 0, 0, 0)

				if board_data & uint32(8) and not (ALL_PIECES & uint((1 << 5) + (1 << 6))) and not self.is_square_atacked(0, 3, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not self.is_square_atacked(0, 4, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
					add_move(curr_square, 6, 11, 0, 0, 0, 1)

				if board_data & uint32(16) and not (ALL_PIECES & uint((1 << 1) + (1 << 2) + (1 << 3))) and not self.is_square_atacked(0, 4, bitboards , board_data, BLACK_PIECES, WHITE_PIECES) and not self.is_square_atacked(0, 5, bitboards , board_data, BLACK_PIECES, WHITE_PIECES):
					add_move(curr_square, 2, 11, 0, 0, 0, 1)

		return moves[:count]


	def copy_position(self):
		return (self.bitboards.copy(), self.board_data)


	def is_square_atacked(self, side, square, bitboards, board_data, black_pieces, white_pieces):

		if side  == 0:
			if bitboards[0] & BLACK_PAWN_ATTACKS[square]:
				return True
			elif bitboards[1] & KNIGHT_ATTACKS[square]:
				return True
			elif (bitboards[2] | bitboards[4]) & BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> uint(64 - BISHOP_OCCUPANCY_BITS[square]))] & (~white_pieces):
				return True
			elif (bitboards[3] | bitboards[4]) & ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * ROOK_MAGIC_NUMBERS[square]) >> uint(64 - ROOK_OCCUPANCY_BITS[square]))] & (~white_pieces):
				return True
			elif bitboards[5] & KING_ATTACKS[square]:
				return True
		else:
			if bitboards[6] & WHITE_PAWN_ATTACKS[square]:
				return True
			elif bitboards[7] & KNIGHT_ATTACKS[square]:
				return True
			elif (bitboards[8] | bitboards[10]) & BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> uint(64 - BISHOP_OCCUPANCY_BITS[square]))] & (~black_pieces):
				return True
			elif (bitboards[9] | bitboards[10]) & ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * ROOK_MAGIC_NUMBERS[square]) >> uint(64 - ROOK_OCCUPANCY_BITS[square]))] & (~black_pieces):
				return True
			elif bitboards[11] & KING_ATTACKS[square]:
				return True

		return False


	def make_move(self, move):
		bitboards = self.bitboards
		data = self.board_data

		piece = (move >> uint32(12)) & uint32(15)
		source = move & uint32(63)
		target = (move >> uint32(6)) & uint32(63)
		'''
		if ((data << uint32(12)) & uint32(63)) == 100:
			return False
		'''
		if 0 <= piece <= 5:
			
			if (move >> uint32(16)) & uint32(1):
				bitboards[0] ^= uint(1 << source)
				bitboards[((move >> uint32(17)) & uint32(3)) + 1] |= uint(1 << target)
				data &= uint32(4095)

			elif (move << uint32(19)) & uint32(1):
				bitboards[0] ^= uint((1 << source) + (1 << target))
				bitboards[6] ^= uint(1 << (target + 8))
				data &= uint32(4095)

			elif (move << uint32(19)) & uint32(1):
				bitboards[5] ^= uint((1 << source) + (1 << target))
				bitboards[3] ^= uint(1 << ((source + target) // 2))

				if target == 62:
					bitboards[3] ^= uint(1 << 63)
				
				else:
					bitboards[3] ^= uint(1 << 56)

				data += uint32(4096)

			else:
				bitboards[piece] ^= uint((1 << source) + (1 << target))

				mask = uint(0)
				for i in range(6):
					mask |= bitboards[6 + i]
					bitboards[i + 6] &= ~uint(1 << target)

				if mask & uint(1 << target):
					data &= uint32(4095)
				else:
					data += uint32(4096)

			data |= uint32(1)

			if piece == 0 and source - target == 16:
				data &= ~uint32(((1 << 6) - 1) << 6)
				data |= uint32((target + 8) << 6)

			if piece == 5:
				data &= ~uint32(6)

			if data & uint32(2) and piece == 3 and source == 63:
				data &= ~uint32(2)

			elif data & uint32(4) and piece == 3 and source == 56:
				data &= ~uint32(4)

			if self.is_square_atacked(1, least_significant_bit_count(bitboards[5]), bitboards, data, bitboards[6] | bitboards[7] | bitboards[8] | bitboards[9] | bitboards[10] | bitboards[11], bitboards[0] | bitboards[1] | bitboards[2] | bitboards[3] | bitboards[4] | bitboards[5]):
				return False

		else:
			if (move >> uint32(16)) & uint32(1):
				bitboards[6] ^= uint(1 << source)
				bitboards[((move >> uint32(17)) & uint32(3)) + 7] |= uint(1 << target)
				data &= uint32(4095)

			elif (move << uint32(19)) & uint32(1):
				bitboards[6] ^= uint((1 << source) + (1 << target))
				bitboards[0] ^= uint(1 << (target + 8))
				data &= uint32(4095)

			elif (move << uint32(19)) & uint32(1):
				bitboards[11] ^= uint((1 << source) + (1 << target))
				bitboards[9] ^= uint(1 << ((source + target) // 2))

				if target == 2:
					bitboards[9] ^= uint(1 << 3)
				
				else:
					bitboards[9] ^= uint(1 << 5)

			else:
				bitboards[piece] ^= uint((1 << source) + (1 << target))

				mask = uint(0)
				for i in range(6):
					mask |= bitboards[i]
					bitboards[i] &= ~uint(1 << target)

				if mask & uint(1 << target):
					data &= uint32(4095)
				else:
					data += uint32(4096)

			data ^= uint32(1)

			if piece == 6 and target - source == 16:
				data &= ~uint32(((1 << 6) - 1) << 6)
				data |= uint32((target - 8) << 6)

			if piece == 11:
				data &= ~uint32(24)

			if data & uint32(8) and piece == 9 and source == 7:
				data &= ~uint32(8)

			elif data & uint32(16) and piece == 9 and source == 0:
				data &= ~uint32(16)

			if self.is_square_atacked(0, least_significant_bit_count(bitboards[11]), bitboards, data, bitboards[6] | bitboards[7] | bitboards[8] | bitboards[9] | bitboards[10] | bitboards[11], bitboards[0] | bitboards[1] | bitboards[2] | bitboards[3] | bitboards[4] | bitboards[5]):
				return False

		self.bitboards = bitboards
		self.board_data = data

		return True


	def print_moves(self, moves):
		for move in moves:
			print(f'From: {square_string[move & uint32((1 << 6) - 1)]}')
			print(f'To: {square_string[(move >> uint32(6)) & uint32((1 << 6) - 1)]}')
			print(f'Piece: {piece_string[(move >> uint32(12)) & uint32((1 << 4) - 1)]}')
			print(f'Promotion: {"No" if not ((move >> uint32(16)) & uint32(1)) else piece_string[(move >> uint32(17)) & (uint32((1 << 4) - 1)) + 1 + (((move >> uint32(12)) & uint32((1 << 4) - 1)) // uint32(6) * 6)]}')
			print(f'EnPassant: {"Yes" if ((move >> uint32(19)) & uint32(1)) else "No"}')
			print(f'Castling: {"Yes" if ((move >> uint32(20)) & uint32(1)) else "No"}')
			print()