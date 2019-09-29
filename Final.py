import string
import sys					#file as arguement in command line.
import copy					#deep-copy lists

###############################################################################
#	LEKTIKOS ANALYTHS:														  #
#	(Kaleitai ws synarthsh apo ton syntaktiko analyth)						  #
###############################################################################
dx =0
line =1
position=1
def lex():
	'O Lektikos Analyths (lex), diabazei "gramma-gramma" to phgaio programma'
	'Return: Th Lektikh Monada alla kai enan "akeraio" pou thn xarakthrizei.'
	'Pio sygkekrimena: ("string", int)'
	###########################################################################
	#	
	#	AYTOMATO KATASTASEWN: ksekina apo mia arxikh katastash, me thn eisodo kathe xarakthra allazei katastash ews otou synanthsei mia telikh katastash.
	#		
	#	Returns: Lista apo 2 pramata: 
	#		Prwto einai ena string(anagnwristiko)
	#		Deytero einai mia stathera. Mia gia kathe periptwsh(case)
	#
	#	Edw, to aytomato anagnwrizei:
	#	>Desmeymenes lekseis:
	#		and, declare, do, else, enddeclare, exit, procedure, function, print, call, if, in, inout, not, select, program, or, return, while, default.
	#	>Symbola ths glwssas:
	#		(A...Z kai a...z) 		grammata
	#		(0...9)					pshfia
	#		(+, -, *, /) 			symbola arithmhtikwn praksewn
	#		(<, >, =, <=, >=, <>) 	telestes sysxetishs
	#		(:=, :) 				symbola anatheshs
	#		(;, ,) 					diaxwristes
	#		({, }, (, ), [, ]) 		symbola omadopoihshs
	#		(\*, *\)				diaxwrismos sxoliwn
	#	>Anagnwristika kai statheres:
	#		p.x. counter, a12, 32768
	#		*Oi arithmhtikes statheres sth Ciscal exoun eyros apo -32768 ews 32767.
	#		*Ta anagnwristika arxizoun apo Gramma kai synexizoun me gramma 'h pshfio.
	#			(Lambanei ypopsin tou mono ta 30 prwta grammata)
	#	>errors
	#
	###########################################################################
	
	#Opening file, as arguement in command line:
	try:
		fp = open(sys.argv[1], 'r')
	except IndexError:
		fp = open('sourceCode.txt', 'r')	#Without command line argument, open this specific sourceCode.txt
	
	#Define flags
	state0=0		#flag for return symbols (some go to other flags)
	state1=1		#flag for anagnwristika (apotelountai apo gramma kai epeita gramma h pshfio)
	state2=2		#flag for numbers
	state3=3		#flag for '<'
	state4=4		#flag for '>'
	state5=5		#flag for ':'
	state6=6		#flag of comments
	state7=7		#flag of comments
	state8=8		#flag of comments
	OK=-1			#OK flag
	error=-2		#ERROR flag
	EOF=-3			#End-Of-File flag
	
	negativeFlag=0  #flag for negative number

	#Arxikopoihsh listas Lektikhs Monadas
	lektikhMonada = []
	#Arxikopoihsh ths listas pou tha kanw return.
	LM = []
	#Arxikopoihsh listas desmeymenwn leksewn
	desmLexeis = [['and', 23], ['declare', 24], ['do', 25], ['else', 26], ['enddeclare', 27], ['exit', 28], ['procedure', 29], ['function', 30], ['print', 31], 
	['call', 32], ['if', 33], ['in', 34], ['inout', 35], ['not', 36], ['select', 37], ['program', 38], ['or', 39], ['return', 40], ['while', 41], ['default', 42]]
	
	#counting variables
	global dx										#Current file-pointer position.
	global line										#Current line. 					 Used to print (line:position)
	global position									#Current position inside a line. Used to print (line:position)
	
	countLetters = 0								#counting number of letters (state1)
	flagNumbers = 0									#counting >30 
	anagnwristiko = ''								#Arxikopoihsh anagnwristikou sto keno.
	
	
	fp.seek(dx)		#Seek to the last point,to get the next word.
	
	state=state0
	while(state!=OK and state!=error and state!=EOF):
		input = fp.read(1)							#Read new character from the file.
		position += 1
	
		#BUG found!?
		#My windows OS has 'Python 3.5.1'
		#Running on windows by cmd this file, command 'ftell()' appears suddenly a very large number. All running smoothly at Unix OS.
		#Check ftell()'s very large number, insted of 14:
		#print('Input: %s\tstate:%s \ttell:%d' % (input, state, fp.tell()))
	
		if(not input and state!=state7):			#state7 has its own EOF, wanted to print specific error in there.
			if(state==state1):						#Function exits in the following states
				state=OK
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM += [anagnwristiko] + [1]					#case1
			elif(state==state2):
				state=OK
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM += [anagnwristiko] + [2]					#case2
			else:
				state=EOF									#End-Of-File
				
		#state=EOF
		if(state==EOF):	
			LM = ['EOF'] + [44]			#case44
		#state0
		if(state==state0):
			if (input == '\t' or input==' ' or input=='\n'):	#TAB or SPACE or newline
				if (input == 't'):
					position+=8						#8 spaces is one TAB
				if(input=='\n'):
					line+=1
					position=0
				state=state0
			elif(input in string.ascii_letters):	#Letter
				state=state1										
			elif(input in string.digits):			#Digit			
				state=state2
			elif(input =='<'):
				state=state3
			elif(input=='>'):
				state=state4
			elif(input==':'):
				state=state5
			elif(input=='\\'):
				state=state6
			elif(input==''):		#EOF
				state=EOF
			
			elif(input=='\r'):		#return(hitting Enter button)
				state=state0
			else:
				state=OK
				lektikhMonada = input
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				if(input=='+'):
					LM += [anagnwristiko] + [3]
				elif(input=='-'):
					#Want to check if follows negative number.
					input = fp.read(1)
					position+=1
					if(input in string.digits):
						negativeFlag=1
						state=state2
					else:	
						fp.seek(fp.tell()-2)
						position-=2
						input=fp.read(1)
						position+=1
						LM += [anagnwristiko] + [4] 					
				elif(input=='*'):
					LM += [anagnwristiko] + [5]
				elif(input=='/'):
					LM += [anagnwristiko] + [6]
				elif(input==';'):
					LM += [anagnwristiko] + [7]
				elif(input==','):
					LM += [anagnwristiko] + [8]
				elif(input=='{'):
					LM += [anagnwristiko] + [9]
				elif(input=='}'):
					LM += [anagnwristiko] + [10]
				elif(input=='('):
					LM += [anagnwristiko] + [11]
				elif(input==')'):
					LM += [anagnwristiko] + [12]
				elif(input=='['):
					LM += [anagnwristiko] + [13]
				elif(input==']'):
					LM += [anagnwristiko] + [14]
				elif(input=='='):
					LM += [anagnwristiko] + [15]
				else:				
					state=error
					print('error: Unknown character= %s' % input)
					print('Line> %d:%d' % (line, position))
		#state1
		if(state==state1):
			if(input in string.ascii_letters or input in string.digits):
				countLetters +=1
				if(countLetters>30):						#O metaglwttisths tha lambanei ypopsin MONO ta 30 prwta gramata. (Ta alla ta agnoei)
					flagNumbers = countLetters-30	
				if(flagNumbers >= 1):
					anagnwristiko = "".join(lektikhMonada)	#Returning format
					LM += [anagnwristiko] + [1]				#case1	
				else:						
					lektikhMonada += input
					state= state1
			else:
				state= OK
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM = [anagnwristiko] + [1]					#case1

				if(flagNumbers>=1):
					print('warning: Word with size >30 characters.')
					print('Line> %d:%d' % (line, position))
				
				fp.seek(fp.tell()-1)						#Seek back one position.
				position-=1
		#state2
		if(state==state2):
			if(input in string.digits):	
				state=state2
				lektikhMonada += input
			else:
				state=OK
							
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM += [anagnwristiko] + [2]					#case2	
				fp.seek(fp.tell()-1)
				position-=1
				if(int(anagnwristiko)>32767 or int(anagnwristiko)<(-32768)):	#Oi akeraioi arithmoi ths Ciscal prepei na exoun akeraies times apo -32768 ews 32767.
					state=error
					if int(anagnwristiko)>32767:
						print('error: Number %d is > than the limit (32767)' % int(anagnwristiko))
						print('Line> %d:%d' % (line, position))
					else:
						print('error: Number %d is < than the limit (-32768)' % int(anagnwristiko))
						print('Line> %d:%d' % (line, position))
		#state3
		if(state==state3):
			state=OK
			input=fp.read(1)
			position+=1
			if(input=='='):
				lektikhMonada = '<='
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM += [anagnwristiko] + [16]				#case16
			elif(input=='>'):
				lektikhMonada = '<>'
				anagnwristiko = "".join(lektikhMonada)
				LM += [anagnwristiko] + [17]				#case17
			else:
				lektikhMonada = '<'
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM += [anagnwristiko] + [18]				#case18
				fp.seek(fp.tell()-1)						#Seek back
				position-=1
		#state4
		if(state==state4):
			state=OK
			input=fp.read(1)
			position-=1
			if(input=='='):
				lektikhMonada = '>='
				anagnwristiko = "".join(lektikhMonada)		#Returning format
				LM += [anagnwristiko] + [19]				#case19
			else:
				lektikhMonada = '>'
				anagnwristiko = "".join(lektikhMonada)
				LM += [anagnwristiko] + [20]				#case20
				fp.seek(fp.tell()-1)						#Seek back
				position-=1
		#state5
		if(state==state5):
			input=fp.read(1)		
			position+=1
			if(input=='='):
					state=OK
					lektikhMonada = ':='
					anagnwristiko = "".join(lektikhMonada)	#Returning format
					LM += [anagnwristiko] + [21]			#case21
			else:
				state=OK
				lektikhMonada = ':'
				fp.seek(fp.tell()-1)						#Seek back
				position-=1
				anagnwristiko = "".join(lektikhMonada)
				LM += [anagnwristiko] + [22]
		#state6
		if (state==state6):
			input=fp.read(1)		
			position+=1
			if(input=='*'):
				state=state7
				input = fp.read(1)							#Follows state7 so read his character.
				position +=1
		#Den yparxoun sxolia mias grammhs ('\\')
		#	elif(input=='\\'):		
		#		state=error
		#		
		#		fp.seek(fp.tell()-1)							#Seek back
		#		position -= 1
		#		print('error: After "\\" is missing "*". \tNo1.')
		#		print('Line> %d:%d' % (line, position))
			else:
				state=error
				fp.seek(fp.tell()-1)							#Seek back
				position -= 1
				print('error: After "\\" is missing "*".')
				print('Line> %d:%d' % (line, position))
		#state7
		if(state==state7):
			if(input=='*'):
				state=state8
			elif(input==''):									#EOF
				state=error
				print('error: Unclosed comments. \tNo1')
				print('Line> %d:%d' % (line, position))
			elif(input=='\n'):									#NewLine
				line +=1
				position=0
			elif(input=='\t'):
				position+=8										#8 spaces is one TAB
			else:						
				input=fp.read(1)								#Move File-Pointer forward to check EOF.
				position+=1
				if(input==''):
					state=error
					print('error: Unclosed comments. \tNo2')
					print('Line> %d:%d' % (line, position))
				else:
					fp.seek(fp.tell()-1)
					position-=1
		#state8
		if(state==state8):
			input = fp.read(1)
			position+=1
			if(input=='\\'):
				state=state0
			elif(input==''): 									#EOF
				state=error
				print('error: Unclosed comments.')
				print('Line> %d:%d' % (line, position))
			elif(input=='*'):
				state=state8
				fp.seek(fp.tell()-1)							#Seek back
				position-=1
			else:
				state=state7
				fp.seek(fp.tell()-1)							#Seek back
				position-=1
		#state=error
		if(state==error):
			lektikhMonada = '-2'
			LM = ['error'] +[-2]				#case=-2
 
	dx = fp.tell()								#Save position for next function call.

	#An to anagnwristiko einai mia apo tis Desmeymenes Lekseis, add his own number case(23ews42) in the end.
	anagnwristiko = "".join(lektikhMonada)
	for i in range(len(desmLexeis)):
		if	anagnwristiko == desmLexeis[i][0]:
			LM.pop()
			LM += [desmLexeis[i][1]]
			break
	
	#TestPrint: line with position, state, lektikhMonada, anagnwristiko, LM(returned list)
	#print('PrintStatus: \n\tline=\t%d:%d \n\tstate=\t%d \n\tlektikhMonada=\t%s \n\tanagnwristiko=\t%s \n\tLM[0]=\t%s \n/tLM[1]=\t%s' % (line, position, state, lektikhMonada, anagnwristiko, LM[0], LM[1]))

	fp.close()									#Close open files
	return LM[0],LM[1]
