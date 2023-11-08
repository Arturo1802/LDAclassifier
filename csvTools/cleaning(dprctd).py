import csv
 
from translating import traducir_linea 		
import subprocess
comando = "libretranslate"
resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

with open('cleandb.csv',"w", newline='') as clean:
	writer=csv.writer(clean, delimiter=',') 
	with open('db.csv', newline='', encoding="cp1252") as db:
		reader = csv.reader(db, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, doublequote=True)
		line = 0
		for row in reader: 
			#row.pop(-1) #Extra data in csv was removed
			if line == 0:
				print(f'Columnas: {", ".join(row)}')
				line += 1
				writer.writerow(row)
				continue  
			if line==0 or line >=2 and (line - 2) % 5 == 0:
			
				for i in range(7):
					if i ==1  :					
						row[i]=traducir_linea(row[i].replace("Traducción realizada con la versión gratuita del traductor www.DeepL.com/Translator"," ").strip().replace("	 ",""))
					if i >1: 
						if "y" in row[i]:
							row[i] = 1
							
						elif "n" in row[i]:
							row[i] = 0
				#print(row)
				writer.writerow(row)
			line += 1
if resultado.returncode == 0:
	print("Comando ejecutado exitosamente.")
else:
	print("Error al ejecutar el comando. Código de salida:", resultado.returncode)