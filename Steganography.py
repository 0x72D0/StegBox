from PIL import Image
from subprocess import Popen, PIPE
from Convertir import Convertir

###################
## Main
def main():
	try:
		process = Popen(['toilet',"-f","bigmono9","-F","gay","ffffroze"], stdout=PIPE, stderr=PIPE)
		(output, err) = process.communicate()
		print output
	except : print "Please install Toilet :3  (apt-get install toilet)" 	
	fichier = raw_input("Open Image > ")
	#fichier = "cur.png"	
	im = Image.open(fichier,'r')
	conv = Convertir(Image.open(fichier,'r').getdata())	
	
	conv.examineAll()
	runTools(fichier)
	
	choix = ""
	while choix != "z":
		print "Please choose an option"
		print "==========================================================="
		print "1 - View pixels"
		print "2 - Ascii"
		print "3 - Octal"
		print "4 - Binary"
		print "5 - LSB"
		print "6 - Conversion de 2 couleurs en binaires"
		print "z - Exit\n"

		choix = raw_input("ffffffroze> ")
		if choix=="1":print conv.rawPixel()
		if choix=="2":print conv.pixel2Ascii("")
		if choix=="3":print conv.pixel2Octal("")
		if choix=="4":print conv.pixel2Binary("")
		if choix=="5":print conv.LSB("")
		if choix=="6":print conv.color2Bin("")			
	

###################
## extern tool
def runTools(fichier):
	#Binwalk 
	process = Popen(['toilet',"-f","future","binwalk"], stdout=PIPE, stderr=PIPE)
	(output, err) = process.communicate()
	print "\n\n"+output
	process = Popen(['binwalk',fichier], stdout=PIPE, stderr=PIPE)
	(output, err) = process.communicate()
	print output
	
	#pngcheck     -v ??????????
	process = Popen(['toilet',"-f","future","pngcheck"], stdout=PIPE, stderr=PIPE)
	(output, err) = process.communicate()
	print "\n\n"+output
 	process = Popen(['pngcheck',fichier], stdout=PIPE, stderr=PIPE)
	(output, err) = process.communicate()
	print output

	process = Popen(['toilet',"-f","future","Menu"], stdout=PIPE, stderr=PIPE)
	(output, err) = process.communicate()
	print "\n\n"+output
	#print base64.b64decode(a)
	#IMAGE XOR
	#nouveleimage
	#ALPHA!!!!


if __name__ == '__main__':
	main()