def printLex():
	'Check testForLex.txt file'
	#Calling lex() in the whole file:
	print('Return value ( LM,case ): \n(LM=Lektikh Monada, case=O arithmos pou thn xarakthrizei.)')
	while(1):
		tupl = lex()
		LMonada = tupl[0]
		case = tupl[1]
		print('>\t( %s,%d )' % (tupl[0], tupl[1]))
		print('______________________________________________________________|')
		
		if(case==44): 	#case44=EOF
			break
	return
#printLex()

###############################################################################
#	Synarthseis ENDIAMESOU KWDIKA:											  #
###############################################################################
global listOfAllQuads		#lista me Oles tis tetrades pou tha paraxthoun apo to programma.
listOfAllQuads = []
countQuad = 1				#O arithmos pou xarakthrizei thn tetrada. Brisketai mprosta apo thn 4ada.
def nextQuad():
	'Epistrefei ton arithmo ths epomenhs tetradas pou prokyptei otan paraxthei.'
	global countQuad
	
	return countQuad
def genQuad(first, second, third, fourth):
	'Dhmiourgei thn epomenh 4ada.'
	'Prwto stoixeio sth lista tha balw ton arithmo ths nextQuad(), ousiastika tha ginei 5ada.'
	global countQuad
	global listOfAllQuads
	list = []
	
	list = [nextQuad()]			#Bazw prwta ton arithmo.
	list += [first] + [second] + [third] + [fourth]		#Epeita ta orismata
	
	countQuad +=1	#Ayksanw kata 1 ton arithmo ths epomenhs 4adas.
	listOfAllQuads += [list] 	#Put quad in global listOfAllQuads.
	return list

T_i = 1
listOfTempVariables = []
def newTemp():
	'Dhmiourgei kai epistrefei mia nea proswrinh metablhth, ths morfhs T_1, T_2,.. .'
	global T_i
	global listOfTempVariables
	
	list = ['T_']
	list.append(str(T_i))
	tempVariable="".join(list)
	T_i +=1
	
	#Save them in listOfTempVariables(is used in 'cCode()' function)
	listOfTempVariables += [tempVariable]

	ent = Entity()								#Create an Entity
	ent.type = 'TEMP'							#
	ent.name = tempVariable						#
	ent.tempVar.offset = compute_offset()		#
	new_entity(ent)								#
	
	return tempVariable
def emptyList():
	'Dhmiourgei mia kenh lista etiketwn 4dwn.'
	pointerList = []	#Arxikopoihsh pointer list.
	
	return pointerList
