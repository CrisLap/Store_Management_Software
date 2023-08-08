# Qui raccolgo tutte le funzioni che utilizzo nel software di gestione dello shop.


import csv
import os
from datetime import datetime



def help_cmd():

  """
  Funzione che stampa un messaggio di aiuto con informazioni sui comandi da utilizzare per l'esecuzione del programma.
  """
  
  print("\nI comandi disponibili sono i seguenti:\n"+
        "aggiungi: aggiungi un prodotto al magazzino\n"+
        "elenca: elenca i prodotti in magazzino\n"+
        "vendita: registra una vendita effettuata\n"+
        "profitti: mostra i profitti totali\n"+
        "aiuto: mostra i possibili comandi\n"+
        "chiudi: esci dal programma")

    





def stock_info():

  """
Funzione che genera la situazione puntuale delle scorte, partendo dal file .csv in cui sono registrati i prodotti acquistati e venduti.

  Viene letto il file 
  1-file Magazzino.csv, creato con il primo prodotto acquistato, viene letto. Ogni riga (corrispondente a un prodotto acquistato o venduto) viene registrata in un elenco di dizionari
  2-l'elenco dei dizionari viene modificato: per ogni prodotto, viene controllata la presenza dello stesso nei dizionari precedenti. 
    Se esiste, la sua quantità viene aggiunta al dizionario precedente.
  3-solo la prima occorrenza per ogni prodotto contiene ora la giusta quantità totale, le altre righe vengono cancellate: la lista finale dei dizionari corrisponde allo stock
  4-la funzione restituisce tmp: la chiave è il prodotto, il suo valore è un dizionario con le seguenti informazioni: quantità, prezzo d'acquisto e prezzo di vendita 
  """
  
  with open("Magazzino.csv","r") as csv_file:        
        csv_reader=csv.DictReader(csv_file)
        list_dict=[]
        for row in list(csv_reader):
            list_dict.append(row)

        for i,line in enumerate(list_dict):
            prev_lines=[]
            for j in range(i):
                prev_lines.append(list_dict[j]["PRODOTTO"])
            for k,prev_line in enumerate(prev_lines):
                if line["PRODOTTO"]==prev_line:
                    list_dict[k]["QUANTITA'"]=int(list_dict[k]["QUANTITA'"])+int(line["QUANTITA'"])
                else:
                    continue

        tmp={}           
        for i,row in enumerate(list_dict):
            prev_lines=[]
            for j in range(i):
                prev_lines.append(list_dict[j]["PRODOTTO"])
    
            if not row["PRODOTTO"] in prev_lines:

                info={}
                info["Quantità"]=int(row["QUANTITA'"])
                info["Prezzo d'acquisto"]=float(row["PREZZO D'ACQUISTO"])
                info["Prezzo di vendita"]=float(row["PREZZO DI VENDITA"])
                tmp[row["PRODOTTO"]]=info
            else:
                continue
        return tmp 
    
    






