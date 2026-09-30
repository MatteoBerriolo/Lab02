def carica_da_file (file_album):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = {}
    '''inserisco un dizionario per rendere possibile la separaizione delle varie colonne in base alla tipologia '''
    try:
        with open(file_album, "r", encoding='utf-8') as f:
            linee = f.readlines()
            ''' la fase del .readlines() mi permette di saltare la prima riga del file di testo iniziale, dato che non ho dati necessari'''
            for riga in linee[1:] : ''' indica che prende l'indice di partenza e poi successivamente fino alla fine della lista '''
            riga = riga.strip()
            if riga :
                parti = riga.split(',')
                codice = parti[0]
                titolo = parti[1]
                autore = parti[2]
                mese = int(parti[3].strip())
                anno = int(parti[4].strip())

                ''' dopo aver preso tutti le varie parti della riga dividendole con i nomi che le caratterizzano posso inserirle nella funzione aggiungi_foto'''
                aggiungi_foto(album, codice, titolo, autore, mese, anno, file_album)
    except FileNotFoundError:
        print(f"Errore: il file {file_album} non esiste.")
    return album

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_album):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    foto = {
        "album": album,
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno,
    }
    '''impongo una condizione che se l'anno non è presente creo una lista che lo inserisca'''
    if anno not in album:
        album[anno] = []

    album[anno].append(foto)

def cerca_foto(album,codice):
    """Cerca una foto nell'album dato il codice"""
    for anno, lista_foto in album.items():
        for foto in lista_foto:
            if foto['codice'] == codice:
                return foto
    '''con questo metodo controllo se è presente la foto all'interno della lista album, nel caso non fosse così restituisco None '''
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:
        print(f"Nessuna foto trovata per l'anno {anno}.")
        return []

    '''dopo aver controllato che l'anno sia in album, devo metterle anche in ordine utilizzando il sorted, in base a quello che 
    c'è dentro posso metterlo in ordine in base al nome del titolo '''
    foto_ordiante = sorted(album[anno], key=lambda x: x['titolo'])
    return foto_ordiante

def main():
    album = []
    file_album = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_album = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_album)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_album)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue
            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")


        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")

    if __name__ == "__main__":
        main()
