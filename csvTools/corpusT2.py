import csv
 
from translating import traducir_linea 
with open('./csvTools/corpusT2.csv',"w", newline='') as clean: 
	print("---------")
	writer=csv.writer(clean, delimiter=',')
	with open('./csvTools/cleanfulldb.csv', newline='') as db: 
		reader = csv.reader(db, delimiter=',')
		line = 0 
		for row in reader:   
			if line == 0:
				print(f'Columnas: {", ".join(row)}')
				line += 1
				writer.writerow(row)
				continue  
			if line==0 or line >=2 and (line - 2) % 5 == 0:
				writer.writerow(row)
			line += 1
 