def add(product_name,quantity):
    
    """
    Funzione che aggiunge i prodotti acquistati al magazzino. Riceve come input le variabili product_name e quantity.

    1-Il file Magazzino.csv (creato con il primo prodotto acquistato) viene aperto in modalità append (le nuove righe vengono aggiunte alla fine del file).
    2-si controlla che il file sia vuoto: se lo è, viene creata l'intestazione con le informazioni sul nome del prodotto, la quantità, il prezzo di acquisto, il prezzo di vendita, il tipo di operazione (acquisto, vendita) e la data dell'operazione.
    3viene creata una lista con i nomi dei prodotti e viene verificata la presenza del prodotto inserito: 
       I) se non esiste, vengono chieste le informazioni sul prezzo di acquisto e sul prezzo di vendita e viene scritta una nuova riga nel file .csv
      II) se il prodotto esiste già, viene creata una nuova riga con i prezzi di acquisto e di vendita già registrati per quel prodotto.

    """

    with open("Magazzino.csv","a+",newline="") as csv_file:
        columns=["PRODOTTO","QUANTITA'","PREZZO D'ACQUISTO","PREZZO DI VENDITA","OPERAZIONE","DATE&ORA"]
        csv_reader=csv.DictReader(csv_file)
        csv_writer=csv.DictWriter(csv_file,fieldnames=columns)

        
        fileEmpty = os.stat("Magazzino.csv").st_size == 0
        if fileEmpty:
            csv_writer.writeheader()  

        
        list_products=[]
        csv_file.seek(0)
        for row in csv_reader:
            list_products.append(row["PRODOTTO"])
            
        
        if not product_name in set(list_products):
            purchase_price,selling_price=None,None
            while purchase_price==None or purchase_price <=0:
                try:
                    purchase_price=float(input("Prezzo d'acquisto: "))
                    if purchase_price <=0:
                        print(f"\nIl valore inserito {purchase_price} è minore o uguale a zero. Inserire un nuovo valore positivo per il prezzo di acquisto")
                except ValueError:
                    print("\nPrezzo di acquisto non valido: inserire numero decimale")
            while selling_price==None or selling_price <=0:
                try:        
                    selling_price=float(input("Prezzo di vendita: "))
                    if selling_price <=0:
                        print(f"\nIl valore inserito {selling_price} è minore o uguale a zero. Inserire un nuovo valore positivo per il prezzo di vendita")
                except ValueError:
                    print("\nPrezzo di vendita non valido: inserire numero decimale")

            
            csv_writer.writerow({"PRODOTTO":product_name,"QUANTITA'":quantity,"PREZZO D'ACQUISTO":purchase_price,"PREZZO DI VENDITA":selling_price,"OPERAZIONE":"acquisto","DATE&ORA":datetime.strftime(datetime.now(), "%d-%m-%Y %H.%M.%S")})

        
        else:
            csv_file.seek(0)
            list_lines=[]
            for row in list(csv_reader)[1:]:
                list_lines.append(row)
            for i,product in enumerate(list_products):
                if product_name==product:
                    z=i
                    break
                else:
                    continue
            
            csv_writer.writerow({"PRODOTTO":product_name,"QUANTITA'":quantity,"PREZZO D'ACQUISTO":list_lines[z]["PREZZO DI VENDITA"],"PREZZO DI VENDITA":list_lines[z]["PREZZO DI VENDITA"],"OPERAZIONE":"acquisto","DATE&ORA":datetime.strftime(datetime.now(), "%d-%m-%Y %H.%M.%S")})
        
        print(f"AGGIUNTO {quantity} X {product_name}")
    
    stock_info()
        









def itemize():
    
    """
    Funzione che elenca le scorte.

    1. Viene verificata la presenza di un file denominato Magazzino.csv. Se non esiste, viene mostrato un errore
    2-Per ogni prodotto (con quantità >0) in magazzino vengono stampati il nome, la quantità e il prezzo di vendita.

    """

    try:
        stock=stock_info()
        head_text=["\nPRODOTTO","QUANTITA'","PREZZO"]
        print(*head_text)

        for i in range(len(list(stock.keys()))):
            if list(stock.values())[i]["Quantità"]!=0:
                print(f"{list(stock.keys())[i]} "+
                f"{list(stock.values())[i]['Quantità']} "+
                f"€{list(stock.values())[i]['Prezzo di vendita']:.2f} ")
    except FileNotFoundError:
        print("Il registro acquisti/vendite non esiste. Forse il primo acquisto non è ancora stato registrato?...")
        
        
        








