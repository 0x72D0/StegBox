from subprocess import Popen, PIPE

class Convertir():

	def __init__(self, pixel):
		self.pixel = pixel
		self.flagType = raw_input("Flag type (ex. FLAG, ex. tjctf) > ")
		#self.flagType = "tjctf"

	###########################################
	## Effectue tout les tests
	def examineAll(self):
		process = Popen(['toilet',"-f","future","Basic Test"], stdout=PIPE, stderr=PIPE)
		(output, err) = process.communicate()
		print "\n\n"+output
		print "Conversion ascii... "
		print "RGB : "+self.lookForFlag(self.pixel2Ascii(0), self.flagType)+" R : "+self.lookForFlag(self.pixel2Ascii(1), self.flagType)+" G : "+self.lookForFlag(self.pixel2Ascii(2), self.flagType)+" B : "+self.lookForFlag(self.pixel2Ascii(3), self.flagType)
		print "Conversion octal..."
		print "RGB : "+self.lookForFlag(self.pixel2Octal(0), self.flagType)+" R : "+self.lookForFlag(self.pixel2Octal(1), self.flagType)+" G : "+self.lookForFlag(self.pixel2Octal(2), self.flagType)+" B : "+self.lookForFlag(self.pixel2Octal(3), self.flagType)
		print "Conversion binaire..."
		print "RGB : "+self.lookForFlag(self.pixel2Binary(0), self.flagType)+" R : "+self.lookForFlag(self.pixel2Binary(1), self.flagType)+" G : "+self.lookForFlag(self.pixel2Binary(2), self.flagType)+" B : "+self.lookForFlag(self.pixel2Binary(3), self.flagType)
		print "Conversion LSB..." 
		print "RGB : "+self.lookForFlag(self.LSB(0), self.flagType)+" R : "+self.lookForFlag(self.LSB(1), self.flagType)+" G : "+self.lookForFlag(self.LSB(2), self.flagType)+" B : "+self.lookForFlag(self.LSB(3), self.flagType)	



	###########################################
	## Imprime les pixels de l'image
	def rawPixel(self):
		for i in self.pixel:
			print i


	###########################################
	## Converti les pixels en ascii
	def pixel2Ascii(self, position):
		if position == "" : position = self.position()
		a = ""	
		for i in self.pixel:
			if position == 0: a+= chr(i[0])+chr(i[1])+chr(i[2])
			if position == 1: a+= chr(i[0])
			if position == 2: a+= chr(i[1])
			if position == 3: a+= chr(i[2])
		return a	


	###########################################
	## Converti les pixels en octal
	def pixel2Octal(self, position):
		if position == "" : position = self.position()
		a = ""
		for i in self.pixel:
			try : 
				if position == 0: a+=chr(int(str(i[0]),8))+chr(int(str(i[1]),8))+chr(int(str(i[2]),8))		
				if position == 1: a+=chr(int(str(i[0]),8))
				if position == 2: a+=chr(int(str(i[1]),8))
				if position == 3: a+=chr(int(str(i[2]),8))
			except : er = 1
		return a


	###########################################
	## Converti les pixels en binaire
	def pixel2Binary(self, position):
		if position == "" : position = self.position()
		a = ""
		for i in self.pixel:
			if position == 0: a+=''.join('{:08b}'.format(ord(c)) for c in chr(i[0]))+''.join('{:08b}'.format(ord(c)) for c in chr(i[1]))+''.join('{:08b}'.format(ord(c)) for c in chr(i[2]))
			if position == 1: a+=''.join('{:08b}'.format(ord(c)) for c in chr(i[0]))
			if position == 2: a+=''.join('{:08b}'.format(ord(c)) for c in chr(i[1]))
			if position == 3: a+=''.join('{:08b}'.format(ord(c)) for c in chr(i[2]))
		return ''.join((chr(int(a[i:i+8], 2)) for i in range(0, len(a), 8)))


	###########################################
	## Cherche les LSB des pixels 
	def LSB(self, position):
		if position == "" : position = self.position()
		a = ""
		for i in self.pixel:
			if position == 0: a+=bin(i[0])[-1]+bin(i[1])[-1]+bin(i[2])[-1]
			if position == 1: a+=bin(i[0])[-1]
			if position == 2: a+=bin(i[1])[-1]
			if position == 3: a+=bin(i[2])[-1]
		return ''.join((chr(int(a[i:i+8], 2)) for i in range(0, len(a), 8)))


	###########################################
	## Converti deux couleurs en binaires
	def color2Bin(self, flagType):
		a = ""
		color0 = raw_input("Valeur du pixel considere comme 0 : ")
		color1 = raw_input("Valeur du pixel consiedere comme 1 : ")
		position = raw_input("Position R(0) G(1) B(2) A(3) : ")
		binary=""
		for i in self.pixel:
			if i[position] == int(color0):
				binary+="1"
			if i[position] == int(color1):
				binary+="1"
			else : binary+="0"
		a =  ''.join((chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)))
		return a
		self.lookForFlag(a, self.flagType)


	###########################################
	## Verifie si un FLAG est present
	def lookForFlag(self, pixel, flagType):
		if pixel.find(flagType)!=-1 : return pixel[pixel.find(flagType):pixel.find(flagType)+30]
		else : return "None"


	###########################################
	## Position de conversion
	def position(self):
		valide = False
		while valide == False :
			valide = True 
			print "Convertir pour R, G, B ou RGB ?"
			choix = raw_input("ffffffroze> ").upper()
			if choix == "RGB" : return 0
			elif choix == "R" : return 1
			elif choix == "G" : return 2
			elif choix == "B" : return 3
			else : 
				print "Invalide"
				valide = False




