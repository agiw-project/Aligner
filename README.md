# Aligner

Fornire nella cartella Url i file contenenti gli indirizzi URL delle entity page.\n
PIPELINE:\n
Run main.\n
In caso di mancata estrazione precedente: si creeranno i file json dell'estrazione, altrimenti si passerà alla calibrazione.\n
In caso di mancata calibrazione: si calcoleranno le threshold migliori salvandole nel file di testo max_threshold.txt, altrimenti si passerà all'allineamento.\n
Allineamento delle 100 pagine comparando a coppia le sorgenti 1-2, 1-3, 2-3.\n
Stampa delle metriche: precision, recall e fscore.
