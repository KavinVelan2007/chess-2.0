from fen import *
import pickle
from libc.string cimport memset, memcpy
cimport cython


# cython decorators
'''
@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
'''
# -----------------

ctypedef (unsigned long long) U64
ctypedef (unsigned int) U32
ctypedef (unsigned char) U8
cdef U64 one = 1

'''
DATA STARTS HERE
'''

temp_BITBOARDS, temp_BOARD_DATA = generate_bitboards_from_board(fenString)


cdef U64[12] BITBOARDS = temp_BITBOARDS
cdef U32 BOARD_DATA = temp_BOARD_DATA


del temp_BITBOARDS, temp_BOARD_DATA


square_string = [
	'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8',
	'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
	'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6',
	'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
	'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
	'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
	'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
	'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']

piece_string = "♙♘♗♖♕♔♟♞♝♜♛♚"


cdef U64[64] WHITE_PAWN_ATTACKS = [
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	2,
	5,
	10,
	20,
	40,
	80,
	160,
	64,
	512,
	1280,
	2560,
	5120,
	10240,
	20480,
	40960,
	16384,
	131072,
	327680,
	655360,
	1310720,
	2621440,
	5242880,
	10485760,
	4194304,
	33554432,
	83886080,
	167772160,
	335544320,
	671088640,
	1342177280,
	2684354560,
	1073741824,
	8589934592,
	21474836480,
	42949672960,
	85899345920,
	171798691840,
	343597383680,
	687194767360,
	274877906944,
	2199023255552,
	5497558138880,
	10995116277760,
	21990232555520,
	43980465111040,
	87960930222080,
	175921860444160,
	70368744177664,
	562949953421312,
	1407374883553280,
	2814749767106560,
	5629499534213120,
	11258999068426240,
	22517998136852480,
	45035996273704960,
	18014398509481984
]

cdef U64[64] BLACK_PAWN_ATTACKS = [
	512,
	1280,
	2560,
	5120,
	10240,
	20480,
	40960,
	16384,
	131072,
	327680,
	655360,
	1310720,
	2621440,
	5242880,
	10485760,
	4194304,
	33554432,
	83886080,
	167772160,
	335544320,
	671088640,
	1342177280,
	2684354560,
	1073741824,
	8589934592,
	21474836480,
	42949672960,
	85899345920,
	171798691840,
	343597383680,
	687194767360,
	274877906944,
	2199023255552,
	5497558138880,
	10995116277760,
	21990232555520,
	43980465111040,
	87960930222080,
	175921860444160,
	70368744177664,
	562949953421312,
	1407374883553280,
	2814749767106560,
	5629499534213120,
	11258999068426240,
	22517998136852480,
	45035996273704960,
	18014398509481984,
	144115188075855872,
	360287970189639680,
	720575940379279360,
	1441151880758558720,
	2882303761517117440,
	5764607523034234880,
	11529215046068469760,
	4611686018427387904,
	0,
	0,
	0,
	0,
	0,
	0,
	0,
	0
]

cdef U64[64] KING_ATTACKS = [
	770,
	1797,
	3594,
	7188,
	14376,
	28752,
	57504,
	49216,
	197123,
	460039,
	920078,
	1840156,
	3680312,
	7360624,
	14721248,
	12599488,
	50463488,
	117769984,
	235539968,
	471079936,
	942159872,
	1884319744,
	3768639488,
	3225468928,
	12918652928,
	30149115904,
	60298231808,
	120596463616,
	241192927232,
	482385854464,
	964771708928,
	825720045568,
	3307175149568,
	7718173671424,
	15436347342848,
	30872694685696,
	61745389371392,
	123490778742784,
	246981557485568,
	211384331665408,
	846636838289408,
	1975852459884544,
	3951704919769088,
	7903409839538176,
	15806819679076352,
	31613639358152704,
	63227278716305408,
	54114388906344448,
	216739030602088448,
	505818229730443264,
	1011636459460886528,
	2023272918921773056,
	4046545837843546112,
	8093091675687092224,
	16186183351374184448,
	13853283560024178688,
	144959613005987840,
	362258295026614272,
	724516590053228544,
	1449033180106457088,
	2898066360212914176,
	5796132720425828352,
	11592265440851656704,
	4665729213955833856,
]


