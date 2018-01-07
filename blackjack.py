# coding:utf-8

import random

RANK, SUIT = 0,1

def win_lose(dealer_hand,player_hand,bet,player_money):
    player_point = get_point(player_hand)
    dealer_point = get_point(dealer_hand)
    if player_point <= 21:
        if (player_point > dealer_point) or (dealer_point > 21) :
          if player_point == 21:
              return ('<<player win>>', player_money + int(bet*2.5))
          else:
              return ('<<player win>>', player_money + bet*2)
        elif player_point == dealer_point :
            return ('<<push>>', player_money + bet)
        else :
            return ('<<player lose>>', player_money)
    else:
        return ('<<player lose>>', player_money)




def player_op(deck,player_hand,op) :
    doubled, ending = False, False
    if op == '1':
        print('[player: stand]')
        doubled, ending = False, True
    elif op == '2':
        print('[player: hit]')
        player_hand.append(deck.pop())
        print_player_hand(player_hand)
        doubled, ending = False, False
    elif op == '3':
         if len(player_hand) == 2 : #手札は2枚かどうか
             print('[player: double]')
             player_hand.append(deck.pop())
             print_player_hand(player_hand)
             doubled, ending = True, True
         else:
             print('(ダブルはできません)')


    if get_point(player_hand) > 21:
        print('[プレイヤーはバストした！]')
        ending = True
    elif get_point(player_hand) == 21:
        print('21です！')
        ending = True

    return doubled,ending

def dealer_op(deck,player_hand,dealer_hand) :
    while get_point(player_hand) <= 21:
          if get_point(dealer_hand) >= 17 :
              print('[dealer : stand]')
              break
          else:
              print('[dealer: hit]')
              dealer_hand.append(deck.pop())
          print_dealer_hand(dealer_hand,False)


def get_point(hand):
    result = 0
    ace_flag = False
    for card in hand :
      if card[RANK] == 1:  #カードがAか？
          ace_flag = True
      if card[RANK] > 10:
        num = 10
      else :
        num = card[RANK]
      result = result + num
    if ace_flag and result <= 11:
        result += 10
    return result

# print_player_hand 関数

def print_player_hand(player_hand):
    print('player（', get_point(player_hand),'):  ')
    for card in player_hand:
        print('[', card[SUIT], card[RANK],']')
    print()

#print_dealer 関数

def print_dealer_hand(dealer_hand,uncovered):
     if uncovered:
         print('dealer(', get_point(dealer_hand),'):   ')
     else:
         print('dealer (??):  ')
     flag = True
     for card in dealer_hand:
         if flag or uncovered:
              print('[', card[SUIT],card[RANK], ']')
              flag = False
         else:
              print('[ * * ]')
     print()

def make_deck():
    suits  =  ['S','H','D','C'] #スートの定義
    ranks = range(1,14)  #ランクの定義
    deck = [(x,y) for x in ranks for y in suits]
    random.shuffle(deck)  #シャッフルする
    return deck




def main():
    turn = 1
    player_money = 100
    deck = make_deck() # これで山札が足りなくならないので、こkに移動
    while(player_money > 0):
        

        #ターンの始めにターン数と所持金の情報を表示
        print('-'*20)
        print('turn:',turn)
        print('money:',player_money)
        print('-'*20)
        player_hand = [] #プレイヤーの手札を格納するリスト
        dealer_hand = [] #ディーラーの手札を格納するリスト
        
        try:
            bet = int(input('bet > '))
        except:
            print('整数で入力してください')
            continue

        # 入力値が所持金を超えていたらやり直し
        if bet > player_money:
            print('所持金が不足しています')
            continue
        #入力値が0より小さかったらやり直し
        elif bet <= 0:
             print('ベットできる額は1以上です。')
             continue
        player_money -= bet
        
        #デッキの残りが10枚以下ならデッキを再構築&シャッフル
        if len(deck) < 10 :
             deck = make_deck()

        # print(deck)
        for i in range(2): #お互いに2枚ずつ引く
            player_hand.append(deck.pop()) #デッキからプレイヤーの手札へ
            dealer_hand.append(deck.pop()) #デッキからディーラーの手札へ
        

        #手札の情報を表示
        print('-'*20)
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand,False) #本来はTrueであるがここではFalseにしておく
        print('-'*20)
        #player turn
        while True:
          op = input('stand : 1, hit : 2, double : 3 > ')
          doubled,ending = player_op(deck,player_hand,op)
          if doubled :
              player_money -= bet
              bet += bet
          if ending :
              break

        #dealer turn
        dealer_op(deck,player_hand,dealer_hand)

        print('-'*20)#手札の情報を表示
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand,True) #ゲーム終了時は、ディーラーの手札全て表示
        print('-'*20)

        message, player_money = win_lose(dealer_hand,player_hand,bet,player_money)
        print(message)

        turn += 1
        input("next turn")
    print('game over')

if __name__ == '__main__':
    main()
