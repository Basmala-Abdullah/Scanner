import re
from tkinter import*
from PIL import ImageTk, Image


root = Tk()
root.title("Scanner")
root['background']='#0e141b'
e = Text(root, width=20, height=6)
e.grid(row = 0, column = 0)



list_of_classes= []



Keywords = {'repeat':'repeat keyword', 'until': 'until keyword'}
Keywords_key = Keywords.keys()

AssignOperators = {':=': 'Assignment op'}
AssignOperators_key = AssignOperators.keys()

operators = {'<': 'Lessthan op', '>': 'Greaterthan op', '>=': 'GreaterthanORequal op', '<=': 'SmallerthanORequal op', '=' : 'isEqual op'}
operators_key = operators.keys()

punctuation_symbol = {':': 'colon', ';': 'semi-colon', '.': 'dot', ',': 'comma'}
punctuation_symbol_key = punctuation_symbol.keys()

def TokenList():
    win2=Toplevel()
    win2.title('Tokens DFA')
    win2.geometry("200x400")
    win2['background'] = '#0e141b'
    a1 = e.get(1.0,END);
    count = 0
    p = a1.split("\n")
    for line in p:
        tokens = line.split(' ')
        if tokens == ['']:
            return
        print("Tokens are ", tokens)
        # __________###DFA###___________#
        for token in tokens:
            count = count +1
            if token in AssignOperators_key:
                print(token, "operator is ", AssignOperators[token])
                myLabel1 = Label(win2, text="<" + token + " , " + AssignOperators[token] + ">")
                myLabel1.grid(row=count, column=8)
                list_of_classes.append('Assignment operator')
            elif token in operators_key:
                print(token, "operator is ", operators[token])
                myLabel1 = Label(win2, text="<"+token+ " , "+operators[token]+">")
                myLabel1.grid(row=count, column=8)
                list_of_classes.append('Operator')
            elif token in punctuation_symbol_key:
                print(token, " punctuation symbol is ", punctuation_symbol[token])
                myLabel1 = Label(win2, text="<"+token+ " , "+punctuation_symbol[token]+">")
                myLabel1.grid(row=count, column=8)
                list_of_classes.append('punctuation')
            elif token in Keywords_key:
                print(token, " Keyword is ", Keywords[token])
                myLabel1 = Label(win2, text="<"+token+ " , "+ Keywords[token]+">")
                myLabel1.grid(row=count, column=8)
                list_of_classes.append(token)
            elif (token[0]).isdecimal():
                flag1 = True
                for char in token[1::1]:
                    if not (char.isdecimal()):
                        flag = False
                if flag1 == True:
                    print(token, "number is Number")
                    myLabel1 = Label(win2, text="<" + token + " , Number >")
                    myLabel1.grid(row=count, column=8)
                    list_of_classes.append('Number')
            elif (token[0]).isalpha():
                flag2 = True
                for char in token[1::1]:
                    if not (char.isalpha() or char.isdecimal() or char == '_'):
                        flag2 = False
                if flag2 == True:
                    print(token, "identifier is Identifier")
                    myLabel1 = Label(win2, text="<" + token + " , Identifier >")
                    myLabel1.grid(row=count, column=8)
                    list_of_classes.append('Identifier')
            else:
                print(token, " is an invalid token")
                myLabel1 = Label(win2, text=token + " is invalid")
                myLabel1.grid(row=count, column=8)
                list_of_classes.append('Invalid')
        myLabel1.config(anchor=CENTER)
        print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _")
        print(list_of_classes)



def Submit():
    global small
    win1=Toplevel()
    win1.title('Tokens DFA')
    win1['background'] = '#0e141b'
    small = ImageTk.PhotoImage(Image.open("Images/smalldfa.jpeg"))
    myLabel5 = Label(win1,image=small)
    myLabel5.grid(row=0, column=5)
    bBigDFA = Button(win1, text="Show Classes", command=TokenList())
    bBigDFA.grid(row=0, column=0, columnspan=3)

    a = e.get(1.0, END)
    program = a.split("\n")
    c = 0
    for line in program:
        tokens = line.split(' ')
        if tokens == ['']:
            return
        # __________###TokenDFA###___________#
        for token in tokens:
            c=c+1
            list_of_token_states=['[Start] ']
            if token[0] == '>' or token[0]== '<':
                    list_of_token_states.append('[OP1] ')
                    if (len(token)>=2):
                        if(token[1] == '='):
                            list_of_token_states.append('[OP2] ')
                            for i in range(2,len(token),1):
                                list_of_token_states.append('[Rejected] ')
                        else:
                            for i in range(1,len(token),1):
                                list_of_token_states.append('[Rejected] ')

            elif token[0] == ':' :
                    list_of_token_states.append('[OP3] ')
                    if(token[1] == '='):
                        list_of_token_states.append('[OP2] ')
                        for i in range(2,len(token),1):
                            list_of_token_states.append('[Rejected] ')
                    else:
                        for i in range(1, len(token), 1):
                            list_of_token_states.append('[Rejected] ')

            elif token[0]==';':
                list_of_token_states.append('[EOS] ')
                if (len(token) >= 2):
                        for i in range(1, len(token), 1):
                            list_of_token_states.append('[Rejected] ')

            elif token in Keywords_key:
                if token == 'repeat':
                    list_of_token_states.append('[r] [e] [p] [e] [a] [t]')
                if token == 'until':
                    list_of_token_states.append('[u] [n] [t] [i] [l]')

            elif (token[0]).isdecimal():
                list_of_token_states.append('[NUM] ')
                for char in token[1::1]:
                    if not (char.isdecimal()):
                        list_of_token_states.append('[Rejected] ')
                        break
                    else:
                        list_of_token_states.append('[NUM] ')

            elif (token[0]).isalpha():
                list_of_token_states.append('[ID] ')
                for char in token[1::1]:
                    if not (char.isalpha() or char.isdecimal() or char == '_'):
                        list_of_token_states.append('[Rejected] ')
                        break
                    else:
                        list_of_token_states.append('[ID] ')

            else:
                list_of_token_states.append('[Rejected] ')

            x = ''
            for z in range(0,len(list_of_token_states),1):
                x = x + list_of_token_states[z]

            myLabel6 = Label(win1, text=token + '     ' + x)
            myLabel6.grid(row=c, column=2)

