import math
import random
import sys
#手はg,c,pのどれかを出す
#n回じゃんけんを行い、勝率を出力する

enemy_hand_list = ['g','c','p']
n=int(sys.argv[1])

#左から勝ち,負け,あいこの回数
battle_count = [0,0,0]

for i in range(n):
  while 1:
    player_hand = input("じゃんけんポン！(g,c,p):")
    enemy_hand = random.choice(enemy_hand_list)
    if enemy_hand == player_hand:
      print("あいこ")
      battle_count[2] += 1
      continue
    elif (player_hand == "c" and enemy_hand == "g") or (player_hand == "g" and enemy_hand == "p") or (player_hand == "p" and enemy_hand == "c"):
      print("負け")
      battle_count[1] += 1
      break
    elif (player_hand == "g" and enemy_hand == "c") or (player_hand == "p" and enemy_hand == "g") or (player_hand == "c" and enemy_hand == "p"):
      print("勝ち")
      battle_count[0] += 1
      break
    else:
      print("入力が不正です。g,c,pのどれかを入力してください")
      continue

print("勝ち:",battle_count[0],"負け:",battle_count[1],"あいこ:",battle_count[2])