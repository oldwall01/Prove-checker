######################################################################
######################################################################

###########################  Tokenizer  ##############################

##"""
##If S is a list of characters, munch(S) is the result of greedily
##trying to form the longest possible token from the start of S, one 
##character at a time. munch(S) destroys its argument.
##Helper functions are canPush , newState, charsToTok, validToken
##"""
######################################################################

	
def whitespace(C):
	if ord(C) in [9,10,11,12,13,32]: return True
	else: return False

def digit(C):
	if ord(C)>=48 and ord(C) <=57: return True
	else: False
	


def paren(C):
	if ord(C) in [40, 41]: return True
	else: return False



def doubleQuota(C):
	if ord(C) == 34: return True
	else: return False


	
	

######################################################################

## newState(state, C), retruns the new 'state' after the token list with 
## 		previous 'state' after adding a new char C

def newState(state, C):
	if state == 'empty':
		if digit(C):	return 'number'
		elif paren(C):	return 'paren'
		elif doubleQuota(C):	return 'hString'
	elif state == 'number' and digit(C): 	return 'number'
	elif state == 'hString' and not doubleQuota(C):	return 'hString'
	elif state == 'hString' and doubleQuota(C): return 'string'
	

## canPush(C, state) means the token char list can list can accept
## 		C into the into list and make the state a valid token state.

def canPush(C, state):
	if state == 'empty': 
		if digit(C): return True
		elif paren(C): return True
		elif doubleQuota(C): return True
		else: return False
	elif state == 'number' and digit(C): return True
	elif state == 'hString': return True
	else: return False

######################################################################

## charsToTok(Charlist): Charlist is a list of chars and charsToTok 
## convert is to a string 
def charsToTok(Charlist, state):
	a = ''.join(Charlist)
	if state=='number': return int(a)
	else: return a

## when state is one either 'atom', 'number', 'alSymb', 'special',
##  or 'doubleE' it's a valid token	
def validToken(state):
	if state in ['number', 'string', 'paren']:
		return True
	else: return False

##"""
##munch(S):
##	chars = [],
##	state = 'empty',
##	while S != [] and canPush(head(S),state):
##		remove the first character of S and add it to the \
##		end of chars,
##		state := newState(state,c)
##	if validToken(state): return (charsToTok(chars), True))
##	else: return(None,False)
##"""

def munch(S):
	chars = []
	state = 'empty'
	while S != '' and canPush(S[0], state):
		chars = chars + [S[0]]
		state = newState(state, S[0])
		S = S[1:]
	if validToken(state): 
		if state =='string':
			chars = chars[1:len(chars)-1]
			return (charsToTok(chars, state), True, S)
		else: return (charsToTok(chars, state), True, S)
	else: return (None, False, S)
	
	
######################################################################
##"""
##tokens(S):
##	tokens = []
##	remove all initial white space from S,
##	while S is not empty
##		remove all initial white space from S,
##		(token,Flag) := munch(S)
##		if Flag:
##			tokens := tokens + [token]
##		else
##			return (None,False)
##	return (tokens,True)
##"""

def tokenize(S):
	tokens = []
	while S!='' and whitespace(S[0]):
		S = S[1:]
	while S != '':
		while S!='' and whitespace(S[0]):
			S = S[1:]
		(token, Flag, S1) = munch(S)
		if Flag:
			tokens = tokens + [token]
			S = S1
		else:
			S = S[1:]
	if tokens != []: return (tokens, True)
	else: return(None, False)
	


######################################################################
######################################################################

###########################    Parser     ############################

######################################################################
# If L is a list of tokens and :[i] is the beginning postion of a 
# subexpression within L, then nextExp(L, i) is the index of the end 
# of that subexpression in L, plus 1.
######################################################################

def nextExp(L, i):
	prenCount=0
	if L[i]=='(':
		prenCount+=1
		n=i+1
		while prenCount>0:
			if L[n]=='(': prenCount+=1
			if L[n]==')': prenCount-=1
			n+=1
		return n
	else: return i+1
		
######################################################################

##"""
##A theorem is a triple ( "t" s A ) where s is a statement and A is an
##argument .
##"""
def isTheorem(e):
	if e[0] =='(' and e[len(e)-1] ==')' and e[1] == 't':
		return True
	else: return False
	

def parseTheorem(L):
	p = L[2]
	A = parseArgument(L[3:len(L)-1])
	return ['t', p, A]


##"""
##An argument list of suppositions, assertions, and theorems, in which no
##supposition comes after an assertion or theorem.
##"""
def parseArgument(L):
	A, i = [], 1
	while L[i] != ')':
		A = A + [parse(L[i:nextExp(L,i)])]
		i = nextExp(L,i)
	return A



