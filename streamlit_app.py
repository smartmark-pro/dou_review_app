import streamlit as st
from env.doudizhu import Doudizhu
from env.game import GameEnv, EnvCard2RealCard, RealCard2EnvCard
# from PIL import Image
import numpy as np
# st.set_page_config(layout="wide")

# 参考 https://github.com/kwai/DouZero

deck = []
for i in range(3, 15):
    deck.extend([i for _ in range(4)])
deck.extend([17 for _ in range(4)])
deck.extend([20, 30])


# def create_deck(data):
#         # 创建一副牌
#         suits = ['♠', '♥', '♦', '♣']
#         ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2']
#         if data:
#             deck = []
#         else:
#             deck = [f'{rank}{suit}' for suit in suits for rank in ranks] + ['小王', '大王']
#             random.shuffle(deck)
#         return deck

def generate():
    _deck = deck.copy()
    np.random.shuffle(_deck)
    card_play_data = {'landlord': _deck[:20],
                      'landlord_up': _deck[20:37],
                      'landlord_down': _deck[37:54],
                      'three_landlord_cards': _deck[17:20],
                      }
    for key in card_play_data:
        card_play_data[key].sort()
    return card_play_data

def start_game(game_type):
    if game_type == "随机一把":
        data = generate()

    else:
        if game_type == "图片上传识别":
            uploaded_file = st.file_uploader("选择一张图片", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                # TODO 将图片扔到接口， 返回数据
                data = []
                # # 使用 PIL 打开图片
                # image = Image.open(uploaded_file)
                
                # # 显示上传的图片
                # st.image(image, caption='上传的图片', use_column_width=True)

        else:
            # 花色自动赋值
            data = st.text_area(label="三行数据， 顺序地主, 上家农民 下家农民", value="")
    return data

def main():
    st.title("斗地主复盘")
    st.subheader("玩家可以选择一方， 手动点击， 其余为ai出牌")
    positions = {k:i for i, k in enumerate(["地主", "上家农民", "下家农民"])}
    choose_pos = st.sidebar.selectbox("玩家位置", options=positions.keys())
    game_type = st.sidebar.selectbox("对局生成方式", options=["随机一把", "图片上传识别", "手动输入"])
    
    real_pos = positions.get(choose_pos)
    
        
    is_hidden_cards = st.sidebar.checkbox("是否隐藏对手手牌", value=False)
    ai_given_type = st.sidebar.selectbox("ai出牌控制", options=["自动", "手动"])
    ai_given_time = st.sidebar.slider('ai出牌间隔', 1, 20, 3)
    is_show_card_record= st.sidebar.checkbox("是否展示记牌器", value=False)

    

    
    # 创建游戏实例
    if 'game' not in st.session_state:
        data = start_game(game_type)
        ddz = Doudizhu(data, real_pos)
        st.session_state.game = ddz
        # st.session_state.game.deal()
        st.session_state.current_player = 0
        st.session_state.selected_cards = []
        st.session_state.game_over = False
        st.session_state.step = 1

    game = st.session_state.game
    current_player = st.session_state.current_player

    if st.session_state.game_over:
        st.write("游戏结束！")
        if st.button("重新开始"):
            data = start_game(game_type)
            ddz = Doudizhu(data, real_pos)
            st.session_state.game = ddz
            # st.session_state.game.deal()
            st.session_state.current_player = 0
            st.session_state.selected_cards = []
            st.session_state.game_over = False
            st.session_state.step = 1
        return
    key = 0

    st.subheader(f"轮到{game.roles[st.session_state.current_player]}出牌")

    # 显示每个玩家的手牌
    # p1, p2, p3 = st.columns(3)
    players = []
    def run(position, update=False):
        action_message, action_list = st.session_state.game.env.step(position, update=update)
        action_list = action_list[:3]
        show_action_list = [(str(''.join([EnvCard2RealCard[c] for c in action_info[0]])) if len(
            str(''.join([EnvCard2RealCard[c] for c in action_info[0]]))) > 0 else "Pass",
                             str(round(float(action_info[1]) * 1, 3))) for action_info in action_list]
        print(action_message, show_action_list)
        # st.write("当前得分：" + str(round(float(action_list[0][1]), 3)))
        print(action_message["action"] if action_message["action"] else "pass")
        action_list_str = " | ".join([ainfo[0] + " = " + ainfo[1] for ainfo in show_action_list])
        print(action_list_str)
        st.write(action_list_str)
        return action_message, action_list

    for i in range(3):
        p = st.container(border=True)
        with p:
            st.subheader(game.roles[i])
            infoset = game.get_player_cards(i)
            cards = infoset.player_hand_cards
            if cards:
                player = st.columns(len(cards))
                players.append(player)
                # print("__________________", cards, infoset.player_hand_cards)
                for col, card in zip(player, cards):
                    key += 1
                    # print(card, key)
                    if col.button(EnvCard2RealCard.get(card), key=key):
                        # 选择牌的逻辑
                        if i == current_player:
                            st.session_state.selected_cards.append(card)


    # 显示已选择的牌
    num = len(st.session_state.selected_cards)
    show = st.container(border=True)

    st.write(str(game.env.played_cards))
    with show:
        if num>0:
            st.write(str(st.session_state.selected_cards))
        else:
            st.write(st.write("pass"))

    # 确认出牌按钮
    b1, b4, b2, b3 = st.columns(4)

    with b4:
        if st.button("清空", key="清空"):
            st.session_state.selected_cards.clear() 
            # st.info(f"{game.roles[st.session_state.current_player]} 出牌: {str(st.session_state.selected_cards)}")
    with b2:
        if st.button("AI提示", key="ai"):
            position = st.session_state.game.get_player_cards(current_player)
            action_message, action_list = run(position, update=False)
            st.session_state.action_list = action_list
    with b3:
        if st.button("确认出牌"):
            # cards = list(st.session_state.action_list[0][0])
            
            st.session_state.selected_cards = st.session_state.action_list[0][0] # [RealCard2EnvCard.get(c) for c in cards]
            st.success(f"{game.roles[current_player]}  出牌: {str(st.session_state.selected_cards)}")
            position = st.session_state.game.get_player_cards(current_player)
            from copy import deepcopy
            selected_cards = deepcopy(st.session_state.selected_cards)
            cur_infoset = game.env.get_infoset()

            if selected_cards and selected_cards not in cur_infoset.legal_actions:
                st.error(selected_cards)

            st.session_state.game.env.do_update(position, action=selected_cards)
            st.session_state.selected_cards.clear()  # 清空选择的牌
            
            # 检查游戏是否结束
            print("111",cur_infoset.player_hand_cards)
            if st.session_state.game.env.game_done():  # 当前玩家出完牌
                st.session_state.game_over = True
                st.success(f"{game.roles[st.session_state.current_player]}  胜利！")
                return 
                
                
                
            st.session_state.current_player = (current_player + 1) % 3  # 转到下一个玩家
            st.session_state.step += 1

    
    

    # 添加退出游戏的选项
    if st.button("退出游戏"):
        st.session_state.game_over = True
# TODO
# 游戏状态不对， 其它人的牌应该是未知的
if __name__ == "__main__":
    main()