count = 0
count = count+1

def BigDFA():
        co = 0
        flag = True
        global big
        win3 = Toplevel()
        win3.title('Tokens DFA')
        win3['background'] = '#0e141b'
        big = ImageTk.PhotoImage(Image.open("Images/bigdfa1.png"))
        myLabel5 = Label(win3, image=big)
        myLabel5.grid(row=0, column=5)
        list_of_states=[]
        list_of_states.append('[1]')
        co=co+1
        if list_of_classes[0] == 'repeat':
            list_of_states.append("[2]")
            #visualize hay5osh 3ala state 2
            co = co + 1
            for z in range(1,len(list_of_classes),4):
                if list_of_classes[z] == 'Identifier':
                    list_of_states.append("[3]")
                    #state 3 accepted
                    co = co + 1
                    if z+1 < len(list_of_classes):
                        if list_of_classes[z+1]=='Assignment operator':
                            list_of_states.append("[4]")
                            #state 4 accepted
                            co = co + 1
                            if z + 2 < len(list_of_classes):
                                if list_of_classes[z+2] == 'Identifier' or list_of_classes[z+2] == 'Number':
                                    list_of_states.append("[5]")
                                    # state 5 accepted
                                    co = co + 1
                                    if z+3 < len(list_of_classes):
                                        if list_of_classes[z+3] == 'punctuation':
                                            list_of_states.append("[6]")
                                            co = co + 1
                                        else:
                                            for i in range(co - 1, len(list_of_classes), 1):
                                                list_of_states.append("[10]")
                                            flag = False
                                            break
                                    else:
                                        break
                                else:
                                    for i in range(co - 1, len(list_of_classes), 1):
                                        list_of_states.append("[10]")
                                    flag = False
                                    break
                            else:
                                break
                        else:
                            for i in range(co - 1, len(list_of_classes), 1):
                                list_of_states.append("[10]")
                            flag = False
                            break
                    else:
                        break
                elif list_of_classes[z] != 'until':
                    for i in range(co - 1, len(list_of_classes), 1):
                        list_of_states.append("[10]")
                    flag = False
                    break
                else:
                    if co-1 < len(list_of_classes):
                        if list_of_classes[co - 1] == 'until' and co-1 > 4:
                            list_of_states.append("[7]")
                            if co < len(list_of_classes):
                                if list_of_classes[co] == 'Identifier' or list_of_classes[co]== 'Number':
                                    list_of_states.append("[8]")
                                    if co+1 < len(list_of_classes):
                                        if list_of_classes[co+1] == 'Operator' :
                                            list_of_states.append("[9]")
                                            if co + 2 < len(list_of_classes):
                                                if list_of_classes[co + 2] == 'Identifier' or list_of_classes[co + 2] == 'Number':
                                                    list_of_states.append("[11]")
                                                else:
                                                    for i in range(co + 2, len(list_of_classes), 1):
                                                        list_of_states.append("[10]")
                                                    break
                                            else:
                                                break
                                        else:
                                            for i in range(co + 1, len(list_of_classes), 1):
                                                list_of_states.append("[10]")
                                            break
                                    else:
                                        break
                                else:
                                    for i in range(co, len(list_of_classes), 1):
                                        list_of_states.append("[10]")
                                    break
                            else:
                                break
                        else:
                            for i in range(co-1, len(list_of_classes), 1):
                                list_of_states.append("[10]")
                            break
                    else:
                        break
        else:
            flag = False
            for i in range(0, len(list_of_classes), 1):
                 list_of_states.append("[10]")
        myLabel2 = Label(win3, text= list_of_states)
        myLabel2.grid(row=count, column=5)
"""
        if mult%4 is 0:
            if list_of_classes[co-1] == 'until':
                list_of_states.append("[7]")
                if list_of_classes[co+1] == 'Identifier':
                    list_of_states.append("[8]")
                    if list_of_classes[co+2] == 'Operator':
                        list_of_states.append("[9]")
                        if list_of_classes[co+3] == 'Identifier' or list_of_classes[co+3] == 'Number':
                            list_of_states.append("[11]")
                            if len(list_of_classes) >= co+4:
                                for i in range(co+4,len(list_of_classes),1):
                                    list_of_states.append("[10]")
                        else:
                            list_of_states.append("[10]")
                    else:
                        for i in range(co+2, len(list_of_classes), 1):
                            list_of_states.append("[10]")
                else:
                    for i in range(co+1, len(list_of_classes), 1):
                        list_of_states.append("[10]")
            else:
                for i in range(co, len(list_of_classes), 1):
                    list_of_states.append("[10]")
"""


myButton = Button(root, text = "Show Token DFA", command=Submit)
myButton.grid(row = 2, column = 0,columnspan=3)

buttonBigDFA = Button(root, text="Show Sequence DFA", command = BigDFA)
buttonBigDFA.grid(row = 3, column = 0,columnspan=3)



root.mainloop()