def sell(product_name,quantity):
    
    """
    Funzione che aggiunge i prodotti venduti al magazzino.

    1-Il file Magazzino.csv viene aperto in modalità append (le nuove righe vengono aggiunte alla fine del file).
    2-viene creato un elenco con i nomi dei prodotti e viene controllata la presenza del prodotto inserito:
       I) se non esiste, viene visualizzato un errore "prodotto non disponibile".
      II) se esiste già:
            i) ogni riga di Magazzino.csv (corrispondente a un prodotto acquistato o venduto) viene registrata in un elenco di dizionari
           ii) l'elenco dei dizionari viene modificato: per ogni prodotto, viene controllata la presenza dello stesso nei dizionari precedenti. 
              Se esiste, la sua quantità viene aggiunta al dizionario precedente
          iii) solo la prima occorrenza per ogni prodotto contiene ora la giusta quantità totale.
                Le altre righe vengono cancellate: l'elenco finale dei dizionari corrisponde allo stock prima della vendita
           iv) viene controllata la disponibilità dei prodotti. Se la quantità è sufficiente, viene aggiunta una nuova riga al file .csv, altrimenti viene stampato un errore.
            v) se la vendita è registrata la variabile stop=1, altrimenti 0, e viene richiamata la funzione stock_info per aggiornare lo stock
    """

    with open("Magazzino.csv","a+",newline="") as csv_file:
        columns=["PRODOTTO","QUANTITA'","PREZZO D'ACQUISTO","PREZZO DI VENDITA","OPERAZIONE","DATE&ORA"]
        csv_reader=csv.DictReader(csv_file)
        csv_writer=csv.DictWriter(csv_file,fieldnames=columns)
        fileEmpty = os.stat("Magazzino.csv").st_size == 0
        if fileEmpty:
            csv_writer.writeheader()  
        
        list_products=[]
        csv_file.seek(0)
        for row in csv_reader:
            list_products.append(row["PRODOTTO"])

        if not product_name in set(list_products):
            print("Prodotto non presente in magazzino")
        
        else:
            csv_file.seek(0)
            csv_reader=csv.DictReader(csv_file)
            list_lines=[]
            for row in list(csv_reader):
                list_lines.append(row)
            for i,product in enumerate(list_products):
                if product_name==product:
                    z=i
                    break
                else:
                    continue
            
            csv_file.seek(0) 
            csv_reader=csv.DictReader(csv_file)
            list_dict=[]
            for row in list(csv_reader):
                list_dict.append(row)
            
            for i,line in enumerate(list_dict):
                prev_lines=[]
                for j in range(i):
                    prev_lines.append(list_dict[j]["PRODOTTO"])
                for k,prev_line in enumerate(prev_lines):
                    if line["PRODOTTO"]==prev_line:
                        list_dict[k]["QUANTITA'"]=int(list_dict[k]["QUANTITA'"])+int(line["QUANTITA'"])
                    else:
                        continue

            tmp={}           
            for i,row in enumerate(list_dict):
                prev_lines=[]
                for j in range(i):
                    prev_lines.append(list_dict[j]["PRODOTTO"])

                if not row["PRODOTTO"] in prev_lines:
                    info={}
                    info["Quantità"]=int(row["QUANTITA'"])
                    info["Prezzo d'acquisto"]=float(row["PREZZO D'ACQUISTO"])
                    info["Prezzo di vendita"]=float(row["PREZZO DI VENDITA"])
                    tmp[row["PRODOTTO"]]=info

                else:
                    continue

            if quantity<=int(tmp[product_name]["Quantità"]):
                csv_writer.writerow({"PRODOTTO":product_name,"QUANTITA'":-quantity,"PREZZO D'ACQUISTO":list_lines[z]["PREZZO D'ACQUISTO"],"PREZZO DI VENDITA":list_lines[z]["PREZZO DI VENDITA"],"OPERAZIONE":"vendita","DATE&ORA":datetime.strftime(datetime.now(), "%d-%m-%Y %H.%M.%S")})
                stop=1
            else:
                availability=int(tmp[product_name]["Quantità"])
                print(f"Disponibilità massima in magazzino per il prodotto {product_name}: {availability}")
                stop=0

            return stop

    stock_info()





    
  
def profit():

  """
  Funzione che stampa il profitto totale lordo e netto 

  1-Se il tipo di operazione è "acquisto" il prezzo totale (prezzo*quantità) viene aggiunto alla variabile costo_acquisto
  2-Se il tipo di operazione è "vendita", il prezzo totale (prezzo*quantità) viene aggiunto a gross_profit (tenendo conto del segno).
  3-Il profitto netto viene calcolato come differenza
  """

  with open("Magazzino.csv") as csv_file:
        csv_reader=csv.DictReader(csv_file)
        list_lines=[]
        buying_cost=0
        gross_profit=0
        for row in list(csv_reader):
            list_lines.append(row)
        for line in list_lines:

            if line["OPERAZIONE"]=="acquisto":
                buying_cost+=float(line["PREZZO D'ACQUISTO"])*int(line["QUANTITA'"])
                
            if line["OPERAZIONE"]=="vendita":
                gross_profit+=-(float(line["PREZZO DI VENDITA"])*int(line["QUANTITA'"]))
    
  net_profit=gross_profit-buying_cost
  print(f"Profitto: lordo = {gross_profit:.2f}€, netto = {net_profit:.2f}€")
