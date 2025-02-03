from fen import *
import pickle
cimport cython


ctypedef (unsigned long long) U64
ctypedef (unsigned int) U32
ctypedef (unsigned char) U8
cdef U64 one = 1
cdef U32 one32 = 1


temp_BITBOARDS, temp_data = generate_bitboards_from_board(fenString)
cdef U64[12] BITBOARDS
cdef U32 BOARD_DATA = temp_data
for i in range(12):
    BITBOARDS[i] = temp_BITBOARDS[i]
del temp_BITBOARDS, temp_data


square_string = [
    'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8',
    'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7',
    'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6',
    'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5',
    'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4',
    'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3',
    'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2',
    'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']


piece_string = "PNBRQKpnbrqk"


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


with open('chess-2.0/rookAttacks.dat','rb') as f:
    temp_ROOK_ATTACKS = pickle.load(f)
cdef U64[64][4096] ROOK_ATTACKS
for i in range(64):
    ROOK_ATTACKS[i] = temp_ROOK_ATTACKS[i]
with open('chess-2.0/bishopAttacks.dat','rb') as f:
    temp_BISHOP_ATTACKS = pickle.load(f)
cdef U64[64][512] BISHOP_ATTACKS
for i in range(64):
    BISHOP_ATTACKS[i] = temp_BISHOP_ATTACKS[i]
del temp_BISHOP_ATTACKS, temp_ROOK_ATTACKS