def parse(e):
	if isTheorem(e)		:	return parseTheorem(e)
	if isAssertion(e)	:	return parseAssertion(e)
	if isSupposition(e)	:	return e[0]

##""""
##A supposition is a string that begins with "Suppose"
##"""
def isSupposition(e):
	if len(e) == 1 and e[0][0:7] =='Suppose': return True
	else: return False
	
######################################################################


##""""
##An assertion is a triple ( "a" s J ) where s is a statement and J is a
##justification.
##"""
def isAssertion(e):
	if e[0] =='(' and e[len(e)-1] ==')' and e[1] == 'a':
		return True
	else: return False

def parseAssertion(e):
	s = e[2]
	J = parseJustification(e[3:len(e)-1])
	return ["a", s, J]
	
def parseJustification(L): return L[1:len(L)-1]


######################################################################
######################################################################
######################################################################

##argLength(A): A is argument list, argLength(A) returns the how many
## elements (including supposition, theorem and assertion) in the list
##argLength(A):
##        L=0
##        for e in A:
##                L=L+componentLength(A)
##        return L
def argLength(A):
	L=0
	for e in A:
		L = L + componentLength(e)
	return L

## e is an argument, componentLength(e) returns how many components the
## argument contains. 
##componentLength(e):
##        if isSupposition(e): return 1
##        if assertion(e): return 1
##        if theorem(e): return argLength(e[1])+1
def componentLength(e):
	if isSuppositionlist(e): return 1
	if isAssertionlist(e): return 1
	if isTheoremlist(e): return argLength(e[2]) + 1

## isSuppositionlist(e) is True when e is a string and begin with Suppose
def isSuppositionlist(e):
	if (type(e) is str) and e[0:7] =='Suppose':
		return True
	else:
		return False

## isAssertionlist(e) is True when e is a list whose first element is 'a'
def isAssertionlist(e):
	if (type(e) is list) and e[0] == 'a':
		return True
	else:
		return False

## isTheoremlist(e) is True when e is a list and its first element is 't'
def isTheoremlist(e):
	if (type(e) is list) and e[0] == 't':
		return True
	else:
		return False

##numberToNested(A, n):
##Given an argument and a non-negative integer n, less than or argLength(A),
##numberToNested is a list [n 1 ,...n k ] such that the n'th step of
##argument A is A[n 1 ]...[n k ]. For example,
##● numToNested(A,3) = [1,1,0] since line 3 above is really A[1][2][0]
##● numToNestedI(A,2) = [1,1], since line 2 is A[1][1]
##● numToNested(A,4) = [1,2,1], since line 4 is A[1][2][1]
def	numberToNested(A, n):
        if n < 1 or n > argLength(A):
                return print('Error: the line is not in the argument!')
        else:
                i = 0
                componentCount = 0
                oldCount = 0
                while componentCount < n:
                        oldCount = componentCount
                        componentCount = componentCount + componentLength(A[i])
                        i += 1
                if isSuppositionlist(A[i-1]):
                        return [i-1]
                elif isAssertionlist(A[i-1]):
                        return [i-1] + [1]
                elif (n == oldCount + 1) and isTheoremlist(A[i-1]):
                        return [i-1] + [1]
                else:
                        return [i-1]+[2]+numberToNested(A[i-1][2],
                                        n-oldCount-1)

								
# eg: N=[1, 2, 3, 4], return A[1][2][3][4]
def indexNested(A,N):
	if len(N) == 1: return A[N[0]]
	else:
		front = N[0:len(N)-1]
		back= N[len(N)-1]
		return indexNested(A,front)[back]
	
##Justifications(A,n) is
##the list of line numbers used to justify the n'th line in argument A.
##This list is empty unless the n'th line of A is an assertion.
##● Justifications(A,4) = [2,3]
##● Justifications(A,5)=[ ]
def justifications(A,n):
	N = numberToNested(A, n)
	if len(N) <= 1:
		return []
	else:
		upperList = indexNested(A,N[0:len(N)-1])
		if not isAssertionlist(upperList):
			return []
		elif len(upperList) <=2:
			return []
		else:
			return numberInList(upperList[2])

## L is list, numberInList(L) returns all the number type element in 
## a new list 
def numberInList(L):
	numbers = []
	for X in L:
		if type(X) is int:
			numbers = numbers + [X]
	return numbers
		
######################################################################
##suppositionsInForce(A,n) the
##line numbers of the suppositions in force at the n'th line of
##argument A.
##● suppositionsInForce(A,4)=[1,3]
##● suppositionsInForce(A,8) = [1]
def suppositionsInForce(A,n):
	supInForce = []
	N = numberToNested(A, n)
	line = 1
	while line <= n:
		Nline = numberToNested(A, line)
		if isSuppositionlist(indexNested(A, Nline)) and sameRoot(N, Nline):
			supInForce = supInForce + [line]
		line += 1
	return supInForce

