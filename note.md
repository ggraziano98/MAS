MERCATO SCEMO



    1 oggetto di scambio: Banane
                            -->     il prezzo dovrà poi essere concordato tra domanda e acquisto quando faremo un modello migliore
                                per ora i venditori si comportano come dominanti 
        - Per ogni giorno di mercato arrivano i rifornimenti di banane ai venditori
            - questi oscillano intorno ad un valore fisso, se minore c'è 'scarsità' di banane, se maggiore c'è 'abbondanza' di banane



    N agenti che vendono
        - decidono prezzo di vendita ogni giorno
            - hanno uno stock di banane che ogni giorno si "ricarica" (con qualche oscillazione random) e decidono il prezzo in base ad esso 
            - ogni giorno decidono di correggere il prezzo di vendita (intorno al prezzo medio del giorno precedente):
                - Alzarlo se il giorno prima hanno venduto più della media della quantità venduta in un tot di giorni precedenti
                - Alzarlo se lo stock complessivo del venditore n scarseggia (intorno ad un valore medio)
                - Abbassarlo se il giorno prima hanno venduto meno della media della quantità venduta in un tot di giorni precedenti
                - Abbassarlo se lo stock del venditore n abbonda (intorno ad un valore medio)



    M agenti che comprano 
        - stessi soldi/distribuzione di soldi
        - incontrano j venditori ogni giorno a random
            ----- come scriviamo sto incontro?
            --------------------------------------- c'è un metodo MultiGrid dentro mesa che permette a piu agenti di condividere la stessa cella
                                                    potremmo simulare in questo modo gli incontri casuali nel mercato sbarazzandoci del problema dei primi vicini
                                                    https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html
        - decidono prezzo di acquisto
            - ogni giorno l'agente m consuma k banane
                - in base a k ha un fabbisogno di banane che determina il suo bisogno di acquisto
                - il bisogno di acquisto determina la propensione a spendere di più e comprare al prezzo dei venditori
        - scelgono di comprare da un certo venditore in modo da massimizzare la propria utility:
            - Minore spesa e quantità maggiore o uguale al fabbisogno



    Scale temporali:
        - Tutte le dinamiche si ripetono ogni giorno da capo
        - All'interno della giornata ci sono dei tick nei quali gli agenti si incontrano 
        - "La pausa" tra un giorno ed il seguente consiste nell'aggiornamento delle variabili (stock-prezzi attesi-etc) 