def makeList(x):
	'Dhmiourgei mia lista etiketwn tetradwn pou periexei mono to x.'
	
	#Den kserw an edw tha xreiazetai diplh lista: listThis=[[x]], tha deiksei.
	listThis = [x]
	
	return listThis
def merge(list1, list2):
	'Dhmiourgei mia lista etiketwn 4dwn apo th synenwsh listwn list1, list2.'
	list=[]
	list += list1 + list2

	return list
def backPatch(list, z):
	'H lista "list" apoteleitai apo deiktes se tetrades ths listOfAllQuads, twn opoiwn to teleytaio teloumeno Den einai symplhrwmeno.'
	'H backPatch episkeptetai mia mia tis 4des aytes kai tis symplhrwnei me thn etiketa z.'
	'''Prepei na sarwsw th listOfAllQuads kai gia kathe 4ada, pou exei prwto teloumeno arithmo
		pou periexetai sthn list:
		Otan briskw '_' sto 4o teloumeno twn 4dwn aytwn,
		tha to symbplhrwsw me to "z".
	'''
	global listOfAllQuads
	
	for i in range(len(list)):
		for j in range(len(listOfAllQuads)):
			if(list[i]==listOfAllQuads[j][0] and listOfAllQuads[j][4]=='_'):
				listOfAllQuads[j][4] = z
				j=len(listOfAllQuads)	#to pass second loop faster and enter next i.
	return

###############################################################################
#	Synarthseis PINAKA SYMBOLWN:											  #
###############################################################################	
class Argument():
	' /_\  <- Trigwno'
	def __init__(self):
		self.name = ''		#Dinw to name gia na kserw poio Argument einai.
		self.type = 'Int'	#All variables in this language will be Int.
		self.parMode = ''	# 'RET', 'CV', 'REF'
class Entity():
	' _ _ 				 '
	'|___|	<- Orthogwnio'

	def __init__(self):
		self.name = ''					#Dinw to name gia na kserw poio Entity einai.
		self.type = ''	
		
		self.variable = self.Variable()
		self.subprogram = self.SubProgram()
		self.parameter = self.Parameter()
		self.tempVar = self.TempVar()
		self.constant = self.Constant()
	class Variable:
		def __init__(self):
			self.type = 'Int'
			self.offset = 0				# Apostash apo thn arxh ths stoibas.
	class SubProgram:					# functions or procedures
		def __init__(self):
			self.type = ''				# 'int' -> function,   'void' -> procedure.
			self.startQuad = 0			# nextQuad().
			self.frameLength = 0		# To mhkos eggrafhmatos drasthriopoihshs.
			self.argumentList = my_arguments			#h lista parametrwn.
	class Constant:
		def __init__(self):
			self.value = ''
	class Parameter:
		def __init__(self):
			self.mode = ''				# 'RET', 'CV', 'REF'
			self.offset = 0				# Apostash apo thn arxh ths stoibas.
	class TempVar:
		def __init__(self):
			self.type = 'Int'			
			self.offset = 0				# Apostash apo thn arxh ths stoibas.
class Scope():
	'(_)  <- Kyklos'
	def __init__(self):
		self.name = ''						#Dinw to name gia na kserw poio Scope einai.
		self.entityList = my_entities		#h lista apo entities
		self.nestingLevel = 0				# Bathos fwliasmatos.
		self.enclosingScope = my_scopes			#Perikleionta scopes, oxi mono aytou tou scope, alla OLWN twn scope.

my_arguments = []						#list of Argument objects
my_arguments = copy.deepcopy(my_arguments)
def new_argument(object):
	'Add given object to list'
	global my_arguments, my_entities
	
	my_arguments.append(object)			#add object to list my_arguments.
	my_entities[-1].subprogram.argumentList.append(object)
	
my_entities = []						#list of Entity objects
my_entities = copy.deepcopy(my_entities)
def new_entity(object):
	'Add given object to list'
	global my_arguments, my_entities, my_scopes
	
	my_scopes[-1].entityList.append(object)
	my_entities.append(object)			#add object to list my_entities.
	
	my_arguments = []					#Mhdenismos listas twn Arguments, gia na gemisei me kainouries times, sto epomeno entity.

my_scopes = []							#list of Scope objects.
my_scopes = copy.deepcopy(my_scopes)	
firstScope = Scope()					#Arxikopohsh tou prwtou scope.
my_scopes.append(firstScope)			#add object to list my_scopes.

firstTimeFlag=1
def new_scope(name):
	'create new scope'
	global firstScope, my_entities, my_scopes, firstTimeFlag
	
	firstScope.name = name
	
	nextScope = Scope()
	
	if(not firstTimeFlag):
		nextScope.enclosingScope.append(firstScope)	#To nextScope perikleietai sto firstScope. 

	firstScope = nextScope
	firstScope.entityList = []
	my_entities = []								#Mhdenismos listas twn Entities, gia na ksanaparoun times.
	
	#next Scope is at next nesting-Level:
	if(firstScope.enclosingScope == []):
		firstScope.nestingLevel = 0
	else:
		firstScope.nestingLevel = firstScope.enclosingScope[-1].nestingLevel + 1
	firstTimeFlag=0	

def delete_scope():
	global my_scopes
	
	if(my_scopes!=[]):
		del my_scopes[-1]				#delete last scope.

def compute_offset():
	'Computes how many bytes '
	global my_scopes
	
	counter=0
	if(my_scopes[-1].entityList is not []):
		for ent in (my_scopes[-1].entityList):
			if(ent.type == 'VAR' or ent.type == 'TEMP' or ent.type=='SUBPR' or ent.type=='PARAM'):
				counter +=1
	#SizeOf Int variable = 4 and 'Fixed starting size': 3*4=12
	offset = 12+(counter*4)
	
	return offset

def compute_startQuad():
	'Compute startQuad (=current Quad) of function or procedure.'
	global my_scopes
	
	for E in my_scopes[-1].enclosingScope[-2].entityList:
		if(E.type == 'SUBPR' and E.name==my_scopes[-1].enclosingScope[-1].name):
			E.subprogram.startQuad = nextQuad()
		
def compute_framelength():
	'Compute frameLength of function or procedure.'
	global my_scopes
	
	for E in my_scopes[-1].enclosingScope[-2].entityList:
		if(E.type == 'SUBPR' and E.name==my_scopes[-1].enclosingScope[-1].name):
			E.subprogram.frameLength = compute_offset()
	
def add_parameters():
	'Create Entities of Parameters of functions or procedures. (ec. in a, inout b)'
	global my_arguments
	
	offset = compute_offset()
	
	for arg in my_arguments:
		ent = Entity()
		ent.name = arg.name
		ent.type = 'PARAM'
		ent.parameter.mode = arg.parMode
		ent.parameter.offset = offset
		new_entity(ent)
	
def print_Symbol_table():
	'Prints Symbol-Table: Scopes, Entities, Arguements'
	global my_scopes, my_entities, my_arguments
	
	print("########################################################################################")
	print("")
	for sco in my_scopes:
		print("SCOPE: "+"name:"+sco.name+" nestingLevel:"+str(sco.nestingLevel))
		#print(len(sco.enclosingScope))
		print("\tENTITIES:")
		for ent in sco.entityList:
			if(ent.type == 'VAR'):
				print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t variable-type:"+ent.variable.type+"\t offset:"+str(ent.variable.offset))
			elif(ent.type == 'TEMP'):
				print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t temp-type:"+ent.tempVar.type+"\t offset:"+str(ent.tempVar.offset))
			elif(ent.type == 'SUBPR'):
				if(ent.subprogram.type == 'Function'):
					print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t function-type:"+ent.subprogram.type+"\t startQuad:"+str(ent.subprogram.startQuad)+"\t frameLength:"+str(ent.subprogram.frameLength))
					print("\t\tARGUMENTS:")
					for arg in ent.subprogram.argumentList:
						print("\t\tARGUMENT: "+" name:"+arg.name+"\t type:"+arg.type+"\t parMode:"+arg.parMode)
				elif(ent.subprogram.type == 'Procedure'):
					print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t procedure-type:"+ent.subprogram.type+"\t startQuad:"+str(ent.subprogram.startQuad)+"\t frameLength:"+str(ent.subprogram.frameLength))
					print("\t\tARGUMENTS:")
					for arg in ent.subprogram.argumentList:
						print("\t\tARGUMENT: "+" name:"+arg.name+"\t type:"+arg.type+"\t parMode:"+arg.parMode)
			elif(ent.type == 'PARAM'):
				print("\tENTITY: "+" name:"+ent.name+"\t type:"+ent.type+"\t mode:"+ent.parameter.mode+"\t offset:"+str(ent.parameter.offset))
	print("########################################################################################")
