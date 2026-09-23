# Face Detection & Encoding

Progetto personale in Python per rilevare volti dalla webcam e acquisire campioni da utilizzare in successivi esperimenti di riconoscimento facciale. Integra **OpenCV** per l’acquisizione e la visualizzazione del video, **face_recognition** per il rilevamento e la codifica dei volti e **NumPy** per il salvataggio degli encoding.

## Funzionalità

- Rilevamento dei volti su ogni fotogramma con il modello HOG.
- Visualizzazione di rettangoli verdi attorno ai volti e del numero di volti rilevati.
- Acquisizione manuale di una fotografia tramite tastiera.
- Salvataggio della fotografia originale, senza annotazioni.
- Estrazione e salvataggio dell’encoding facciale in formato `.npy`.

Il progetto rileva e codifica i volti; non confronta ancora gli encoding per identificare persone già registrate. L’acquisizione dei campioni non comporta l’addestramento di un nuovo modello.

## Tecnologie

| Tecnologia | Utilizzo |
| --- | --- |
| Python | Logica dell’applicazione |
| OpenCV | Accesso alla webcam, gestione dei fotogrammi e annotazioni |
| face_recognition | Rilevamento dei volti ed estrazione degli encoding |
| NumPy | Salvataggio dei vettori numerici |

## Installazione

Sono necessari Python, una webcam e un ambiente desktop che consenta l’apertura delle finestre OpenCV.

Installa le dipendenze:

```bash
python -m pip install opencv-python face_recognition numpy
```

`face_recognition` dipende da `dlib`: l’installazione può richiedere strumenti di compilazione, a seconda del sistema operativo e della versione di Python.

## Configurazione della webcam

Il codice utilizza:

```python
cam = cv.VideoCapture(2)
```

L’indice `2` seleziona il dispositivo video con quell’indice, generalmente la terza webcam enumerata. Per utilizzare la webcam predefinita, prova `0`. La disponibilità degli indici dipende dal sistema.

## Avvio

Salva lo script come `main.py` ed esegui:

```bash
python main.py
```

1. Inserisci il nome da associare al campione.
2. Posizionati davanti alla webcam.
3. Premi **C** per acquisire una fotografia e calcolare l’encoding.
4. Premi **Q** per chiudere l’applicazione.

Utilizza un nome semplice, senza separatori di percorso o caratteri non validi nei nomi dei file.

## File generati

La cartella `faces` viene creata automaticamente nella directory da cui viene avviato il programma.

Esempio di struttura dopo un’acquisizione riuscita:

```text
progetto/
├── main.py
├── README.md
└── faces/
    ├── Mario.jpg
    └── Mario_encodings.npy
```

| File | Contenuto |
| --- | --- |
| `Mario.jpg` | Fotogramma originale acquisito dalla webcam |
| `Mario_encodings.npy` | Vettore di 128 valori che rappresenta il volto rilevato |

Acquisizioni successive con lo stesso nome sovrascrivono i file corrispondenti.

## Come funziona

Il programma legge continuamente i fotogrammi dalla webcam e conserva una copia dell’immagine originale. Converte poi il fotogramma da BGR a RGB e utilizza `face_locations` per individuare i volti.

Le coordinate restituite vengono utilizzate per disegnare i rettangoli verdi e mostrare il conteggio dei volti nella finestra video.

Quando viene premuto **C**, il programma salva il fotogramma originale e richiama `face_encodings`. Se viene trovato almeno un volto, salva il primo encoding restituito. Alla chiusura, rilascia la webcam e distrugge le finestre OpenCV.

## Limiti attuali

- Non identifica le persone e non confronta gli encoding salvati.
- Se sono presenti più volti, salva soltanto il primo encoding restituito, che potrebbe non corrispondere alla persona indicata.
- La fotografia viene salvata anche se non viene trovato alcun volto.
- Se un’acquisizione senza volto sovrascrive una fotografia esistente, un eventuale encoding precedente rimane nella cartella.
- Illuminazione, posa, occlusioni e qualità della webcam possono influenzare il rilevamento.
- La fluidità dipende dall’hardware e dalla risoluzione video; non sono inclusi benchmark di prestazioni.

Per acquisire un campione coerente, deve essere presente una sola persona nell’inquadratura.

## Competenze applicate

- Elaborazione di un flusso video con OpenCV.
- Conversione tra spazi colore BGR e RGB.
- Utilizzo di modelli preaddestrati per la computer vision.
- Annotazione delle immagini tramite coordinate.
- Estrazione e persistenza di rappresentazioni numeriche dei volti.
- Gestione dell’input da tastiera e delle risorse della webcam.

## Possibili sviluppi

- Accettare l’acquisizione soltanto quando è presente un unico volto.
- Verificare il salvataggio delle immagini e validare il nome inserito.
- Raccogliere più campioni per persona senza sovrascrivere quelli precedenti.
- Confrontare gli encoding per riconoscere persone già registrate.
- Rendere configurabili l’indice della webcam e la directory di salvataggio.
- Misurare prestazioni e qualità del rilevamento in condizioni diverse.

## Gestione dei dati

Fotografie ed encoding facciali sono dati personali sensibili. Utilizzare campioni propri o acquisiti con il consenso delle persone coinvolte ed evitare di pubblicarli nel repository.

È consigliato aggiungere queste righe al file `.gitignore`:

```gitignore
faces/
__pycache__/
.venv/
```