##
def sameRoot(N1, N2):
        if len(N2) == 1:
                if N1[0] >= N2[0]: return True
                else: return False
        else:
                if len(N1) < len(N2): return False
                elif N1[len(N2)-1] < N2[len(N2)-1]:
                        return False
                elif N1[0:len(N2)-2] != N2[0:len(N2)-2]:
                        return False
                else: return True
######################################################################                        
## A is an argument, premiseOf(A) returns all the premises in A
def premiseOf(A):
	premise = []
	line = 1
	while line <= argLength(A):
		N = numberToNested(A, line)
		if len(N) != 1:         ## must be a supposition
			S= indexNested(A, N)
			upperList = indexNested(A,N[0:len(N)-1])
			if not isSuppositionlist(S):
				if isAssertionlist(upperList):
					jOfn = justifications(A, line)
					if jOfn == []:
						premise = premise + [S]
					elif len(jOfn) == 1:
						J = indexNested(A, numberToNested(A, jOfn[0]))
						p='\"'+J+'\"' + ' => ' + '\"'+ S + '\"'
						premise = premise + [p]
					else:
						J0 = indexNested(A, numberToNested(A, jOfn[0]))
						J1 = indexNested(A, numberToNested(A, jOfn[1]))
						Js = '\"'+ J0 + '\"' + ' & ' + '\"' + J1 + '\"'
						for X in jOfn[2:]:
							Jx = indexNested(A, numberToNested(A, X))
							Js = Js + ' & ' + '\"' + Jx + '\"'
						p= '(' + Js +')' + ' => ' + '\"'+ S + '\"'
						premise = premise + [p]
				elif isTheoremlist(upperList):
					if upperList[2] == []:
						premise = premise + [S]
					else:
						lastline = argLength(upperList[2]) + line
						lastArg = indexNested(A, numberToNested(A, lastline))
						SUPs = []
						for X in upperList[2][0: len(upperList[2]) - 1]:
							if isSuppositionlist(X):
								SUPs = SUPs + [X]
						if len(SUPs) == 0:
							p='\"'+lastArg+'\"' + ' => ' + '\"'+ S + '\"'
							premise = premise + [p]
						elif len(SUPs) == 1:
							p='(' + '\"'+SUPs[0]+'\"' + ' => ' + '\"' + lastArg + '\"' + ')' + ' => '+ '\"'+ S + '\"'
							premise = premise + [p]
						else:
							sup = '\"'+ SUPs[0] + '\"' + ' & ' + '\"' + SUPs[1] + '\"'
							for Y in SUPs[2:]:
								sup = sup + ' & ' + '\"' + Y + '\"'
							supToL = '(' + sup +')' + ' => ' + '\"'+ lastArg + '\"'
							p = '('+supToL+')' + ' => ' + '\"'+ S + '\"'
							premise = premise + [p]
		line += 1

	return premise


###################################################################### 
##A proof is correct if it is structurally valid and its premises are
##true.
##
##Intuitively, structural soundness depends on this: when a line
##number m appears in the justification for line n, the following must
##hold:
##a. m < n .
##b. every supposition in force at line m must also be in force at
##   line n .
def validProof(A):
	line = 1
	while line <= argLength(A):
		Js = justifications(A, line)
		sup =  suppositionsInForce(A, line)
		if Js != []:
			for X in Js:
				if X > line:
					return False
				sup1 = suppositionsInForce(A, X)
				for Y in sup1:
					if Y not in sup:
						return False
		line += 1
	return True
	

###################################################################### 
###################################################################### 
###################################################################### 
###################################################################### 
###################################################################### 
## main functions	
def proofcheck(S):
	(tokens, flag1) = tokenize(S)
	if not flag1:
		return print('Error: tokenizer fails!!!')
	A = parseTheorem(tokens)
	if not validProof(A[2]):
		return print('Failure: Invalid proof!!!')
	else:
		print('Valid Proof!! Check outfile for premises.')
		file = open('proofoutput.txt', 'w')
		file.write('The premises are as follows: \n\n')
		for X in premiseOf(A[2]):
			file.write('\''+ X + '\''+ '\n')
		lastArg = indexNested(A[2], numberToNested(A[2], argLength(A[2])))
		file.write('\'' + '(' + '\"'+A[2][0]+'\"' + ' => ' + '\"' + lastArg + '\"' + ')' + ' => '+ '\"'+ A[1] + '\"' + '\'')
		file.close()
	
	
	

		
		
	
	
			