cdef U64[64] KNIGHT_ATTACKS = [
	132096,
	329728,
	659712,
	1319424,
	2638848,
	5277696,
	10489856,
	4202496,
	33816580,
	84410376,
	168886289,
	337772578,
	675545156,
	1351090312,
	2685403152,
	1075839008,
	8657044482,
	21609056261,
	43234889994,
	86469779988,
	172939559976,
	345879119952,
	687463207072,
	275414786112,
	2216203387392,
	5531918402816,
	11068131838464,
	22136263676928,
	44272527353856,
	88545054707712,
	175990581010432,
	70506185244672,
	567348067172352,
	1416171111120896,
	2833441750646784,
	5666883501293568,
	11333767002587136,
	22667534005174272,
	45053588738670592,
	18049583422636032,
	145241105196122112,
	362539804446949376,
	725361088165576704,
	1450722176331153408,
	2901444352662306816,
	5802888705324613632,
	11533718717099671552,
	4620693356194824192,
	288234782788157440,
	576469569871282176,
	1224997833292120064,
	2449995666584240128,
	4899991333168480256,
	9799982666336960512,
	1152939783987658752,
	2305878468463689728,
	1128098930098176,
	2257297371824128,
	4796069720358912,
	9592139440717824,
	19184278881435648,
	38368557762871296,
	4679521487814656,
	9077567998918656,
]


cdef U64[64] ROOK_OCCUPANCY = [
	282578800148862,
	565157600297596,
	1130315200595066,
	2260630401190006,
	4521260802379886,
	9042521604759646,
	18085043209519166,
	36170086419038334,
	282578800180736,
	565157600328704,
	1130315200625152,
	2260630401218048,
	4521260802403840,
	9042521604775424,
	18085043209518592,
	36170086419037696,
	282578808340736,
	565157608292864,
	1130315208328192,
	2260630408398848,
	4521260808540160,
	9042521608822784,
	18085043209388032,
	36170086418907136,
	282580897300736,
	565159647117824,
	1130317180306432,
	2260632246683648,
	4521262379438080,
	9042522644946944,
	18085043175964672,
	36170086385483776,
	283115671060736,
	565681586307584,
	1130822006735872,
	2261102847592448,
	4521664529305600,
	9042787892731904,
	18085034619584512,
	36170077829103616,
	420017753620736,
	699298018886144,
	1260057572672512,
	2381576680245248,
	4624614895390720,
	9110691325681664,
	18082844186263552,
	36167887395782656,
	35466950888980736,
	34905104758997504,
	34344362452452352,
	33222877839362048,
	30979908613181440,
	26493970160820224,
	17522093256097792,
	35607136465616896,
	9079539427579068672,
	8935706818303361536,
	8792156787827803136,
	8505056726876686336,
	7930856604974452736,
	6782456361169985536,
	4485655873561051136,
	9115426935197958144,
]

cdef U64[64] BISHOP_OCCUPANCY = [
	18049651735527936,
	70506452091904,
	275415828992,
	1075975168,
	38021120,
	8657588224,
	2216338399232,
	567382630219776,
	9024825867763712,
	18049651735527424,
	70506452221952,
	275449643008,
	9733406720,
	2216342585344,
	567382630203392,
	1134765260406784,
	4512412933816832,
	9024825867633664,
	18049651768822272,
	70515108615168,
	2491752130560,
	567383701868544,
	1134765256220672,
	2269530512441344,
	2256206450263040,
	4512412900526080,
	9024834391117824,
	18051867805491712,
	637888545440768,
	1135039602493440,
	2269529440784384,
	4539058881568768,
	1128098963916800,
	2256197927833600,
	4514594912477184,
	9592139778506752,
	19184279556981248,
	2339762086609920,
	4538784537380864,
	9077569074761728,
	562958610993152,
	1125917221986304,
	2814792987328512,
	5629586008178688,
	11259172008099840,
	22518341868716544,
	9007336962655232,
	18014673925310464,
	2216338399232,
	4432676798464,
	11064376819712,
	22137335185408,
	44272556441600,
	87995357200384,
	35253226045952,
	70506452091904,
	567382630219776,
	1134765260406784,
	2832480465846272,
	5667157807464448,
	11333774449049600,
	22526811443298304,
	9024825867763712,
	18049651735527936,
]

