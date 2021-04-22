input_lst = ['i love babitaji', 'babitaji is beautiful', 'hi', 'hello there', 'do you like BabitaJi?', 'i love old episodes',
'why new episodes are bad','new episode sucks', 'chup ho ja saatvi fail', 'you are shit', 'you are stupid',
'what do you do?', 'how much you earn?', 'mehta saheb helpful','bye','see you later', 'i have exams',
'i hate exams', 'i like Chai', 'chai piyoge?', 'i love tea', 'i work hard to get babitaji trust',
'Thanks','whats your name?', 'your name?','my name is kanishk','you are nice','you are funny','you are good','what you have gada electronics right?',
'you are good bot','how about Iyer?']

output = ['12','12','1','1','9','13','11','11','7','7','7','8','8','2','2','14','14','6','6','6','12','3','4','4','4',
'15','15','15','9','3','15','16']
if len(input_lst)!=len(output):
  print('Input doesnt match with output length!!')
from bot import *
count = test(input_lst,output)

print("="*35)
print("Final score : ",count, "/",len(output))
print("="*35)
