import random
from env.game import GameEnv
from env.deep_agent import DeepAgent
ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
real_rank =dict({r: i+3 for i, r in enumerate(ranks)}, **{'2': 17,  "X": 20, "D": 30})


class Doudizhu:
    def __init__(self, cards_data, user_position):

        self.card_play_data_list = cards_data
        self.user_position = user_position
        AI = [0, 0]
        AI[0] = self.user_position
        AI[1] = DeepAgent(self.user_position, None)
        self.env = GameEnv(AI)
        self.env.card_play_init(cards_data)

        # self.deck = self.create_deck(data)
        self.players = [[], [], []]  # 三个玩家
        self.roles = ["地主", "下家农民", "上家农民"]
        self.landlord = None
        self.current_player = 0
        self.last_played = None  # 上一轮出牌

    # def card_play_init(self, card_play_data):
    #     self.info_sets['landlord'].player_hand_cards = \
    #         card_play_data['landlord']
    #     self.info_sets['landlord_up'].player_hand_cards = \
    #         card_play_data['landlord_up']
    #     self.info_sets['landlord_down'].player_hand_cards = \
    #         card_play_data['landlord_down']
    #     self.three_landlord_cards = card_play_data['three_landlord_cards']
    #     self.get_acting_player_position()
    #     self.game_infoset = self.get_infoset()

    # def create_deck(self, data):
    #     # 创建一副牌
    #     suits = ['♠', '♥', '♦', '♣']
    #     ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
    #     if data:
    #         deck = []
    #     else:
    #         deck = [f'{rank}{suit}' for suit in suits for rank in ranks] + ['小王', '大王']
    #         random.shuffle(deck)
    #     return deck

    # def deal(self):
    #     # 发牌
    #     for i in range(17):
    #         for player in range(3):
    #             self.players[player].append(self.deck.pop())
            
    #     self.landlord = self.players[0]  # 假设第一个玩家是地主
    #     for i in range(3):
    #         self.players[0].append(self.deck.pop())
    #     for i in range(3):
    #         self.players[i].sort(key=lambda x: -real_rank.get(x[0]))

    def get_player_cards(self, player_index):
        pos_name = {0: "landlord", 1: "landlord_down", 2: "landlord_up"}
        return self.env.info_sets[pos_name.get(player_index)]

    def play_cards(self, player_index, cards):
        if self.validate_play(cards):
            self.players[player_index] = [card for card in self.players[player_index] if card not in cards]
            self.last_played = cards
            self.current_player = (self.current_player + 1) % 3
            return True
        return False

    def validate_play(self, cards):
        # 添加出牌验证逻辑（例如合法性、比大小等）
        return True  # 此处简化，始终返回 True