cdef U8[64] ROOK_OCCUPANCY_BITS = [
	12,11,11,11,11,11,11,12,
	11,10,10,10,10,10,10,11,
	11,10,10,10,10,10,10,11,
	11,10,10,10,10,10,10,11,
	11,10,10,10,10,10,10,11,
	11,10,10,10,10,10,10,11,
	11,10,10,10,10,10,10,11,
	12,11,11,11,11,11,11,12
]

cdef U8[64] BISHOP_OCCUPANCY_BITS = [
	6,5,5,5,5,5,5,6,
	5,5,5,5,5,5,5,5,
	5,5,7,7,7,7,5,5,
	5,5,7,9,9,7,5,5,
	5,5,7,9,9,7,5,5,
	5,5,7,7,7,7,5,5,
	5,5,5,5,5,5,5,5,
	6,5,5,5,5,5,5,6
]


cdef U64[64] ROOK_MAGIC_NUMBERS = [
	36029381405327360,
	1170971088562163712,
	612524735842488320,
	72075186291671072,
	144117387368072224,
	144132784624501248,
	144115743334859264,
	108087490574033024,
	36169536658997280,
	2305984021588353028,
	581105158147022852,
	4611826790276530306,
	9295570402741059712,
	144255942752469504,
	9548757145382686788,
	1297599644532080772,
	36833643725440,
	9876396457261547520,
	141287512612864,
	2252351717511168,
	73184043768217728,
	9517232462330070144,
	1139094181642801,
	865256277972911121,
	18014675534880896,
	87962003972104,
	17611515494784,
	11003710410784,
	8798248895488,
	289356295386038400,
	577588868413919361,
	1173258630019957761,
	9901234168853955632,
	76704165643952384,
	333829460925091968,
	3386637564252160,
	7278945646592133120,
	1127000496407040,
	37718200963564552,
	5207288151277824,
	141012368392192,
	2319354083511123968,
	35189757771792,
	325402665448177696,
	9223935004525592592,
	576465150383521920,
	1173470346280697858,
	563229671686148,
	564051616735744,
	18014684141593856,
	439815466125440,
	9895873094400,
	8798240768128,
	648522746535477376,
	1175580248822055040,
	1157706581899608320,
	2378279936910696513,
	13835075793539580162,
	598134460924161,
	4652218449501683745,
	562985665840130,
	79375950479380482,
	576478417640358020,
	45599496524071938
]


cdef U64[64] BISHOP_MAGIC_NUMBERS = [
	1225647816496513056,
	9027267506275584,
	1768093866612753408,
	9226821205377434624,
	565217712996384,
	1157711119863775297,
	2305984314455656449,
	576480577939833876,
	1207070271572804672,
	1251312969846914,
	9306597566523520,
	2476065558528,
	3171101675184324736,
	576497242481889536,
	3747012761400385602,
	2341896013780370432,
	2256472872387616,
	1161930975966429312,
	1143526455509008,
	1155179918739376130,
	577305196833542162,
	9290909768221185,
	2459809976173072384,
	4647855845597254144,
	6919852433217749506,
	9297480794558720,
	4612830635835785472,
	9385642500548592128,
	2305988145025392672,
	2260733379348768,
	145241672165393408,
	2882866917968972291,
	4040300628981854464,
	9516670680574464001,
	1162071916694733824,
	35223028893952,
	9227895429843652612,
	9223530924875514112,
	155392333385336834,
	4648278048901186049,
	146369195804729605,
	1153066708904216576,
	720593824761516032,
	36170917520941088,
	9223763497521778720,
	40567583182849160,
	2254033338245632,
	288555833749672192,
	4692822348964999234,
	74769014718732,
	9281963370842488896,
	69265264656,
	720861891251535872,
	360323176305033792,
	9016172114378788,
	1587817937966792712,
	281784281532416,
	2252366757892353,
	38298258284744732,
	4629718056369686600,
	1153079834351553536,
	18014742648521985,
	288235397036114048,
	4521201074455568,
]