###############################################################################
#	SYNTAKTIKOS ANALYTHS & ENDIAMESOS KWDIKAS:								  #
###############################################################################
###############################################################################
#  FINAL CODE#
###############################################################################

def final(asciiFile):
	global listOfAllQuads
	for i in range(len(listOfAllQuads)):
		if (listOfAllQuads[i][1] == 'jump'):
			asciiFile.write('j'+' '+str(listOfAllQuads[i][4])+'\n')
		if (listOfAllQuads[i][1] == '='): 
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('beq,$t1,$t2,'+str(listOfAllQuads[i][4])+'\n')
		if (listOfAllQuads[i][1] == '<>'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('bne,$t1,$t2,'+str(listOfAllQuads[i][4])+'\n')
		if (listOfAllQuads[i][1] == '>'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('bgt,$t1,$t2,'+str(listOfAllQuads[i][4])+'\n')
		if (listOfAllQuads[i][1] == '<'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('blt,$t1,$t2,'+str(listOfAllQuads[i][4])+'\n')
		if (listOfAllQuads[i][1] == '>='):	
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('bge,$t1,$t2,'+str(listOfAllQuads[i][4])+'\n')
		if (listOfAllQuads[i][1] == '<='):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('ble,$t1,$t2,'+str(listOfAllQuads[i][4])+'\n')	
		if (listOfAllQuads[i][1] == ':='):
			##loadvr(listOfAllQuads[i][2],1)
			##storerv(1,listOfAllQuads[i][4])
			pass
		if (listOfAllQuads[i][1] == '+'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('+,$t1,$t1,$t2'+'\n')
			##storerv(1,listOfAllQuads[i][4])
		if (listOfAllQuads[i][1] == '-'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('-,$t1,$t1,$t2'+'\n')
			##storerv(1,listOfAllQuads[i][4])
		if (listOfAllQuads[i][1] == '*'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('*,$t1,$t1,$t2'+'\n')
			##storerv(1,listOfAllQuads[i][4])
		if (listOfAllQuads[i][1] == '/'):
			##loadvr(listOfAllQuads[i][2],1)
			##loadvr(listOfAllQuads[i][3],2)
			asciiFile.write('/,$t1,$t1,$t2'+'\n')
			##storerv(1,listOfAllQuads[i][4])
		if (listOfAllQuads[i][1] == 'out'):
			asciiFile.write('li $v0,1'+'\n')
			asciiFile.write('li $a0,'+listOfAllQuads[i][4]+'\n')
			asciiFile.write('syscall'+'\n')

'''
def storerv(r,v):

'''

'''
def gnlvcode(v):
	global my_scopes	
	level = 0  ##isws gia na dw posa epipeda panw brisketai h v
	
	for sco in reversed(my_scopes):
		level+=1
		for in ent sco.entityList:
			if (v is ent.name and ent.type == 'VAR):
				pass

'''
'''
def loadvr(v, r):
	asciiFile = open('asciiFile.ascii', 'w')
	if (v.isdigit()): ##if v is constant    isws na mhn einai swsto gt prepei na dwsoume kateutheian arithmo ws eisodo
		asciiFile.write('li $t%d,%s\n' % (r,v))

	print(my_scopes[0].entityList[0].name)

	for ent in my_scopes[0].entityList: ##checks if v is global
		print(ent.name)
		if (v is ent.name and ent.type == 'VAR'):
			asciiFile.write('lw $t%d,-%d($s0)\n'%(r,ent.variable.offset))
	##tha dw pws tha ta balw gt exw 2 for
		
	for ent in my_scopes[-1].entityList:
		if (v is ent.name and ent.type == 'VAR'):   ##mhpws thelei v.type?
			asciiFile.write('lw $t%d,-%d($sp)\n'%(r,ent.variable.offset))
			
		if (v is ent.name and ent.type == 'PARAM' and ent.parameter.mode == 'CV'): ##den jerw pws na tsekarw ta nestinglevels
			asciiFile.write('lw $t%d,-%d($sp)\n'%(r,ent.parameter.offset))
			
		if (v is ent.name and ent.type == 'TEMP'): ##checks for tempVar
			asciiFile.write('lw $t%d,-%d($sp)\n'%(r,ent.tempVar.offset))
			
		if (v is ent.name and ent.type == 'PARAM' and ent.parameter.mode == 'REF'): ##to idio gia ta nestinglevels
			asciiFile.write('lw $t0,-%d($sp)\n'%(ent.parameter.offset))

'''
def syntaktikosAnalyths(cF):
	'(Edw, ginetai elegxos gia na dipistwthei ean to phgaio programa anhkei h oxi sth glwssa,'
	' akolouthwntas th Grammatikh ths Ciscal).'
	global token					#saves next Lektikh Monada.
	global temp
	#flags:
	global inDoWhileFlag, exitFlag, atLeastOneReturn, isFuncFlag	
	
	#Initialization of global flags
	inDoWhileFlag, exitFlag, atLeastOneReturn, isFuncFlag = 0,0,0,0
	
	#Load first token to start.
	token = lex()
	def program():
		'<PROGRAM> ::= program ID <BLOCK>'
		global token
		
		if(token[0]=='program'):
			token=lex()
			if(token[1]==1):						#ID(anagnwristiko) (= Prwto gramma, epeita gramma 'h pshfio).
				programName = token[0]	
				
				token=lex()
				block(programName, 1)
			else: 
				print('error: Program\'s name was expected, instead of "%s". \tLine> %d:%d' % (token[0], line, position))
				exit(1)
		else:
			print('error: The keyword "program" was expected, instead of "%s". \tLine> %d:%d' % (token[0], line, position))
			exit(1)
		return
	def block(blockName, mainProgramBlockFlag):
		'<BLOCK> ::= { <DECLARATIONS> <SUBPROGRAMS> <SEQUENCE> }'
		global token
		
		if(token[0]=='{'):
			token=lex()
			new_scope(blockName)
			
			if(mainProgramBlockFlag!=1):		#Edw, gia ta orismata twn procedure 'h function, creates Entities.
				add_parameters()
			
			if(token[0]=='declare'):
				declarations()
			
			subPrograms()
			
			genQuad('begin_block', blockName, '_', '_')
			
			if(mainProgramBlockFlag!=1):		#Edw, ypologizetai to startQuad, ths epomenhs 4adas, meta apo function 'h procedure.
				compute_startQuad()
			
			sequence()
			
			#Yparxei "exit" mono mesa se brogxous do-while:
			if(inDoWhileFlag!=1 and exitFlag==1):
				print('error: "exit" can be placed only inside "do-while". \tLine> %d:%d' % (line, position))
				exit(1)
			
			if(token[0]=='}'):
				ekleiseToBlockFlag = 1
				
				token=lex()
				if(mainProgramBlockFlag==1):
					genQuad('halt', '_', '_', '_')
					#print(my_scopes[0].name)
					

				else:
					compute_framelength()			#Meta to telos tou block, Ypologismos tou eggrafhmatos drasthriopoihshs(frameLength).
				
				genQuad('end_block', blockName, '_', '_')
				
				print("Print Symbol-Table:")
				print_Symbol_table()



				##final()
				delete_scope()
				print("Last scope deleted.")
			else:
				print('error: Expected right brackets "}" before "%s" \n\tor else ";". \tLine> %d:%d' % (token[0], line, position))
				exit(1)
		else: 
			print('error: Missing open brackets "{" before "%s". \t Line> %d:%d' % (token[0], line, position))
			exit(1)
		return
	def declarations():
		'<DECLARATIONS> ::= e | declare <VARLIST> enddeclare'
		global token
		
		if(token[0]=='declare'):
			cF.write("int ")
			token=lex()	
			varList()
			if(token[0]=='enddeclare'):
				cF.write(";\n\t")
				token=lex()
			else: 
				print('error: The keyword "enddeclare" was expected. \tLine> %d:%d' % (line, position))
				exit(1)
		return	
	def varList():
		'<VARLIST> ::= e | ID ( , ID )*'
		global token
		
		if(token[1]==1):							#anagnwristiko ID
			cF.write(token[0])
			
			ent = Entity()							#Create an Entity
			ent.type = 'VAR'						#
			ent.name = token[0]						#
			ent.variable.offset = compute_offset()	#
			new_entity(ent)							#
			
			token=lex()
			while(token[0]==','):
				cF.write(token[0])
				token=lex()
				if(token[1]==1):							#anagnwristiko ID
					cF.write(token[0])
					
					ent = Entity()							#Create an Entity
					ent.type = 'VAR'						#
					ent.name = token[0]						#
					ent.variable.offset = compute_offset()	#
					new_entity(ent)							#
					
					token=lex()
				else:	
					print('error: Expected variable before "%s" in declarations. \tLine> %d:%d' % (token[0], line, position))
					exit(1)
		return
	def subPrograms():
		'<SUBPROGRAMS> ::= ( <FUNC> ) *'
		global token
		
		while(token[0]=='procedure' or token[0]=='function'):
			func()
		return
	def func():
		'<FUNC> ::= procedure ID <FUNCBODY> |'
		'			function ID <FUNCBODY>	 '
		global token

		if(token[0]=='procedure'):
			token=lex()
			if(token[1]==1):									#anagnwristiko ID
				#Save procedure's name
				name=token[0]
				
				ent = Entity()						#Create an Entity
				ent.type = 'SUBPR'					#
				ent.name = token[0]					#
				ent.subprogram.type = 'Procedure'	#
				new_entity(ent)						#
				
				token=lex()	
				funcBody(name, 0)			# 0 -> epeidh den einai function.
			else: 
				print('error: procedure\'s name was expected. \tLine> %d:%d' % (line, position))
				exit(1)
		elif(token[0]=='function'):
			token=lex()
			if(token[1]==1):									#anagnwristiko ID
				#Save function's name
				name=token[0]
				
				ent = Entity()						#Create an Entity
				ent.type = 'SUBPR'					#
				ent.name = token[0]					#
				ent.subprogram.type = 'Function'	#
				new_entity(ent)						#
				
				token=lex()
				funcBody(name, 1)			# 1 -> epeidh einai function.
			else: 
				print('error: function\'s name was expected. \tLine> %d:%d' % (line, position))
				exit(1)

		return	
	def funcBody(blockName, isFunction):
		'<FUNCBODY> ::= <FORMALPARS> <BLOCK>'
		global token, atLeastOneReturn

		formalPars()
		block(blockName, -1)		# -1 because its not program's main block.
		
		#Kathe function exei mesa ths toulaxiston ena "return"
		if(isFunction == 1):		# is function indeed
			if(atLeastOneReturn != 1):
				print('error: Function "%s" hasn\'t "return()". \tLine> %d:%d' % (blockName, line, position))
				exit(1)
			else:
				atLeastOneReturn=0
		return			
	def formalPars():
		'<FORMALPARS> ::= ( e | <FORMALPARLIST> )'
		global token
		
		if(token[0]=='('):
			token=lex()
			if(token[0]=='in' or token[0]=='inout'):
				formalParList()
				if(token[0]==')'):
					token=lex()
					return
				else: 
					print('error: Unclosed ")" in parameters. \tLine> %d:%d' % (line, position))
					exit(1)
			elif(token[0]==')'):
				token=lex()
				return
			else:
				print('error: Expected "in" or "inout" to fill in parameters, or \n\t ")" if there are no parameters. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "(" before "%s", to fill in parameters. \tLine> %d:%d' % (token[0], line, position))
			exit(1)	
	def formalParList():
		'<FORMALPARLIST> ::= <FORMALPARITEM> ( , <FORMALPARITEM> )*'
		global token
	
		formalParItem()
		while(token[0]==','):
			token=lex()
			if(token[0]=='in' or token[0]=='inout'):
				formalParItem()
			else:
				print('error: Expected "in"(by value) or "inout"(by reference) after ",". \tLine> %d"%d' % (line, position))
				exit(1)
		return		
	def formalParItem():
		'<FORMALPARITEM> ::= in ID | inout ID'
		global token
		
		if(token[0]=='in'):
			token=lex()
			if(token[1]==1):					#anagnwristiko ID
				arg = Argument()		#Creation of a new argument. (Pinakas Symbolwn)
				arg.name = token[0]		#
				arg.parMode = 'CV'		#
				new_argument(arg)		#
				
				token=lex()
				return
			else:	
				print('error: Expected variable\'s name after "in". \tLine> %d:%d' % (line, position))
				exit(1)
		elif(token[0]=='inout'):
			token=lex()
			if(token[1]==1):					#anagnwristiko ID
				arg = Argument()		#Creation of a new argument. (Pinakas Symbolwn)
				arg.name = token[0]		#
				arg.parMode = 'PAR'		#
				new_argument(arg)		#
				
				token=lex()
				return
			else:	
				print('error: Expected variable\'s name after "inout". \tLine> %d:%d' % (line, position))
				exit(1)
		return
	def sequence():
		'<SEQUENCE> ::= <STATEMENT> ( ; <STATEMENT> )*'
		global token
		
		statement()
		while(token[0]==';'):
			token=lex()
			statement()
		return	
	def bracketsSeq():
		'<BRACKETS-SEQ> ::= { <SEQUENCE> }'
		global token
		
		if(token[0]=='{'):
			token=lex()
			sequence()
			if(token[0]=='}'):
				token=lex()
				return
			else:
				print('error: Expected ";" or right brackets "}" before "%s". \tLine> %d:%d' % (token[0], line, position))
				exit(1)
		else:
			print('error: Must open brackets "{" before "%s". \tLine> %d:%d' % (token[0], line, position))
			exit(1)
		return
	def brackOrStat():
		'<BRACK-OR-STAT> ::= <BRACKETS-SEQ> | <STATEMENT>;'
		global token
		
		#Token of bracketsSeq() is '{':
		if(token[0]=='{'):
			bracketsSeq()
			return
		#Token of statement() is 1 or 'if' or 'do' or 'while' or 'select' or 'exit' or 'return' or 'print' or 'call':
		elif(token[1]==1 or token[0]=='if' or token[0]=='do' or token[0]=='while' or token[0]=='select' 
		or token[0]=='exit' or token[0]=='return' or token[0]=='print' or token[0]=='call'):
			statement()
			if(token[0]==';'):
				token=lex()
				return
			else:
				print('error: Expected ";" at the end of statement. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected brackets "{" or statement. \tLine> %d:%d' % (line, position))
			exit(1)
		return	
	def statement():
		'<STATEMENT> ::= e |	'
		'	<ASSIGNMENT-STAT> | '
		'	<IF-STAT> |			'
		'	<DO-WHILE-STAT> |	'
		'	<WHILE-STAT> |		'
		'	<SELECT-STAT> |		'
		'	<EXIT-STAT> |		'
		'	<RETURN-STAT> |		'
		'	<PRINT-STAT> |		'
		'	<CALL-STAT>			'
		global token
		
		if(token[1]==1):			#anagnwristiko ID
			assignmentStat()
		elif(token[0]=='if'):
			ifStat()
		elif(token[0]=='do'):
			doWhileStat()
		elif(token[0]=='while'):
			whileStat()
		elif(token[0]=='select'):
			selectStat()
		elif(token[0]=='exit'):
			exitStat()
		elif(token[0]=='return'):
			returnStat()
		elif(token[0]=='print'):
			printStat()
		elif(token[0]=='call'):
			callStat()
		return
	def assignmentStat():
		'<ASSIGNMENT-STAT> ::= ID := <EXPRESSION>'
		'''
			AS-> ID := E {P1}
		'''
		global token, temp, isFuncFlag
		
		#Mpainei sthn assignmentStat token=ID(anagnwristiko).
		#save it:
		id= token[0]
		#Load next token:
		token=lex()
		if(token[0]==':='):
			token=lex()
			Eplace =expression()
			#{P1}:
			if(isFuncFlag==1):					# if its function
				genQuad(':=', temp, '_', id)
				isFuncFlag=0
			else:
				genQuad(':=', Eplace, '_', id)
		else:
			print('error: Expected ":=" to fill in variable, before "%s". \tLine> %d:%d' % (token[0], line, position))
			exit(1)
		return
	def expression():
		'<EXPRESSION> ::= <OPTIONAL-SIGN> <TERM> ( <ADD-OPER> <TERM>)*'
		'Xrhsimopoieitai gia thn Anathesh Timhs mias metablhths \'h mias statheras, \'h mias ekfrashs se metablhth.'
		'''
			E-> T1 (+- T2 {P1})* {P2}
		'''
		global token
		
		optionalSign()
		T1place =term()
		while(token[0]=='+' or token[0]=='-'):
			plusOrMinus =addOper()
			T2place =term()
			#{P1}:
			w = newTemp()
			genQuad(plusOrMinus, T1place, T2place, w)
			T1place = w
		#{P2}:
		Eplace = T1place
		return Eplace		
	def optionalSign():
		'<OPTIONAL-SIGN> ::= e | <ADD-OPER>'
		global token
		
		if(token[0]=='+' or token[0]=='-'):
			addOrSubstr =addOper()
			return		
	def addOper():
		'<ADD-OPER> ::= + | -'
		global token
		
		if(token[0]=='+' or token[0]=='-'):
			addOp = token[0]					#save and return '+' or '-'.
			token=lex()
		return addOp	
	def term():
		'<TERM> ::= <FACTOR> (<MUL-OPER> <FACTOR>)*'
		'''
			T-> F1 (mulOper F2 {P1})* {P2}
		'''
		global token
		
		F1place =factor()
		while(token[0]=='*' or token[0]=='/'):
			mulOrDiv =mulOper()
			F2place =factor()
			#{P1}:
			w=newTemp()
			genQuad(mulOrDiv, F1place, F2place, w)
			F1place = w
		#{P2}:
		Tplace =F1place
		return	Tplace	
	def factor():
		'<FACTOR> ::= CONSTANT |'
		'		(<EXPRESSION>) |'
		'		ID <IDTAIL>		'
		global token
		
		if(token[1]==2):							#Constant
			fact = token[0]							#save string-part of lektikh monada.
			token=lex()
		elif(token[0]=='('):
			token=lex()
			Eplace =expression()
			if(token[0]==')'):
				fact = Eplace						#save string-part of lektikh monada.
				token=lex()
			else:
				print('error: Expected ")" after expression. \tLine> %d:%d' % (line, position))
				exit(1)
		elif(token[1]==1):							#ID(anagnwristiko)
			fact=token[0]
			token=lex()
			idTail(fact)
		else:
			print('error: Expected constant or (expression) or variable, before "%s". \tLine> %d:%d' % (token[0], line, position))
			exit(1)
		return fact	
	def idTail(idName):
		'<IDTAIL> ::= e | <ACTUALPARS>'
		global token, isFuncFlag

		if(token[0]=='('):				#Token of actualPars is '('
			isFuncFlag = 1
			actualPars(1, idName)				# 1 -> it is function
			return
	def actualPars(isFunctionFlag, idName):
		'<ACTUALPARS> ::= ( e | <ACTUALPARLIST> )'
		global token
		global temp

		if(token[0]=='('):
			token=lex()		
			actualParList()
			if(token[0]==')'):
				token=lex()
				#If its function:
				if(isFunctionFlag==1):
					w=newTemp()
					genQuad('par', w, 'RET', '_')
					genQuad('call', idName, '_', '_')
					
					temp=w
				#If its procedure:
				else:
					genQuad('call', idName, '_', '_')
			else:
				print('error: Expected ")". \tLine> %d:%d' % (line, position))
				exit(1)
		return		
	def actualParList():
		'<ACTUALPARLIST> ::= <ACTUALPARITEM> ( , <ACTUALPARITEM> )*'
		global token
		
		actualParItem()
		while(token[0]==','):
			token=lex()
			actualParItem()
		return		
	def actualParItem():
		'<ACTUALPARITEM> ::= in <EXPRESSION> | inout ID'
		global token
		
		if(token[0]=='in'):
			token=lex()
			thisExpression =expression()
			genQuad('par', thisExpression, 'CV', '_')
		elif(token[0]=='inout'):
			token=lex()
			if(token[1]==1):							#ID(anagnwristiko)
				genQuad('par', token[0], 'REF', '_')
				token=lex()
			else:
				print('error: Expected variable (ID). \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "in" or "inout". \tLine> %d:%d' % (line, position))
			exit(1)
		return
	def mulOper():
		'<MUL-OPER> ::= * | /'
		global token
		
		if(token[0]=='*' or token[0]=='/'):
			oper =token[0]
			token=lex()
		return oper	
	def ifStat():
		'<IF-STAT> ::= if (<CONDITION>) <BRACK-OR-STAT> <ELSEPART>'
		'''
			IS-> if C then {P1} BOS {P2} else() {P3}
		'''
		global token
		
		#Tha yparxei panta token=if, alliws den tha mbei mesa sthn IfStat().
		token=lex()
		if(token[0]=='('):
			token=lex()
			C =condition()								#returns 2 lists (list of true & false), as tuples.		
			if(token[0]==')'):
				token=lex()
				#{P1}:
				backPatch(C[0], nextQuad())				#C[0] is list of true.
				brackOrStat()
				#{P2}:
				ifList = makeList(nextQuad())
				genQuad('JUMP', '_', '_', '_')
				backPatch(C[1], nextQuad())				#C[1] is list of false.
				elsePart()
				#{P3}:
				backPatch(ifList, nextQuad())
			else:
				print('error: Expected ")" after condition. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "(" after "if". \tLine> %d:%d' % (line, position))
			exit(1)
		IStrue = C[0]
		ISfalse= C[1]
		return IStrue, ISfalse		
	def elsePart():
		'<ELSEPART> ::= e | else <BRACK-OR-STAT>'
		global token
		
		if(token[0]=='else'):
			token=lex()
			brackOrStat()
		return
	def doWhileStat():
		'<DO-WHILE-STAT> ::= do <BRACK-OR-STAT> while (<CONDITION>)'
		'''
			DWS-> do {P1} BOS while (C {P2})
		'''
		global token, inDoWhileFlag, exitFlag
		inDoWhileFlag =1				#flag takes value.
		
		#{P1}:
		toDoJumpHere=nextQuad()
		
		token=lex()
		brackOrStat()
		#break do-while when exit called.
		if(exitFlag==1):
			return
		if(token[0]=='while'):
			token=lex()
			if(token[0]=='('):
				token=lex()
				C =condition()							#returns 2 lists (list of true & false), as tuples.
				#{P2}:
				backPatch(C[0], toDoJumpHere)			#C[0] is list of true.
				backPatch(C[1], nextQuad())				#C[1] i slist of false.
				if(token[0]==')'):
					token=lex()
					return
				else:
					print('error: Expected ")" to close while loop. \tLine> %d:%d' % (line, position))
					exit(1)
			else:
				print('error: Expected "(" to open while loop. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "while()". \tLine> %d:%d' % (line, position))
			exit(1)
		DWStrue	= C[0]
		DWSfalse= C[1]
		return DWStrue, DWSfalse	
	def whileStat():
		'<WHILE-STAT> ::= while (<CONDITION>) <BRACK-OR-STAT>'
		'''
			WS-> while ({P1} C) {P2} BOS {P3}
		'''
		global token

		token=lex()
		if(token[0]=='('):
			token=lex()
			#{P1}:
			Cquad=nextQuad()
			C =condition()								#returns 2 lists (list of true & false), as tuples.		
			if(token[0]==')'):
				#{P2}:
				backPatch(C[0], nextQuad())				#C[0] is list of true.

				token=lex()
				brackOrStat()
				
				#{P3}:
				genQuad('JUMP', '_', '_', Cquad)
				backPatch(C[1], nextQuad())				#C[1] is list of false.
			else:
				print('error: Expected ")" to close while loop. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "(" to open while loop. \tLine> %d:%d' % (line, position))
			exit(1)
		WStrue = C[0]
		WSfalse = C[1]
		return	WStrue, WSfalse	
	def selectStat():
		'<SELECT-STAT> ::= select (ID)				 '
		'					(CONST: <BRACK-OR-STAT>)*'
		'					DEFAULT: <BRACK-OR-STAT> '
		'''
			{P0} select (ID)
				1: {P1} {}	{P2}
				2: {P1} {}	{P2}
				 ...
				default: {}  {P3}
		'''
		global token
		i=0
		choice=0
		
		#{P0}
		exitList=emptyList()
		
		token=lex()
		if(token[0]=='('):
			token=lex()
			if(token[1]==1):						#ID(anagnwristiko)
				choice=token[0]						#Save selection ID	unnecessary for now..
				token=lex()
				if(token[0]==')'):
					token=lex()
					while(token[0]!='default'):
						i+=1
						if(token[1]==2):			#Number needed as constant.
							if(int(token[0])==i):	#Numbers in row 1,2,3...
								token=lex()
								if(token[0]==':'):
									#{P1}
									Elist = makeList(nextQuad())
									genQuad('<>', choice, i, '_')
									
									token=lex()
									brackOrStat()
									
									backPatch(Elist, nextQuad())
									#{P2}
									eList = makeList(nextQuad())
									genQuad('JUMP', '_', '_', '_')
									exitList = merge(exitList, eList)
									backPatch(exitList, nextQuad())
								else:
									print('error: Expected ":" after "%d". \tLine> %d:%d' % (i, line, position))
									exit(1)
							else:
								print('error: Expected next number in row, "%d" or "default". \tLine> %d:%d' % (i, line, position))
								exit(1)
						else:
							print('error: Expected number "%d" or "default" at next selection case, \n\tinstead of "%s". \tLine> %d:%d' % (i, token[0], line, position))
							exit(1)
					if(token[0]=='default'):
						token=lex()
						if(token[0]==':'):
							token=lex()
							brackOrStat()
							#{P3}
							backPatch(exitList, nextQuad())
							return
						else:
							print('error: Expected ":" after "default". \tLine> %d:%d' % (line, position))
							exit(1)					
				else:
					print('error: Expected ")" after variable of selection before "%s", \n\tor select case number. \tLine> %d:%d' % (token[0], line, position))
					exit(1)
			else:
				print('error: Expected variable of selection after "(". \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "(" after "select". \tLine> %d:%d' % (line, position))
			exit(1)
	def exitStat():
		'<EXIT-STAT> ::= exit'
		global token, inDoWhileFlag, exitFlag
		exitFlag=0
		
		token=lex()
		if(inDoWhileFlag==1):
			exitFlag=1
		return	
	def returnStat():
		'<RETURN-STAT> ::= return (<EXPRESSION>)'
		'Use inside functions to return the result of function.'
		'''
			RS-> return (E) {P1}
		'''
		global token, atLeastOneReturn
		
		atLeastOneReturn=1
		
		token=lex()
		if(token[0]=='('):
			token=lex()
			Eplace =expression()
			if(token[0]==')'):
				token=lex()
				#{P1}:
				genQuad('retv', Eplace, '_', '_')
			else:
				print('error: Expected ")". \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "(" after "return". \tLine> %d:%d' % (line, position))
			exit(1)
		return	
	def printStat():
		'<PRINT-STAT> ::= print (<EXPRESSION>)'
		'''
			PS-> print (E) {P2}
		'''
		global token
		
		token=lex()
		if(token[0]=='('):
			token=lex()
			Eplace =expression()
			if(token[0]==')'):
				token=lex()
				#{P2}:
				genQuad('out', Eplace, '_', '_')
			else:
				print('error: Expected ")". \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			print('error: Expected "(" after "print". \tLine> %d:%d' % (line, position))
			exit(1)
		return	
	def callStat():
		'<CALL-STAT> ::= call ID <ACTUALPARS>'
		'p.x. call function_name(actual_parameters)'
		'Xrhsimopoieitai mesa se synarthseis gia na epistrafei to apotelesma ths synarthshs.'
		global token

		token=lex()
		if(token[1]==1):									#ID(anagnwristiko)
			token=lex()
			idName = token[0]
			actualPars(0, idName)							#0 means its not inside a function
			return
		else:
			print('error: Expected function_name. \tLine> %d:%d' % (line, position))
			exit(1)	
	def condition():
		'<CONDITION> ::= <BOOLTERM> (or <BOOLTERM>)*'
		'''
			C-> BT1 {P1} (or {P2} BT2 {P3})*
		'''
		global token
		Ctrue, Cfalse = [], []
		
		BT1 =boolTerm()								#returns 2 lists (list of true & false), as tuples.
		#{P1}:
		Ctrue = BT1[0]								#BT1[0] is list of true.
		Cfalse = BT1[1]								#BT1[1] is list of false.
		
		while(token[0]=='or'):
			token=lex()
			#{P2}:
			backPatch(Cfalse, nextQuad())

			BT2 =boolTerm()							#returns 2 lists (list of true & false), as tuples.
			#{P3}:
			Ctrue = merge(Ctrue, BT2[0])			#BT2[0] is list of true.
			Cfalse = BT2[1]							#BT2[1] is list of false.
		return	Ctrue, Cfalse	
	def boolTerm():
		'<BOOLTERM> ::= <BOOLFACTOR> (and <BOOLFACTOR>)*'
		'''
			BT-> BF1 {P1} (and {P2} BF2 {P3})*
		'''
		global token
		BTtrue, BTfalse = [], []
		
		BF1 =boolFactor()							#returns 2 lists (list of true & false), as tuples.
		#{P1}:
		BTtrue = BF1[0]								#BF1[0] is list of true.
		BTfalse = BF1[1]							#BF1[1] is list of false.
		
		while(token[0]=='and'):
			token=lex()
			#{P2}:
			backPatch(BTtrue, nextQuad())
			
			BF2 =boolFactor()						#returns 2 lists (list of true & false), as tuples.
			#{P3}:
			BTfalse = merge(BTfalse, BF2[1])		#BF2[1] is list of false.
			BTtrue = BF2[0]							#BF2[0] is list of true.
		return	BTtrue, BTfalse	
	def boolFactor():
		'<BOOLFACTOR> ::= not [<CONDITION>] |							'
		'				  [<CONDITION>] |								'
		'				  <EXPRESSION> <RELATIONAL-OPER> <EXPRESSION>	'
		global token
		BFtrue, BFfalse = [], []
		Eplace1, Eplace2, relop = '', '', ''
		
		if(token[0]=='not'):
			'''
				BF-> not [C] {P1}
			'''
			token=lex()
			if(token[0]=='['):
				token=lex()
				C =condition()						#returns 2 lists (list of true & false), as tuples.				
				if(token[0]==']'):
					token=lex()
					#{P1}:
					BFtrue = C[1]					#C[1] is list of false.
					BFfalse = C[0]					#C[0] is list of true.
				else:
					print('error: Expected "]" after condition. \tLine> %d:%d' % (line, position))
					exit(1)
			else:
				print('error: Expected "[" after "not". \tLine> %d:%d' % (line, position))
				exit(1)
		elif(token[0]=='['):
			'''
				BF-> [C] {P1}
			'''
			token=lex()
			C =condition()							#returns 2 lists (list of true & false), as tuples.
			if(token[0]==']'):
				token=lex()
				#{P1}:
				BFtrue = C[0]						#C[0] is list of true.
				BFfalse = C[1]						#C[1] is list of false.
			else:
				print('error: Expected "]" after condition. \tLine> %d:%d' % (line, position))
				exit(1)
		else:
			'''
				BF-> E1 relop E2 {P1}
			'''
			Eplace1 =expression()	
			#print(Eplace1)
			relop =relationalOper()
			#print(relop)
			Eplace2 =expression()
			
			#{P1}:
			BFtrue=makeList(nextQuad())
			genQuad(relop, Eplace1, Eplace2, '_')	#will be backPatched later on.
			BFfalse=makeList(nextQuad())
			genQuad('JUMP', '_', '_', '_')			#will be backPatched later on.
		return BFtrue, BFfalse	
	def relationalOper():
		'<RELATIONAL-OPER> ::= = | < | <= | <> | >= | >'
		global token
		
		if(token[0]=='=' or token[0]=='<' or token[0]=='<=' or token[0]=='<>' or token[0]=='>=' or token[0]=='>'):
			relop = token[0]						#save string-part of lektikh monada.
			token=lex()
		else:
			print('error: Missing = or < or <= or <> or >= or >. \tLine> %d:%d' % (line, position))
			exit(1)
		return relop

	program()
	print(' \n ________________')
	print('*_____OK_END_____*')


def intCode(intF):
	'Write listOfAllQuads at intFile.int'
	for i in range(len(listOfAllQuads)):
		quad = listOfAllQuads[i]
		intF.write(str(quad[0]))
		intF.write(":  ")
		intF.write(str(quad[1]))
		intF.write("  ")
		intF.write(str(quad[2]))
		intF.write("  ")
		intF.write(str(quad[3]))
		intF.write("  ")
		intF.write(str(quad[4]))
		intF.write("\n")
		
def cCode(cF):
	global listOfTempVariables
	
	if(len(listOfTempVariables)!=0):
		cF.write("int ")
	#Temp_i variables.
	for i in range(len(listOfTempVariables)):
		cF.write(listOfTempVariables[i])
		if(len(listOfTempVariables) == i+1):
			cF.write(";\n\n\t")
		else:
			cF.write(",")
	
	for j in range(len(listOfAllQuads)):
		if(listOfAllQuads[j][1] == 'begin_block'):
			cF.write("L_"+str(j+1)+":\n\t")
		elif(listOfAllQuads[j][1] == ":="):
			cF.write("L_"+str(j+1)+": "+ listOfAllQuads[j][4]+"="+listOfAllQuads[j][2]+";\n\t")
		elif(listOfAllQuads[j][1] == "+"):
			cF.write("L_"+str(j+1)+": "+ listOfAllQuads[j][4]+"="+listOfAllQuads[j][2]+"+"+listOfAllQuads[j][3]+";\n\t")
		elif(listOfAllQuads[j][1] == "-"):
			cF.write("L_"+str(j+1)+": "+ listOfAllQuads[j][4]+"="+listOfAllQuads[j][2]+"-"+listOfAllQuads[j][3]+";\n\t")
		elif(listOfAllQuads[j][1] == "*"):
			cF.write("L_"+str(j+1)+": "+ listOfAllQuads[j][4]+"="+listOfAllQuads[j][2]+"*"+listOfAllQuads[j][3]+";\n\t")
		elif(listOfAllQuads[j][1] == "/"):
			cF.write("L_"+str(j+1)+": "+ listOfAllQuads[j][4]+"="+listOfAllQuads[j][2]+"/"+listOfAllQuads[j][3]+";\n\t")
		elif(listOfAllQuads[j][1] == "JUMP"):
			cF.write("L_"+str(j+1)+": "+"goto L_"+str(listOfAllQuads[j][4])+ ";\n\t")
		elif(listOfAllQuads[j][1] == "<"):
			cF.write("L_"+str(j+1)+": "+"if ("+listOfAllQuads[j][2]+"<"+listOfAllQuads[j][3]+") goto L_"+str(listOfAllQuads[j][4])+";\n\t")
		elif(listOfAllQuads[j][1] == ">"):
			cF.write("L_"+str(j+1)+": "+"if ("+listOfAllQuads[j][2]+">"+listOfAllQuads[j][3]+") goto L_"+str(listOfAllQuads[j][4])+";\n\t")
		elif(listOfAllQuads[j][1] == ">="):
			cF.write("L_"+str(j+1)+": "+"if ("+listOfAllQuads[j][2]+">="+listOfAllQuads[j][3]+") goto L_"+str(listOfAllQuads[j][4])+";\n\t")
		elif(listOfAllQuads[j][1] == "<="):
			cF.write("L_"+str(j+1)+": "+"if ("+listOfAllQuads[j][2]+"<="+listOfAllQuads[j][3]+") goto L_"+str(listOfAllQuads[j][4])+";\n\t")
		elif(listOfAllQuads[j][1] == "<>"):
			cF.write("L_"+str(j+1)+": "+"if ("+str(listOfAllQuads[j][2])+"!="+str(listOfAllQuads[j][3])+") goto L_"+str(listOfAllQuads[j][4])+";\n\t")
		elif(listOfAllQuads[j][1] == "="):
			cF.write("L_"+str(j+1)+": "+"if ("+listOfAllQuads[j][2]+"=="+listOfAllQuads[j][3]+") goto L_"+str(listOfAllQuads[j][4])+";\n\t")
		elif(listOfAllQuads[j][1] == "out"): #print to apotelesma tou expression.
			cF.write("L_"+str(j+1)+": "+"printf(\""+listOfAllQuads[j][2]+"= %d\", "+listOfAllQuads[j][2]+");\n\t")
		elif(listOfAllQuads[j][1] == 'halt'):
			cF.write("L_"+str(j+1)+": {}\n\t")
			
def files():
	'intFile.int & cFile.c'
	#Open files to write
	intFile = open('intFile.int', 'w')
	cFile = open('cFile.c', 'w')
	ascFile = open('asciiFile.asm','w')
	cFile.write("int main(){\n\t")

	syntaktikosAnalyths(cFile)
	intCode(intFile)
	cCode(cFile)
	final(ascFile)
	cFile.write("\n}")
	
	#Close open files
	cFile.close()
	intFile.close()
	ascFile.close()
files()

def print_listOfAllQuads():
	'Prints listOfAllQuads'
	for i in range(len(listOfAllQuads)):
		print (str(listOfAllQuads[i][0])+" "+listOfAllQuads[i][1]+" "+listOfAllQuads[i][2]+" "+listOfAllQuads[i][3]+" "+listOfAllQuads[i][4])
#print_listOfAllQuads()




#loadvr('var1',1)
#final()



	
	
	
	
	
	
	
