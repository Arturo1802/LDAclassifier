import csv
 
from translating import traducir_linea 
with open('cleanfulldb.csv',"w", newline='') as clean: 
	writer=csv.writer(clean, delimiter=',')
	print("-----------::::::::_-------------")
	with open('bd.csv', newline='', encoding="cp1252") as db: 
		reader = csv.reader(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, doublequote=True)
		line = 0
		for row in reader: 
			#row.pop(-1) #Extra data in csv was removed
			if line == 0:
				print(f'Columnas: {", ".join(row)}')
				line += 1
				writer.writerow(row)
				continue  
			for i in range(7):
				if i ==1  :					
					row[i]=traducir_linea(row[i].replace("Traducción realizada con la versión gratuita del traductor www.DeepL.com/Translator"," ").strip().replace("     ",""))
				if i >1: 
					if "y" in row[i]:
						row[i] = 1		
					elif "n" in row[i]:
						row[i] = 0
				#print(row)
			writer.writerow(row)
			line += 1
 