import os

# genereer de winnende combinaties
def genereerCombinaties():
	arrCombinaties = []

	for y in xrange(0, 3):
		# links naar rechts
		arrCombinaties.append([(y * 3) + x for x in xrange(0, 3)])

		# boven naar onder
		arrCombinaties.append([(x * 3) + y for x in xrange(0, 3)])

	# diagonaal, met stappen van 3 (links>rechts) en 4 (rechts>links)
	arrCombinaties.append([0, 4, 8])
	arrCombinaties.append([2, 4, 6])

	return arrCombinaties

arrCombinaties = genereerCombinaties()

# clear de console
def schoon():
    os.system('cls' if os.name=='nt' else 'clear')

# vul het scherm met het huidige bord
def maakBord():
	
	for y in xrange(0,3):
		strPrint = ""

		for x in xrange(0,3):
			strPrint += "[" + arrZetten[((y * 3) + x)] + "]"

		strPrint += " || [" + str((y * 3) + 1) + " - " + str((y * 3) + x + 1) + "]"
		print strPrint

# laat de AI een zet doen
def zetComputer():
	global arrCombinaties
	global arrZetten

	blnActiefBlokken = True # Zet uit als je ook eens wilt winnen
	blnZetGedaan = False

	if blnActiefBlokken:
		# moet er geblocked worden? (als de player de volgende zet kan winnen)
		for arrCombinatie in arrCombinaties:
			strVorige = ""
			intPositieOver = "";
			intHoeVer = 0

			for intPositie in arrCombinatie:
				strWaarde = arrZetten[intPositie].strip()
				if(strWaarde == "X"):
					intHoeVer += 1
				elif strWaarde == "":
					intPositieOver = intPositie

				strVorige = strWaarde

			if intHoeVer == 2:
				if intPositieOver != "" and not blnZetGedaan:
					arrZetten[intPositieOver] = "0"
					blnZetGedaan = True
					break

	# de beste zet uitzoeken
	intPositieScoreVorig = 0
	intBesteZet = 0
	if not blnZetGedaan:
		for intPositie in xrange(0,9):
			if arrZetten[intPositie].strip() == "":
				intPositieScore = getPositieScore("0", intPositie)

				if intPositieScore > intPositieScoreVorig:
					intBesteZet = intPositie
					intPositieScoreVorig = intPositieScore

		arrZetten[intBesteZet] = "0"
		blnZetGedaan = True

	pass

def getPositieScore(f_strSpeler, f_intPositie):
	global arrCombinaties

	intAlBezig = 0
	intMogelijkeCombi = 0
	intBlock = 0

	for arrCombinatie in arrCombinaties:
		strVorige = ""
		blnMogelijkeCombi = True

		# alleen rekenen als de positie in de combinatie voorkomt
		if f_intPositie in arrCombinatie:

			for intPositie in arrCombinatie:
				strWaarde = arrZetten[intPositie].strip()
				if strWaarde == f_strSpeler and isNogMogelijk("0", arrCombinatie):
					intAlBezig += 1
				
				if isNogMogelijk("0", arrCombinatie):
					intMogelijkeCombi += 1

				if isBlockOp("X", intPositie):
					#print str(f_intPositie) + " is een block op: " + str(intPositie)
					intBlock += 1

				strVorige = strWaarde

	return intMogelijkeCombi + intAlBezig + intBlock


def isNogMogelijk(f_strSpeler, f_arrCombinatie):
	global arrCombinaties

	blnIsAlGeblocked = False

	for intPositie in f_arrCombinatie:
		strWaarde = arrZetten[intPositie].strip()

		if strWaarde != f_strSpeler and strWaarde != "":
			blnIsAlGeblocked = True
		
	if blnIsAlGeblocked:
		return False
	else:
		return True

def isBlockOp(f_strSpeler, f_intPositie):
	global arrCombinaties

	blnIsBlock = False

	for arrCombinatie in arrCombinaties:

		blnIsAlGeblocked = False
		blnBlockTemp = False

		if f_intPositie in arrCombinatie:
			for intPositie in arrCombinatie:
				strWaarde = arrZetten[intPositie].strip()

				if strWaarde != f_strSpeler and strWaarde != "":
					blnIsAlGeblocked = True
				elif strWaarde == f_strSpeler:
					blnBlockTemp = True
			
			if blnIsAlGeblocked:
				blnBlockTemp = False

			if blnBlockTemp:
				blnIsBlock = True

	return blnIsBlock

# heeft er iemand gewonnen?
def checkWin():
	global arrCombinaties

	for arrCombinatie in arrCombinaties:
		strVorige = ""
		blnGewonnen = True

		for intPositie in arrCombinatie:
			strWaarde = arrZetten[intPositie].strip()
			if(strVorige != "" and strWaarde != strVorige or strWaarde == ""):
				blnGewonnen = False

			strVorige = strWaarde

		if blnGewonnen:
			print strWaarde + " heeft gewonnen"
			global blnGameOver
			blnGameOver = True


# is het gelijk spel?
def checkGelijk():
	global arrCombinaties

	blnMogelijkheid = False

	for arrCombinatie in arrCombinaties:
		
		if isNogMogelijk("X", arrCombinatie):
			blnMogelijkheid = True
			#print "X kan winnen via: " + str([x+1 for x in arrCombinatie])

		if isNogMogelijk("0", arrCombinatie):
			blnMogelijkheid = True
			#print "0 kan winnen via: " + str([x+1 for x in arrCombinatie])

		if blnMogelijkheid:
			break

	if not blnMogelijkheid:
		print "gelijk spel :("
		global blnGameOver
		blnGameOver = True			


# reset de zetten die gedaan zijn
def resetZetten():
	f_arrZetten = []
	for x in xrange(0, 9):
		f_arrZetten.append(1)
		#f_arrZetten[x] = ("0" + str(x+1))[-2:]
		f_arrZetten[x] = " "
		
	return f_arrZetten

arrZetten = resetZetten()

# Eerste zet door PC
#zetComputer()

schoon()
maakBord()
blnGameOver = False


while True:
	if not blnGameOver:
		# wacht op input
		strInput = raw_input("Voer 1-9 in om een X op het veld te zetten: ")

		if(strInput.isdigit()):
			if int(strInput) <= 9:
				# is daar nog ruimte?
				if arrZetten[int(strInput)-1].strip() == "":
					arrZetten[int(strInput)-1] = "X"
					# vul het scherm, check winnaar, laat de AI een zet doen, en check opnieuw op een winnaar.
					schoon()
					maakBord()
					checkWin()
					if not blnGameOver:
						zetComputer()
						schoon()
						maakBord()
						checkWin()
						checkGelijk()

				else:
					schoon()
					print "Die is al bezet"
					maakBord()
			else:
				schoon()
				print "Voer een nummer onder de 26 in"
				maakBord()	
		else:
			schoon()
			print "Voer een nummer in"
			maakBord()

	else:
		# eventueel nieuw spel starten
		strInput = raw_input("Opnieuw spelen? J/N: ")

		if strInput.upper() == "J":
			arrZetten = resetZetten()
			blnGameOver = False
			schoon()
			maakBord()
		elif strInput.upper() == "N":
			break

	pass
