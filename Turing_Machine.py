import numpy as np
from functools import reduce



states=[]
start_state=[]
final_states=[]
actions=[]
actions_unary=[]
Hault = 0
flag=0


state_unary = dict(q0 = '1', q1 = '11', q2 = '111', q3 = '1111', q4 = '11111', q5 = '111111', q6 = '1111111', q7 = '11111111', q8 = '111111111', q9 = '1111111111', q10 = '11111111111', q11 = '111111111111', q12 = '1111111111111')
gamma_unary = dict(x = '11', B ='111',c='1111',y='11111')
act_unary = dict(R = '1', L = '11')


with open("mulTM.txt") as file:
    for line in file:
        if line.strip().startswith("states"):
            states_line= line.split(":")[1].strip()
            states = states_line[1:-1].split(",")
        elif line.strip().startswith("start_state"):
            start_state_line = line.split(":")[1].strip()
            start_state = start_state_line[1:-1].split(",")
        elif line.strip().startswith("final_states"):
            final_states_line= line.split(":")[1].strip()
            final_states = final_states_line[1:-1].split(",")
        elif line.strip().startswith("actions"):
            actions_line = line.split(":")[1].strip()
            actions_list = actions_line[1:-1].split("),(")
            for action in actions_list:
                action_elements = action.strip("()").split(",")
                actions.append(action_elements)

print("\nstates:",states,"\n")
print("\nstart state:",start_state,"\n")
print("\nfinal state:",final_states,"\n")
print("\nactions:",actions,"\n")

for i in range(len(actions)):
    actions_unary.append(state_unary[actions[i][0]])
    actions_unary.append('0')
    if actions[i][1]=='1':
        actions_unary.append('1')
    else:
        actions_unary.append(gamma_unary[actions[i][1]])
    actions_unary.append('0')
    
    if actions[i][2]=='1':
        actions_unary.append('1')
    else:
        actions_unary.append(gamma_unary[actions[i][2]])
    actions_unary.append('0')
    
    actions_unary.append(act_unary[actions[i][3]])
    actions_unary.append('0')
    
    actions_unary.append(state_unary[actions[i][4]])
    actions_unary.append('0')


TM_act = ''.join([str(elem) for i,elem in enumerate(actions_unary)])
print("\nactions converted to unary:",TM_act,"\n")

current_state=state_unary[start_state[0]]
input_tape=input("Enter input: ")
input_tape='BBBBBBBBBB'+input_tape+'BBBBBBBBBB'
pos_act = 0
pos_inp = 10
print(input_tape)
while True:
    cur_st = TM_act.split('0')[pos_act]
    inp = TM_act.split('0')[pos_act+1]
    out = TM_act.split('0')[pos_act+2]
    mv = TM_act.split('0')[pos_act+3]
    nxt_st = TM_act.split('0')[pos_act+4]
    pos_act+=5
    if(current_state==cur_st):
        
        if(input_tape[pos_inp]=='1'):
            if(inp=='1'):
                flag=1
        elif(gamma_unary[input_tape[pos_inp]]==inp):
            flag=1
        if(flag==1):
            current_state=nxt_st
            if (out=='1'):
                input_tape = input_tape[:pos_inp] + '1' + input_tape[pos_inp + 1:]
            elif(out=='11'):
                input_tape = input_tape[:pos_inp] + 'x' + input_tape[pos_inp + 1:]
            elif(out=='111'):
                input_tape = input_tape[:pos_inp] + 'B' + input_tape[pos_inp + 1:]
            elif(out=='1111'):
                input_tape = input_tape[:pos_inp] + 'c' + input_tape[pos_inp + 1:]
            elif(out=='11111'):
                input_tape = input_tape[:pos_inp] + 'y' + input_tape[pos_inp + 1:]
            if(mv=='1'):
                pos_inp+=1
            else:
                pos_inp-=1
            pos_act=0
            
            print(input_tape)
    flag=0
    
    if(TM_act.split('0')[pos_act]==''):
        break
    
if(current_state in state_unary[final_states[0]]):
    print("INPUT ACCEPTED")
    print("Output is",input_tape)
else:
    print("INPUT REJECTED")