cdef U64[64] CASTLINGCONSTANTS = [
	7, 15, 15, 15, 3, 15, 15, 11,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	15, 15, 15, 15, 15, 15, 15, 15,
	13, 15, 15, 15, 12, 15, 15, 14	  
]

cdef U8 i

with open('rookAttacks.dat','rb') as f:
	temp_ROOK_ATTACKS = pickle.load(f)

cdef U64[64][4096] ROOK_ATTACKS

for i in range(64):
	ROOK_ATTACKS[i] = temp_ROOK_ATTACKS[i]


with open('bishopAttacks.dat','rb') as f:
	temp_BISHOP_ATTACKS = pickle.load(f)

cdef U64[64][512] BISHOP_ATTACKS

for i in range(64):
	BISHOP_ATTACKS[i] = temp_BISHOP_ATTACKS[i]


del temp_BISHOP_ATTACKS, temp_ROOK_ATTACKS


'''
DATA ENDS HERE
'''


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef U8 count_bits(U64 bit_board):
	cdef U8 c = 0
	while bit_board:
		bit_board &= bit_board - 1
		c += 1
	return c


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef  U8 least_significant_bit_count(U64 bit_board):
	return count_bits((bit_board & -bit_board) - 1)


ctypedef struct Moves:
	U8 count
	U32 move_list[218]


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef void add_move(Moves moves[1], U32 source, U32 target, U32 piece, U32 promoted, U32 promoted_piece, U32 enpassant, U32 castling):
		moves[0].move_list[moves[0].count] = (source) | (target << 6) | (piece << 12) | (promoted << 16) | (promoted_piece << 17) | (enpassant << 19) | (castling << 20) 
		moves[0].count += 1


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef void print_chess_board(U64 bitboards[12], U32 board_data):
	cdef U8 c = 0
	cdef U8 i
	cdef U8 j
	cdef U8 k

	for i in range(8):
		print(8 - i, '    ', end ='')
		for j in range(8):
			for k in range(12):
				if bitboards[k] & (one << c):
					print(f'{piece_string[k]}   ', end = '')
					break
			else:
				print('    ', end = '')
			c += 1
		print('\n')
	print()        
	print('      A   B   C   D   E   F   G   H')
	print()
	print(f'Side to move: {"Black" if (board_data & (1)) else "White"}')
	print()
	print(f'Castling rights: {"K" if ((board_data >> (1)) & (1)) else "-"}{"Q" if ((board_data >> (2)) & (1)) else "-"}{"k" if ((board_data >> (3)) & (1)) else "-"}{"q" if ((board_data >> (4)) & (1)) else "-"}')
	print()
	print(f'En Passant: {"Not possible" if not (board_data & (1 << 5)) else square_string[((board_data >> (6)) & ((1 << 6) - 1))]}')
	print()
	print(f'Half Moves: {(board_data >> (12)) & (((1 << 6 ) - 1))}')
	print()
	print('Board Data:', bin(board_data))
	print('\n')


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef bint is_square_attacked(U8 side, U8 square, U64 bitboards[12], U64 black_pieces, U64 white_pieces):

	if side == 0:
		if bitboards[0] & BLACK_PAWN_ATTACKS[square]:
			return True
		elif bitboards[1] & KNIGHT_ATTACKS[square]:
			return True
		elif (bitboards[2] | bitboards[4]) & BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> (64 - BISHOP_OCCUPANCY_BITS[square]))] & (~white_pieces):
			return True
		elif (bitboards[3] | bitboards[4]) & ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * ROOK_MAGIC_NUMBERS[square]) >> (64 - ROOK_OCCUPANCY_BITS[square]))] & (~white_pieces):
			return True
		elif bitboards[5] & KING_ATTACKS[square]:
			return True
	else:
		if bitboards[6] & WHITE_PAWN_ATTACKS[square]:
			return True
		elif bitboards[7] & KNIGHT_ATTACKS[square]:
			return True
		elif (bitboards[8] | bitboards[10]) & BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> (64 - BISHOP_OCCUPANCY_BITS[square]))] & (~black_pieces):
			return True
		elif (bitboards[9] | bitboards[10]) & ROOK_ATTACKS[square][(((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * ROOK_MAGIC_NUMBERS[square]) >> (64 - ROOK_OCCUPANCY_BITS[square]))] & (~black_pieces):
			return True
		elif bitboards[11] & KING_ATTACKS[square]:
			return True

	return False


@cython.binding(False)
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef Moves return_moves(U64 bitboards[12], U32 board_data):

	cdef U64 WHITE_PAWNS = bitboards[0]
	cdef U64 WHITE_KNIGHTS = bitboards[1]
	cdef U64 WHITE_BISHOPS = bitboards[2]
	cdef U64 WHITE_ROOKS = bitboards[3]
	cdef U64 WHITE_QUEEN = bitboards[4]
	cdef U64 WHITE_KING = bitboards[5]

	cdef U64 BLACK_PAWNS = bitboards[6]
	cdef U64 BLACK_KNIGHTS = bitboards[7]
	cdef U64 BLACK_BISHOPS = bitboards[8]
	cdef U64 BLACK_ROOKS = bitboards[9]
	cdef U64 BLACK_QUEEN = bitboards[10]
	cdef U64 BLACK_KING = bitboards[11]

	cdef U64 WHITE_PIECES = (
		WHITE_BISHOPS
		| WHITE_KING
		| WHITE_KNIGHTS
		| WHITE_PAWNS
		| WHITE_QUEEN
		| WHITE_ROOKS
	)

	cdef U64 BLACK_PIECES = (
		BLACK_BISHOPS
		| BLACK_KING
		| BLACK_KNIGHTS
		| BLACK_PAWNS
		| BLACK_QUEEN
		| BLACK_ROOKS
	)

	cdef U64 ALL_PIECES = BLACK_PIECES | WHITE_PIECES

	cdef Moves[1] moves = [Moves(0)]
	cdef U8 curr_square
	cdef U8 to_square
	cdef U64 attacks
	
	if board_data & 1 == 0:
		
		while WHITE_PAWNS:
			
			curr_square = least_significant_bit_count(WHITE_PAWNS)
			WHITE_PAWNS ^= (one << curr_square)
			attacks = WHITE_PAWN_ATTACKS[curr_square] & BLACK_PIECES
			
			if 8 <= curr_square <= 15:
				
				while attacks:

					to_square = least_significant_bit_count(attacks)
					attacks ^= (one << to_square)
					add_move(moves, curr_square, to_square, 0, 1, 0, 0, 0)
					add_move(moves, curr_square, to_square, 0, 1, 1, 0, 0)
					add_move(moves, curr_square, to_square, 0, 1, 2, 0, 0)
					add_move(moves, curr_square, to_square, 0, 1, 3, 0, 0)
				
				if (one << (curr_square - 8)) & (~ALL_PIECES):

					add_move(moves, curr_square, curr_square - 8, 0, 1, 0, 0, 0)
					add_move(moves, curr_square, curr_square - 8, 0, 1, 1, 0, 0)
					add_move(moves, curr_square, curr_square - 8, 0, 1, 2, 0, 0)
					add_move(moves, curr_square, curr_square - 8, 0, 1, 3, 0, 0)
			
			else:

				while attacks:

					to_square = least_significant_bit_count(attacks)
					attacks ^= (one << to_square)
					add_move(moves, curr_square, to_square, 0, 0, 0, 0, 0)

				if (one << (curr_square - 8)) & (~ALL_PIECES):
					
					if 48 <= curr_square <= 55 and (one << (curr_square - 16)) & (~ALL_PIECES):
						
						add_move(moves, curr_square, curr_square - 8, 0, 0, 0, 0, 0)
						add_move(moves, curr_square, curr_square - 16, 0, 0, 0, 0, 0)
					
					else:

						add_move(moves, curr_square, curr_square - 8, 0, 0, 0, 0, 0)
				
				
				if (board_data & (1 << 5)) and (((board_data >> 6) & ((1 << 6) - 1)) == (curr_square - 9) or (((board_data >> 6)) & ((1 << 6) - 1)) == (curr_square - 7)):

					add_move(moves, curr_square, ((board_data >> 6 & ((1 << 6) - 1))), 0, 0, 0, 1, 0)
		
		while WHITE_KNIGHTS:

			curr_square = least_significant_bit_count(WHITE_KNIGHTS)
			WHITE_KNIGHTS ^= (one << curr_square)
			attacks = KNIGHT_ATTACKS[curr_square] & (~WHITE_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 1, 0, 0, 0, 0)
	
		while WHITE_BISHOPS:

			curr_square = least_significant_bit_count(WHITE_BISHOPS)
			WHITE_BISHOPS ^= (one << curr_square)
			attacks = BISHOP_ATTACKS[curr_square][
				(
					(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
					>> (64 - BISHOP_OCCUPANCY_BITS[curr_square]
				)
			] & (~WHITE_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 2, 0, 0, 0, 0)


		while WHITE_ROOKS:
			
			curr_square = least_significant_bit_count(WHITE_ROOKS)
			WHITE_ROOKS ^= (one << curr_square)
			attacks = ROOK_ATTACKS[curr_square][
				(
					(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
					>> (64 - ROOK_OCCUPANCY_BITS[curr_square]
				)
			] & (~WHITE_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 3, 0, 0, 0, 0)


		while WHITE_QUEEN:

			curr_square = least_significant_bit_count(WHITE_QUEEN)
			WHITE_QUEEN^= (one << curr_square)
			attacks = BISHOP_ATTACKS[curr_square][
				(
					(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
					>> (64 - BISHOP_OCCUPANCY_BITS[curr_square]
				)
			] & (~WHITE_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 4, 0, 0, 0, 0)

			attacks = ROOK_ATTACKS[curr_square][
				(
					(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
					>> (64 - ROOK_OCCUPANCY_BITS[curr_square]
				)
			] & (~WHITE_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 4, 0, 0, 0, 0)

		while WHITE_KING:

			curr_square = least_significant_bit_count(WHITE_KING)
			WHITE_KING ^= (one << curr_square)
			attacks = KING_ATTACKS[curr_square] & (~WHITE_PIECES)
			
			while attacks:
				
				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 5, 0, 0, 0, 0)

			if board_data & 2 and not (ALL_PIECES & ((one << 62) | (one << 61))) and not is_square_attacked(1, 61, bitboards, BLACK_PIECES, WHITE_PIECES) and not is_square_attacked(1, 60, bitboards, BLACK_PIECES, WHITE_PIECES):

				add_move(moves, curr_square, 62, 5, 0, 0, 0, 1)

			if board_data & 4 and not (ALL_PIECES & ((one << 59) | (one << 58) | (one << 57))) and not is_square_attacked(1, 59, bitboards, BLACK_PIECES, WHITE_PIECES) and not is_square_attacked(1, 60, bitboards, BLACK_PIECES, WHITE_PIECES):

				add_move(moves, curr_square, 58, 5, 0, 0, 0, 1)

	else:

		while BLACK_PAWNS:
			
			curr_square = least_significant_bit_count(BLACK_PAWNS)
			BLACK_PAWNS ^= (one << curr_square)
			attacks = BLACK_PAWN_ATTACKS[curr_square] & WHITE_PIECES

			if 56 <= curr_square <= 63:

				while attacks:
					
					to_square = least_significant_bit_count(attacks)
					attacks ^= (one << to_square)
					add_move(moves, curr_square, to_square, 6, 1, 0, 0, 0)
					add_move(moves, curr_square, to_square, 6, 1, 1, 0, 0)
					add_move(moves, curr_square, to_square, 6, 1, 2, 0, 0)
					add_move(moves, curr_square, to_square, 6, 1, 3, 0, 0)

				if (one << (curr_square + 8)) & (~ALL_PIECES):
					
					add_move(moves, curr_square, curr_square + 8, 6, 1, 0, 0, 0)
					add_move(moves, curr_square, curr_square + 8, 6, 1, 1, 0, 0)
					add_move(moves, curr_square, curr_square + 8, 6, 1, 2, 0, 0)
					add_move(moves, curr_square, curr_square + 8, 6, 1, 3, 0, 0)

			else:

				while attacks:
					
					to_square = least_significant_bit_count(attacks)
					attacks ^= (one << to_square)
					add_move(moves, curr_square, to_square, 6, 0, 0, 0, 0)

				if (one << (curr_square + 8)) & (~ALL_PIECES):

					if 8 <= curr_square <= 15 and (one << (curr_square + 16)) & (~ALL_PIECES):
						
						add_move(moves, curr_square, curr_square + 8, 6, 0, 0, 0, 0)
						add_move(moves, curr_square, curr_square + 16, 6, 0, 0, 0, 0)

					else:
						
						add_move(moves, curr_square, curr_square + 8, 6, 0, 0, 0, 0)

				if (board_data & (1 << 5)) and (((board_data >> 6) & ((1 << 6) - 1)) == (curr_square + 9) or (((board_data >> 6) & ((1 << 6) - 1)) == curr_square + 7)):
					
					add_move(moves, curr_square, (((board_data >> 6) & ((1 << 6) - 1))), 6, 0, 0, 1, 0)

		while BLACK_KNIGHTS:
			
			curr_square = least_significant_bit_count(BLACK_KNIGHTS)
			BLACK_KNIGHTS ^= (one << curr_square)
			attacks = KNIGHT_ATTACKS[curr_square] & (~BLACK_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 7, 0, 0, 0, 0)
	
		while BLACK_BISHOPS:

			curr_square = least_significant_bit_count(BLACK_BISHOPS)
			BLACK_BISHOPS ^= (one << curr_square)
			attacks = BISHOP_ATTACKS[curr_square][
				(
					(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
					>> (64 - BISHOP_OCCUPANCY_BITS[curr_square]
				)
			] & (~BLACK_PIECES)

			while attacks:
				
				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 8, 0, 0, 0, 0)

		while BLACK_ROOKS:
			
			curr_square = least_significant_bit_count(BLACK_ROOKS)
			BLACK_ROOKS ^= (one << curr_square)
			attacks = ROOK_ATTACKS[curr_square][
				(
					(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
					>> (64 - ROOK_OCCUPANCY_BITS[curr_square]
				)
			] & (~BLACK_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 9, 0, 0, 0, 0)


		while BLACK_QUEEN:

			curr_square = least_significant_bit_count(BLACK_QUEEN)
			BLACK_QUEEN^= (one << curr_square)
			attacks = BISHOP_ATTACKS[curr_square][
				(
					(BISHOP_OCCUPANCY[curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[curr_square])
					>> (64 - BISHOP_OCCUPANCY_BITS[curr_square]
				)
			] & (~BLACK_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 10, 0, 0, 0, 0)

			attacks = ROOK_ATTACKS[curr_square][
				(
					(ROOK_OCCUPANCY[curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square])
					>> (64 - ROOK_OCCUPANCY_BITS[curr_square]
				)
			] & (~BLACK_PIECES)

			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 10, 0, 0, 0, 0)

		while BLACK_KING:

			curr_square = least_significant_bit_count(BLACK_KING)
			BLACK_KING ^= (one << curr_square)
			attacks = KING_ATTACKS[curr_square] & (~BLACK_PIECES)
			
			while attacks:

				to_square = least_significant_bit_count(attacks)
				attacks ^= (one << to_square)
				add_move(moves, curr_square, to_square, 11, 0, 0, 0, 0)

			if board_data & 8 and not (ALL_PIECES & ((one << 5) | (one << 6))) and not is_square_attacked(0, 3, bitboards, BLACK_PIECES, WHITE_PIECES) and not is_square_attacked(0, 4, bitboards, BLACK_PIECES, WHITE_PIECES):
				add_move(moves, curr_square, 6, 11, 0, 0, 0, 1)

			if board_data & 16 and not (ALL_PIECES & ((one << 1) | (one << 2) | (one << 3))) and not is_square_attacked(0, 4, bitboards, BLACK_PIECES, WHITE_PIECES) and not is_square_attacked(0, 5, bitboards, BLACK_PIECES, WHITE_PIECES):
				add_move(moves, curr_square, 2, 11, 0, 0, 0, 1)
	
	return moves[0]


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef void perft():
	import time
	stime = time.time()
	for i in range(2_000_000):
		return_moves(BITBOARDS, BOARD_DATA)
	print(f"Time: {time.time() - stime}")


def ReturnMoves(BitBoards, BoardData):

	cdef U64[12] bitboards = BitBoards

	cdef U32 board_data = BoardData

	moves = return_moves(bitboards, board_data)

	return moves