cdef int[64] Pawns = [
        0,   0,   0,   0,   0,   0,   0,   0,
        50,  50,  50,  50,  50,  50,  50,  50,
        10,  10,  20,  30,  30,  20,  10,  10,
        5,   5,  10,  25,  25,  10,   5,   5,
        0,   0,   0,  20,  20,   0,   0,   0,
        5,  -5, -10,   0,   0, -10,  -5,   5,
        5,  10,  10, -20, -20,  10,  10,   5,
        0,   0,   0,   0,   0,   0,   0,   0
]
cdef int[64] Rooks =  [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]
cdef int[64] Knights = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]
cdef int[64] Bishops =  [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]
cdef int[64] Queens =  [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,   0,  5,  5,  5,  5,  0, -5,
    0,    0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
cdef int[64] King = [
    -80, -70, -70, -70, -70, -70, -70, -80, 
    -60, -60, -60, -60, -60, -60, -60, -60, 
    -40, -50, -50, -60, -60, -50, -50, -40, 
    -30, -40, -40, -50, -50, -40, -40, -30, 
    -20, -30, -30, -40, -40, -30, -30, -20, 
    -10, -20, -20, -20, -20, -20, -20, -10, 
    20,  20,  -5,  -5,  -5,  -5,  20,  20, 
    20,  30,  10,   0,   0,  10,  30,  20
]


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
cdef U8 least_significant_bit_count(U64 bit_board):
    return count_bits((bit_board & -bit_board) - 1)


cdef class Moves:

    cdef U32[218] move_list
    cdef U8 count    
    
    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    def __cinit__(self):
        self.count = 0
    
    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef void add_move(self, U32 source, U32 target, U32 piece, U32 promoted,
     U32 promoted_piece, U32 enpassant, U32 castling):
            self.move_list[self.count] = ((source) | (target << 6) | 
            (piece << 12) | (promoted << 16) | (promoted_piece << 17) | 
            (enpassant << 19) | (castling << 20))
            self.count += 1

    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef return_move_list(self):
        return self.move_list

    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef return_count(self):
        return self.count


cdef class Board:

    cdef:
        public U64[12] bitboards
        public U32 board_data

    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    def __cinit__(self, bit_boards, boarddata):
        self.board_data = boarddata
        cdef U8 i
        for i in range(12):
            self.bitboards[i] = bit_boards[i]

    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef void print_chess_board(self):
        cdef U8 c = 0
        cdef U8 i
        cdef U8 j
        cdef U8 k
        for i in range(8):
            print(8 - i, '    ', end ='')
            for j in range(8):
                for k in range(12):
                    if self.bitboards[k] & (one << c):
                        print(f'{piece_string[k]}   ', end = '')
                        break
                else:
                    print('    ', end = '')
                c += 1
            print('\n')
        print()        
        print('      A   B   C   D   E   F   G   H')
        print()
        print(f'Side to move: {"Black" if (self.board_data & (1)) else "White"}')
        print()
        print('Castling rights:'
        f' {"K" if ((self.board_data >> (1)) & (1)) else "-"}'
        f'{"Q" if ((self.board_data >> (2)) & (1)) else "-"}'
        f'{"k" if ((self.board_data >> (3)) & (1)) else "-"}'
        f'{"q" if ((self.board_data >> (4)) & (1)) else "-"}')
        print()
        print('En Passant:', 
        "Not possible" if not (self.board_data & (1 << 5)) else square_string[
            ((self.board_data >> (6)) & ((1 << 6) - 1))])
        print()
        print(f'Half Moves: {(self.board_data >> (12)) & (((1 << 6 ) - 1))}')
        print()
        print('Board Data:', bin(self.board_data))
        print('\n')
    
    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef bint is_square_attacked(self, U8 side, U8 square,
     U64 black_pieces, U64 white_pieces):
        if side == 0:
            if self.bitboards[0] & BLACK_PAWN_ATTACKS[square]:
                return True
            elif self.bitboards[1] & KNIGHT_ATTACKS[square]:
                return True
            elif (self.bitboards[2] | self.bitboards[4]) & (
                BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & 
                (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> 
                (64 - BISHOP_OCCUPANCY_BITS[square]))] & (~black_pieces)):
                return True
            elif (self.bitboards[3] | self.bitboards[4]) & (ROOK_ATTACKS[square][
                (((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * 
                ROOK_MAGIC_NUMBERS[square]) >> 
                (64 - ROOK_OCCUPANCY_BITS[square]))] & (~black_pieces)):
                return True
            elif self.bitboards[5] & KING_ATTACKS[square]:
                return True
        else:
            if self.bitboards[6] & WHITE_PAWN_ATTACKS[square]:
                return True
            elif self.bitboards[7] & KNIGHT_ATTACKS[square]:
                return True
            elif (self.bitboards[8] | self.bitboards[10]) & (
                BISHOP_ATTACKS[square][(((BISHOP_OCCUPANCY[square] & 
                (black_pieces | white_pieces)) * BISHOP_MAGIC_NUMBERS[square]) >> 
                (64 - BISHOP_OCCUPANCY_BITS[square]))] & (~white_pieces)):
                return True
            elif (self.bitboards[9] | self.bitboards[10]) & (ROOK_ATTACKS[square][
                (((ROOK_OCCUPANCY[square] & (black_pieces | white_pieces)) * 
                ROOK_MAGIC_NUMBERS[square]) >> 
                (64 - ROOK_OCCUPANCY_BITS[square]))] & (~white_pieces)):
                return True
            elif self.bitboards[11] & KING_ATTACKS[square]:
                return True
        return False

    cpdef bint check_for_check(self, U8 side):
        if side == 0:
            return self.is_square_attacked(not side, 
            least_significant_bit_count(self.bitboards[5]), 
            (self.bitboards[6] | self.bitboards[7] | self.bitboards[8] | 
            self.bitboards[9] | self.bitboards[10] | self.bitboards[11]), 
            (self.bitboards[0] | self.bitboards[1] | self.bitboards[2] | 
            self.bitboards[3] | self.bitboards[4] | self.bitboards[5]))
        else:
            return  self.is_square_attacked(not side, 
            least_significant_bit_count(self.bitboards[11]), 
            (self.bitboards[6] | self.bitboards[7] | self.bitboards[8] | 
            self.bitboards[9] | self.bitboards[10] | self.bitboards[11]), 
            (self.bitboards[0] | self.bitboards[1] | self.bitboards[2] | 
            self.bitboards[3] | self.bitboards[4] | self.bitboards[5]))

    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef Moves return_moves(self):
        cdef U64 WHITE_PAWNS = self.bitboards[0]
        cdef U64 WHITE_KNIGHTS = self.bitboards[1]
        cdef U64 WHITE_BISHOPS = self.bitboards[2]
        cdef U64 WHITE_ROOKS = self.bitboards[3]
        cdef U64 WHITE_QUEEN = self.bitboards[4]
        cdef U64 WHITE_KING = self.bitboards[5]
        cdef U64 BLACK_PAWNS = self.bitboards[6]
        cdef U64 BLACK_KNIGHTS = self.bitboards[7]
        cdef U64 BLACK_BISHOPS = self.bitboards[8]
        cdef U64 BLACK_ROOKS = self.bitboards[9]
        cdef U64 BLACK_QUEEN = self.bitboards[10]
        cdef U64 BLACK_KING = self.bitboards[11]
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
        cdef Moves moves = Moves()
        cdef U8 curr_square
        cdef U8 to_square
        cdef U64 attacks        
        if self.board_data & 1 == 0:
            while WHITE_PAWNS:
                curr_square = least_significant_bit_count(WHITE_PAWNS)
                WHITE_PAWNS ^= (one << curr_square)
                attacks = WHITE_PAWN_ATTACKS[curr_square] & BLACK_PIECES
                if 8 <= curr_square <= 15:
                    while attacks:
                        to_square = least_significant_bit_count(attacks)
                        attacks ^= (one << to_square)
                        moves.add_move(curr_square, to_square, 0, 1, 0, 0, 0)
                        moves.add_move(curr_square, to_square, 0, 1, 1, 0, 0)
                        moves.add_move(curr_square, to_square, 0, 1, 2, 0, 0)
                        moves.add_move(curr_square, to_square, 0, 1, 3, 0, 0)
                    if (one << (curr_square - 8)) & (~ALL_PIECES):
                        moves.add_move(curr_square, curr_square - 8, 0, 1, 0, 0, 0)
                        moves.add_move(curr_square, curr_square - 8, 0, 1, 1, 0, 0)
                        moves.add_move(curr_square, curr_square - 8, 0, 1, 2, 0, 0)
                        moves.add_move(curr_square, curr_square - 8, 0, 1, 3, 0, 0)
                else:
                    while attacks:
                        to_square = least_significant_bit_count(attacks)
                        attacks ^= (one << to_square)
                        moves.add_move(curr_square, to_square, 0, 0, 0, 0, 0)
                    if (one << (curr_square - 8)) & (~ALL_PIECES):
                        if 48 <= curr_square <= 55 and ((one << (
                            curr_square - 16)) & (~ALL_PIECES)):
                            moves.add_move(curr_square, curr_square - 8, 
                            0, 0, 0, 0, 0)
                            moves.add_move(curr_square, curr_square - 16, 
                            0, 0, 0, 0, 0)
                        else:
                            moves.add_move(curr_square, curr_square - 8, 
                            0, 0, 0, 0, 0)
                    if (self.board_data & (1 << 5)) and (((self.board_data >> 
                    (6)) & ((1 << 6) - 1)) == (curr_square - 9) or (((
                        self.board_data >> (6)) & 
                        ((1 << 6) - 1)) == curr_square - 7)):
                        moves.add_move(curr_square, ((self.board_data >> (6) & 
                        ((1 << 6) - 1))), 0, 0, 0, 1, 0)
            while WHITE_KNIGHTS:
                curr_square = least_significant_bit_count(WHITE_KNIGHTS)
                WHITE_KNIGHTS ^= (one << curr_square)             
                attacks = KNIGHT_ATTACKS[curr_square] & (~WHITE_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 1, 0, 0, 0, 0)
            while WHITE_BISHOPS:
                curr_square = least_significant_bit_count(WHITE_BISHOPS)
                WHITE_BISHOPS ^= (one << curr_square)
                attacks = BISHOP_ATTACKS[curr_square][((BISHOP_OCCUPANCY[
                    curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[
                        curr_square]) >> (64 - BISHOP_OCCUPANCY_BITS[
                            curr_square])] & (~WHITE_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 2, 0, 0, 0, 0)
            while WHITE_ROOKS:
                curr_square = least_significant_bit_count(WHITE_ROOKS)
                WHITE_ROOKS ^= (one << curr_square)
                attacks = ROOK_ATTACKS[curr_square][((ROOK_OCCUPANCY[curr_square] &
                ALL_PIECES) * ROOK_MAGIC_NUMBERS[curr_square]) >> 
                (64 - ROOK_OCCUPANCY_BITS[curr_square])] & (~WHITE_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 3, 0, 0, 0, 0)
            while WHITE_QUEEN:
                curr_square = least_significant_bit_count(WHITE_QUEEN)
                WHITE_QUEEN^= (one << curr_square)
                attacks = BISHOP_ATTACKS[curr_square][((BISHOP_OCCUPANCY[
                    curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[
                        curr_square]) >> (64 - BISHOP_OCCUPANCY_BITS[
                            curr_square])] & (~WHITE_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 4, 0, 0, 0, 0)
                attacks = ROOK_ATTACKS[curr_square][((ROOK_OCCUPANCY[
                    curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[
                        curr_square]) >> (64 - ROOK_OCCUPANCY_BITS[
                            curr_square])] & (~WHITE_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 4, 0, 0, 0, 0)
            while WHITE_KING:
                curr_square = least_significant_bit_count(WHITE_KING)
                WHITE_KING ^= (one << curr_square)
                attacks = KING_ATTACKS[curr_square] & (~WHITE_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 5, 0, 0, 0, 0)
                if self.board_data & (2) and not (ALL_PIECES & 
                ((one << 62) | (one << 61))) and not self.is_square_attacked(1, 
                61, BLACK_PIECES, WHITE_PIECES) and not self.is_square_attacked(1, 
                60, BLACK_PIECES, WHITE_PIECES):
                    moves.add_move(curr_square, 62, 5, 0, 0, 0, 1)
                if self.board_data & (4) and not (ALL_PIECES & ((one << 59) | 
                (one << 58) | (one << 57))) and not self.is_square_attacked(1, 
                59, BLACK_PIECES, WHITE_PIECES) and not self.is_square_attacked(1, 
                60, BLACK_PIECES, WHITE_PIECES):
                    moves.add_move(curr_square, 58, 5, 0, 0, 0, 1)
        else:
            while BLACK_PAWNS:
                curr_square = least_significant_bit_count(BLACK_PAWNS)
                BLACK_PAWNS ^= (one << curr_square)
                attacks = BLACK_PAWN_ATTACKS[curr_square] & WHITE_PIECES
                if 56 <= curr_square <= 63:
                    while attacks:
                        to_square = least_significant_bit_count(attacks)
                        attacks ^= (one << to_square)
                        moves.add_move(curr_square, to_square, 6, 1, 0, 0, 0)
                        moves.add_move(curr_square, to_square, 6, 1, 1, 0, 0)
                        moves.add_move(curr_square, to_square, 6, 1, 2, 0, 0)
                        moves.add_move(curr_square, to_square, 6, 1, 3, 0, 0)
                    if (one << (curr_square + 8)) & (~ALL_PIECES):
                        moves.add_move(curr_square, curr_square + 8, 6, 1, 0, 0, 0)
                        moves.add_move(curr_square, curr_square + 8, 6, 1, 1, 0, 0)
                        moves.add_move(curr_square, curr_square + 8, 6, 1, 2, 0, 0)
                        moves.add_move(curr_square, curr_square + 8, 6, 1, 3, 0, 0)
                else:
                    while attacks:
                        to_square = least_significant_bit_count(attacks)
                        attacks ^= (one << to_square)
                        moves.add_move(curr_square, to_square, 6, 0, 0, 0, 0)
                    if (one << (curr_square + 8)) & (~ALL_PIECES):
                        if 8 <= curr_square <= 15 and (one << 
                        (curr_square + 16)) & (~ALL_PIECES):
                            moves.add_move(curr_square, curr_square + 8, 6, 0, 0, 
                            0, 0)
                            moves.add_move(curr_square, curr_square + 16, 6, 0, 0, 
                            0, 0)
                        else:
                            moves.add_move(curr_square, curr_square + 8, 6, 0, 0, 
                            0, 0)
                    if (self.board_data & (1 << 5)) and (((self.board_data >> 
                    (6)) & ((1 << 6) - 1)) == (curr_square + 9) or ((
                        (self.board_data >> (6)) & (
                            (1 << 6) - 1)) == curr_square + 7)):
                        moves.add_move(curr_square, (((self.board_data >> (6)) & 
                        ((1 << 6) - 1))), 6, 0, 0, 1, 0)
            while BLACK_KNIGHTS:
                curr_square = least_significant_bit_count(BLACK_KNIGHTS)
                BLACK_KNIGHTS ^= (one << curr_square)
                attacks = KNIGHT_ATTACKS[curr_square] & (~BLACK_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 7, 0, 0, 0, 0)
            while BLACK_BISHOPS:
                curr_square = least_significant_bit_count(BLACK_BISHOPS)
                BLACK_BISHOPS ^= (one << curr_square)
                attacks = BISHOP_ATTACKS[curr_square][((BISHOP_OCCUPANCY[
                    curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[
                        curr_square]) >> (64 - BISHOP_OCCUPANCY_BITS[
                            curr_square])] & (~BLACK_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 8, 0, 0, 0, 0)
            while BLACK_ROOKS:
                curr_square = least_significant_bit_count(BLACK_ROOKS)
                BLACK_ROOKS ^= (one << curr_square)
                attacks = ROOK_ATTACKS[curr_square][((ROOK_OCCUPANCY[
                    curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[
                        curr_square]) >> (64 - ROOK_OCCUPANCY_BITS[
                            curr_square])] & (~BLACK_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 9, 0, 0, 0, 0)
            while BLACK_QUEEN:
                curr_square = least_significant_bit_count(BLACK_QUEEN)
                BLACK_QUEEN^= (one << curr_square)
                attacks = BISHOP_ATTACKS[curr_square][((BISHOP_OCCUPANCY[
                    curr_square] & ALL_PIECES) * BISHOP_MAGIC_NUMBERS[
                        curr_square]) >> (64 - BISHOP_OCCUPANCY_BITS[
                            curr_square])] & (~BLACK_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 10, 0, 0, 0, 0)
                attacks = ROOK_ATTACKS[curr_square][((ROOK_OCCUPANCY[
                    curr_square] & ALL_PIECES) * ROOK_MAGIC_NUMBERS[
                        curr_square]) >> (64 - ROOK_OCCUPANCY_BITS[
                            curr_square])] & (~BLACK_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 10, 0, 0, 0, 0)
            while BLACK_KING:
                curr_square = least_significant_bit_count(BLACK_KING)
                BLACK_KING ^= (one << curr_square)
                attacks = KING_ATTACKS[curr_square] & (~BLACK_PIECES)
                while attacks:
                    to_square = least_significant_bit_count(attacks)
                    attacks ^= (one << to_square)
                    moves.add_move(curr_square, to_square, 11, 0, 0, 0, 0)
                if self.board_data & (8) and not (ALL_PIECES & ((one << 5) | 
                (one << 6))) and not self.is_square_attacked(0, 3, BLACK_PIECES, 
                WHITE_PIECES) and not self.is_square_attacked(0, 4, BLACK_PIECES, 
                WHITE_PIECES):
                    moves.add_move(curr_square, 6, 11, 0, 0, 0, 1)
                if self.board_data & (16) and not (ALL_PIECES & ((one << 1) | 
                (one << 2) | (one << 3))) and not self.is_square_attacked(0, 
                4, BLACK_PIECES, WHITE_PIECES) and not self.is_square_attacked(0, 
                5, BLACK_PIECES, WHITE_PIECES):
                    moves.add_move(curr_square, 2, 11, 0, 0, 0, 1)
        return moves

    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef bint make_move(self, U32 move):        
        cdef U8 piece = (move >> 12) & (15)
        cdef U8 source = move & (63)
        cdef U8 target = (move >> (6)) & (63)
        cdef U64 mask
        cdef U8 i
        if ((self.board_data << (12)) & (63)) == 100:
            return False
        if 0 <= piece <= 5:
            if (move >> (16)) & (1):
                self.bitboards[0] ^= (one << source)
                self.bitboards[((move >> (17)) & (3)) + 1] |= (one << target)
                self.board_data &= (4095)
            elif (move >> (19)) & (1):
                self.bitboards[0] ^= ((one << source) | (one << target))
                self.bitboards[6] ^= (one << (target + 8))
                self.board_data &= (4095)
            elif (move >> (20)) & (1):
                self.bitboards[5] ^= ((one << source) | (one << target))
                self.bitboards[3] ^= (one << ((source + target) // 2))
                if target == 62:
                    self.bitboards[3] ^= (one << 63)
                else:
                    self.bitboards[3] ^= (one << 56)
                self.board_data += (4096)
            else:
                self.bitboards[piece] ^= ((one << source) | (one << target))
                mask = 0
                for i in range(6):
                    mask |= self.bitboards[6 + i]
                    self.bitboards[i + 6] &= ~(one << target)
                if mask & (one << target):
                    self.board_data &= (4095)
                else:
                    self.board_data += (4096)
            self.board_data |= (1)
            if piece == 0 and source - target == 16:
                self.board_data &= ~(((1 << 6) - 1) << 6)
                self.board_data |= ((target + 8) << 6)
            if piece == 5:
                self.board_data &= ~(6)
            if self.board_data & (2) and piece == 3 and source == 63:
                self.board_data &= ~(2)
            elif self.board_data & (4) and piece == 3 and source == 56:
                self.board_data &= ~(4)
            if self.is_square_attacked(1, least_significant_bit_count(
                self.bitboards[5]), (self.bitboards[6] | self.bitboards[7] | 
                self.bitboards[8] | self.bitboards[9] | self.bitboards[10] | 
                self.bitboards[11]), (self.bitboards[0] | self.bitboards[1] | 
                self.bitboards[2] | self.bitboards[3] | self.bitboards[4] | 
                self.bitboards[5])):
                return False
        else:
            if (move >> (16)) & (1):
                self.bitboards[6] ^= (one << source)
                self.bitboards[((move >> (17)) & (3)) + 7] |= (one << target)
                self.board_data &= (4095)
            elif (move >> (19)) & (1):
                self.bitboards[6] ^= ((one << source) | (one << target))
                self.bitboards[0] ^= (one << (target + 8))
                self.board_data &= (4095)
            elif (move >> (20)) & (1):
                self.bitboards[11] ^= ((one << source) | (one << target))
                self.bitboards[9] ^= (one << ((source + target) // 2))
                if target == 2:
                    self.bitboards[9] ^= (one << 1)
                else:
                    self.bitboards[9] ^= (one << 7)
            else:
                self.bitboards[piece] ^= ((one << source) | (one << target))
                mask = 0
                for i in range(6):
                    mask |= self.bitboards[i]
                    self.bitboards[i] &= ~(one << target)
                if mask & (one << target):
                    self.board_data &= (4095)
                else:
                    self.board_data += (4096)
            self.board_data ^= (1)
            if piece == 6 and target - source == 16:
                self.board_data &= ~(((1 << 6) - 1) << 6)
                self.board_data |= ((target - 8) << 6)
            if piece == 11:
                self.board_data &= ~(24)
            if self.board_data & (8) and piece == 9 and source == 7:
                self.board_data &= ~(8)
            elif self.board_data & (16) and piece == 9 and source == 0:
                self.board_data &= ~(16)
            if self.is_square_attacked(0, least_significant_bit_count(
                self.bitboards[11]), (self.bitboards[6] | self.bitboards[7] | 
                self.bitboards[8] | self.bitboards[9] | self.bitboards[10] | 
                self.bitboards[11]), (self.bitboards[0] | self.bitboards[1] | 
                self.bitboards[2] | self.bitboards[3] | self.bitboards[4] | 
                self.bitboards[5])):
                return False
        return True

    cpdef bint MakeMove(self, U32 move):
        return self.make_move(move)

    def ReturnMoves(self):
        cdef Moves moves = self.return_moves()
        MovesToReturn = []
        cdef U64[12] bitboard_copy
        cdef U32 board_data_copy
        for i in range(moves.count):
            temp = self.copy()
            bitboard_copy = temp[0]
            board_data_copy = temp[1]
            if not self.make_move(moves.move_list[i]):
                self.bitboards, self.board_data = bitboard_copy, board_data_copy
            else:
                self.bitboards, self.board_data = bitboard_copy, board_data_copy
                MovesToReturn += [moves.move_list[i]]
        return MovesToReturn
    
    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef copy(self):
        return (self.bitboards, self.board_data)
    
    @cython.binding(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    @cython.initializedcheck(False)
    @cython.cdivision(True)
    cdef int evaluate(self):
        score = 0
        for i in range(64):
            score += (count_bits(self.bitboards[0]) * 10 + 
            count_bits(self.bitboards[1]) * 30 + 
            count_bits(self.bitboards[2]) * 30 + 
            count_bits(self.bitboards[3]) * 50 + 
            count_bits(self.bitboards[4]) * 90 - 
            (count_bits(self.bitboards[6]) * 10 + 
            count_bits(self.bitboards[7]) * 30 + 
            count_bits(self.bitboards[8]) * 30 + 
            count_bits(self.bitboards[9]) * 50  + 
            count_bits(self.bitboards[10]) * 90))
            score += (((self.bitboards[0] >> i) & one) * Pawns[i] + 
            ((self.bitboards[1] >> i) & one) * Knights[i] + 
            ((self.bitboards[2] >> i) & one) * Bishops[i] + 
            ((self.bitboards[3] >> i) & one) * Rooks[i] + 
            ((self.bitboards[4] >> i) & one) * Queens[i] + 
            ((self.bitboards[0] >> i) & one) * King[i])
            i = 64 - ((i // 8 + 1) * 8) + i % 8
            score -= (((self.bitboards[6] >> i) & one) * Pawns[i] + 
            ((self.bitboards[7] >> i) & one) * Knights[i] + 
            ((self.bitboards[8] >> i) & one) * Bishops[i] + 
            ((self.bitboards[9] >> i) & one) * Rooks[i] + 
            ((self.bitboards[10] >> i) & one) * Queens[i] + 
            ((self.bitboards[11] >> i) & one) * King[i])
        return score


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef U64 perft_internal(U8 depth, Board board):
    cdef Moves moves = board.return_moves()
    cdef U32[218] move_list = moves.return_move_list() 
    cdef U8 i
    cdef Board copy_board
    cdef U64 total_nodes = 0
    if depth == 0:
        return 1
    else:
        for i in range(moves.return_count()):
            copy_board = Board(*board.copy())
            if copy_board.make_move(move_list[i]) == False:
                continue
            total_nodes += perft_internal(depth - 1, copy_board)
    return total_nodes


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
cdef void perft_(U8 depth):
    cdef Board board = Board(BITBOARDS, BOARD_DATA)
    board.print_chess_board()
    cdef Moves moves = board.return_moves()
    cdef U32[218] move_list = moves.return_move_list() 
    cdef U8 i
    cdef Board copy_board
    cdef U64 nodes
    cdef U64 total_nodes = 0
    if depth == 0:
        print("Invalid depth")
    else:
        for i in range(moves.return_count()):
            copy_board = Board(BITBOARDS, BOARD_DATA)
            if copy_board.make_move(move_list[i]) == False:
                continue
            print(f"From: {square_string[move_list[i] & 63]}"
            f" To: {square_string[(move_list[i] >> 6) & 63]} ", end = '')
            nodes = perft_internal(depth - 1, copy_board)
            print(nodes)
            total_nodes += nodes
        print(f"Total Nodes: {total_nodes}")


def perft():
    import time
    depth = int(input("Enter depth: "))
    stime = time.time()
    perft_(depth)
    print(f'Time: {time.time() - stime}')


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
@cython.binding(False)
cdef int minimax_int(Board board, U8 depth, bint maximizing, int alpha, int beta):
    cdef Moves moves = board.return_moves()
    cdef U32 data = board.board_data
    cdef U64[12] bitboards = board.bitboards
    cdef int maxEval = -2147483648
    cdef int minEval = 2147483647
    if depth == 0:
        return board.evaluate()
    if maximizing:
        once = False
        for i in range(moves.count):
            if board.make_move(moves.move_list[i]):
                once = True
                val = minimax_int(board, depth - 1, False, alpha, beta)
                maxEval = max(val, maxEval)
                alpha = max(alpha, val)
                board.board_data = data
                board.bitboards = bitboards
                if beta <= alpha:
                    break
            else:
                board.board_data = data
                board.bitboards = bitboards
        if not once and board.check_for_check(0):
            return -2147483648
        return maxEval
    else:
        once = False
        for i in range(moves.count):
            if board.make_move(moves.move_list[i]):
                once = True
                val = minimax_int(board, depth - 1, True, alpha, beta)
                minEval = min(val, minEval)
                beta = min(beta, val)
                board.board_data = data
                board.bitboards = bitboards
                if beta <= alpha:
                    break
            else:
                board.board_data = data
                board.bitboards = bitboards
        if not once and board.check_for_check(1):
            return 2147483647
        return minEval


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.initializedcheck(False)
@cython.cdivision(True)
@cython.binding(False)
cdef U32 minimax(Board board, U8 depth, bint maximizing, int alpha, int beta):
    cdef Moves moves = board.return_moves()
    cdef Board copy_board
    cdef int maxEval = -2147483648
    cdef int minEval = 2147483647
    cdef U32 data = board.board_data
    cdef U64[12] bitboards = board.bitboards
    cdef U32 move
    if depth == 0:
        return board.evaluate()
    if maximizing:
        once = False
        for i in range(moves.count):
            if board.make_move(moves.move_list[i]):
                once = True
                val = minimax_int(board, depth - 1, False, alpha, beta)
                if val > maxEval:
                    maxEval = val
                    move = moves.move_list[i]
                alpha = max(alpha, val)
                board.board_data = data
                board.bitboards = bitboards
                if beta <= alpha:
                    break
            else:
                board.board_data = data
                board.bitboards = bitboards
        if not once and board.check_for_check(0):
            return 0
        return move
    else:
        once = False
        for i in range(moves.count):
            if board.make_move(moves.move_list[i]):
                once = True
                val = minimax_int(board, depth - 1, True, alpha, beta)
                if val < minEval:
                    minEval = val
                    move = moves.move_list[i]
                minEval = min(val, minEval)
                beta = min(beta, val)
                board.board_data = data
                board.bitboards = bitboards
                if beta <= alpha:
                    break
            else:
                board.board_data = data
                board.bitboards = bitboards
        if not once and board.check_for_check(1):
            return 0
        return move
        

def BestMove(board, depth):
    if board.board_data & (1):
        return minimax(board, depth, False, -2147483648, 2147483647)
    else:
        return minimax(board, depth, True, -2147483648, 2147483647)