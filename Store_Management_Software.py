# Store Management Software

# Creazione di un software per la gestione di uno shop vegano. Il software ha le seguenti caratteristiche:

# Registrazione di nuovi prodotti, con nome, quantità, prezzo di vendita e prezzo di acquisto;
# Elenco di tutti i prodotti contenuti nel magazzino;
# Registrazione in un file csv dello storico di tutte le attività (operazioni di acquisto e vendita, data e ora incluse);
# Registrazione delle vendite effettuate;
# Visualizzazione dei profitti lordi e netti.


import csv
import os
from datetime import datetime
from store_functions import help_cmd
from store_functions import stock_info
from store_functions import add
from store_functions import itemize
from store_functions import sell
from store_functions import profit



cmd = None
while cmd!="chiudi":

    cmd = input("\nInserire un comando per eseguire un'azione (digitare aiuto per vedere le funzioni disponibili): ")  
    
    if cmd=="vendita":

        sold_dict={}
        answer="si"
        
        while answer.lower()!="no":
            is_string,quantity=False,None

            while is_string==False:
                try:
                    product_name=input("Nome del prodotto: ")  
                    if product_name.isnumeric():
                        is_string==False
                        raise ValueError("\nProdotto non valido: inserito valore numerico")
                        continue
                    else:
                        is_string=True
                except ValueError as e:
                    print(e)

            while quantity==None or quantity <=0:
                try:
                    quantity=int(input("Quantità: "))
                    if quantity <= 0:
                        print( "\nIl valore inserito è minore o uguale a zero. Inserire un valore positivo per la quantità")
                except ValueError:
                    print("\nQuantità non valida: inserire numero intero")
    
            #Viene richiamata la funzione sell: se stop=1 la vendita viene registrata in un dizionario temporaneo sold_dict
            #e all'utente viene chiesto se deve essere venduto un nuovo prodotto. Se viene selezionato NO, viene mostrato il prezzo totale             #di vendita.
            stop=sell(product_name,quantity)
            stock=stock_info()
            
            if stop==1:
                sold_dict[product_name]=quantity
  
            answer=input("Aggiungere un altro prodotto?: [si/NO]")
        
        if len(list(sold_dict.keys()))!=0:
            print("\nVENDITA REGISTRATA: ")
            
        total_sold=0
        for key in list(sold_dict.keys()):
            print(f"{sold_dict[key]} X {key}: €{stock[key]['Prezzo di vendita']}")
            total_sold+=(stock[key]['Prezzo di vendita']*sold_dict[key])
        print(f"\nTotale: €{total_sold:.2f}")





    elif cmd=="profitti":

        profit()


    
    elif cmd=="aggiungi":
    
        is_string,quantity=False,None
        while is_string==False:
            try:
                product_name=input("Nome del prodotto: ")  
                if product_name.isnumeric():
                    is_string==False
                    raise ValueError("\nInserimento prodotto non valido: valore numerico inserito") 
                    continue
                else:
                    is_string=True
            except ValueError as e:
                print(e)

        while quantity==None or quantity <=0:
            try:
                quantity=int(input("Quantità: ")) 
                if quantity <= 0:
                    print( "\nIl valore inserito è minore o uguale a zero. Inserire un valore positivo per la quantità")
            except ValueError:
                print("\nQuantità non valida: inserire numero intero")
                    
        #funzione aggiungi viene richiamata
        add(product_name,quantity)





    elif cmd=="elenca":
    
        itemize()
        



    elif cmd=="aiuto":
    
        help_cmd()




    
    elif cmd=="chiudi":

        print("Bye Bye, ci si rivede quando si vuole eseguire un'altra azione")
        break
    else:
        print("\nCommando non valido")
        help_cmd()