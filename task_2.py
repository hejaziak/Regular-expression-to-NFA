import argparse

def inserting_dots(expr):
    symbols = ['*','+','+']
    res = ''
    for i in range(0, len(expr)-1):
        if((expr[i].isdigit() or expr[i].isalpha() or expr[i] ==' ') and (expr[i+1].isdigit() or expr[i+1].isalpha() or expr[i+1] == ' ' )):
            res += expr[i] + '.'
        elif (expr[i] == ')' and expr[i+1] == '('):
            res += expr[i] + '.'
        elif (expr[i] == ')' and (expr[i+1].isdigit() or expr[i+1].isalpha() or expr[i+1] == ' ' )):
          res += expr[i] + '.'
        elif ((expr[i].isdigit() or expr[i].isalpha() or expr[i] ==' ') and (expr[i+1] == '(' ) ):
          res += expr[i] + '.'
        elif ((expr[i] in symbols) and (expr[i+1] == '(') ):
          res += expr[i] + '.'
        elif ((expr[i] in symbols) and (expr[i+1].isdigit() or expr[i+1].isalpha() or expr[i+1] == ' ' )):
          res += expr[i] + '.'
        else:
          res += expr[i]

    if( expr[len(expr)-1] != res[len(res)-1]):
      res += expr[len(expr)-1]

    return res

class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.isEmpty():
            return None
        return self.items.pop()

    def peek(self):
        if len(self.items)-1 < 0:
            return None
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
    
    def isEmpty(self):
        return len(self.items) == 0

def infixToPostfix(infixexpr):
    prec = {}
    prec["^"] = 7
    prec["+"] = 6
    prec["*"] = 5
    prec["?"] = 4
    prec["|"] = 3
    prec["."] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = list(infixexpr)
    for token in tokenList:
        if token.isalnum() or token ==' ':
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)


class NFA:
  def __init__(self):
    self.startState = 0
    self.acceptStates = []
    self.states = []
    self.alphabets = []
    self.transitions = []

  def add_states(self,states):
    for state in states:
      self.states.append(state)

  def add_alphabet(self,alphabets):
    for alphabet in alphabets:
      self.alphabets.append( alphabet)
  
  def states_name_adjust(self,offset):
    nfa = NFA()

    nfa.startState = self.startState + offset
    
    for state in self.acceptStates:
      nfa.acceptStates.append(state + offset)
    
    for state in self.states:
      nfa.states.append(state + offset)
    
    nfa.alphabets = self.alphabets

    for transition in self.transitions:
      frm, to, char = transition
      nfa.transitions.append((frm + offset, state + offset, char))

    return nfa
    

  def char_operation(self, char):
    nfa = NFA()
    nfa.startState = 0
    nfa.states.extend([0,1])
    nfa.alphabets.append(char)
    nfa.acceptStates.append(1)
    nfa.transitions.append((0,1,char))
    return nfa
  
  def Union(self,lst1, lst2): 
    final_list = list(set(lst1) | set(lst2)) 
    return final_list 

  def concat_operation(self,b):
    nfa = NFA()
    b = b.states_name_adjust(len(self.states))

    nfa.startState = self.startState
    nfa.states = nfa.Union(self.states,b.states)
    nfa.alphabets = nfa.Union(self.alphabets,b.alphabets)
    nfa.acceptStates = b.acceptStates
    
    nfa.transitions.extend(self.transitions)
    nfa.transitions.extend(b.transitions)
    for state in self.acceptStates:
      nfa.transitions.append((state,b.startState,' '))

    return nfa

  def union_operation(self,b):
    nfa = NFA()

    self = self.states_name_adjust(1)
    b = b.states_name_adjust(len(self.states))

    nfa.startState = 0

    nfa.states = nfa.Union(self.states,b.states)
    nfa.states.append(0)
    nfa.states.append(len(self.states) + len(b.states) + 1)

    nfa.alphabets = nfa.Union(self.alphabets,b.alphabets)
    if not ' ' in nfa.alphabets:
      nfa.alphabets.append(' ')

    nfa.acceptStates.append(len(self.states) + len(b.states) + 1)

    nfa.transitions.extend(self.transitions)
    nfa.transitions.extend(b.transitions)
    nfa.transitions.append((0,self.startState,' '))
    nfa.transitions.append((0,b.startState,' '))

    for state in self.acceptStates:
      nfa.transitions.append((state,len(self.states) + len(b.states) + 1,' '))

    for state in b.acceptStates:
      nfa.transitions.append((state,len(self.states) + len(b.states) + 1,' '))

    return nfa

  def kleene_operation(self):
    nfa = NFA()

    self = self.states_name_adjust(1)

    print(self.states)

    nfa.startState = 0

    nfa.states.append(0)
    nfa.states.extend(self.states)
    nfa.states.append(len(nfa.states))


    nfa.alphabets = self.alphabets
    if not ' ' in nfa.alphabets:
      nfa.alphabets.append(' ')

    nfa.acceptStates.append(len(nfa.states)-1)
    
    nfa.transitions.extend(self.transitions)
    nfa.transitions.append((0,self.startState,' '))
    nfa.transitions.append((0,len(self.states) + 1,' '))

    for state in self.acceptStates:
      nfa.transitions.append((state,self.startState,' '))
      nfa.transitions.append((state,len(self.states) + 1,' '))

    return nfa

  def plus_operation(self):
    return self.concat_operation(self.kleene_operation())

  def unary_operation(self):
    nfa = NFA()
    nfa = nfa.char_operation(' ')
    return self.union_operation(nfa)

  def print_NFA(self):
    print(self.states)
    print(self.alphabets)
    print(self.startState)
    print(self.acceptStates)
    print(self.transitions)
    print('\n')


def convert(expr):
  stack = Stack()
  expr = list(expr)

  symbols = ['*','+','?','|','.']

  for char in expr:
    if (not char in symbols):
      nfa = NFA()
      stack.push(nfa.char_operation(char))
    else:
      if(char == '|'):
        a,b = stack.pop(),stack.pop()
        stack.push(a.union_operation(b))
      elif (char == '*'):
        a = stack.pop()
        stack.push(a.kleene_operation())
      elif (char == '+'):
        a = stack.pop()
        stack.push(a.plus_operation())
      elif (char == '.'):
        a,b = stack.pop(), stack.pop()
        stack.push(a.concat_operation(b))
      else:
        a = stack.pop()
        stack.push(a.unary_operation())

  
  if(stack.size()==1):
    return stack.pop()
  else:
    return NFA()
        
  
nfa1 = NFA()
nfa1 = nfa1.char_operation('s')

nfa2 = NFA()
nfa2 = nfa1.char_operation('t')

nfa1.kleene_operation().print_NFA()

# print(infixToPostfix(inserting_dots('(s|ct)*')) )


convert(infixToPostfix(inserting_dots('(s| t)*'))).print_NFA()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    # parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
    #                     metavar="file")
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?", metavar="file")

    args = parser.parse_args()
    with open(args.file, 'r') as file:
      for line in file:
        nfa = convert(infixToPostfix(inserting_dots('(s| t)*')))
        with open('task_2_result.txt', 'w') as fr:
            fr.write(','.join(str(e) for e in nfa.states)+'\n')
            fr.write(','.join(str(e) for e in nfa.alphabets)+'\n')
            fr.write(str(nfa.startState)+'\n')
            fr.write(','.join(str(e) for e in nfa.acceptStates)+'\n')
            fr.write(','.join(str(e) for e in nfa.transitions)+'\n')

