import cv2 as cv
import face_recognition as fr
import os
import numpy as np

os.makedirs("faces", exist_ok=True)   #crea una cartella "faces", e se già esiste va avanti 
name = input("Enter your name: ")
cam = cv.VideoCapture(0)   #inizializza la cam predefinita del sistema

while True:                    # ciclo che permette di continuare a catturare frame dalla cam
    success, frame = cam.read()     #cam.read() cattura il frame, e se c'è un errore fermiamo il ciclo 
    if not success:
        print("Failed to capture frame")
        break

    original_frame = frame.copy() # useremo una copia da convertire in rgb

    # Converte il fotogramma in RGB per rilevare i volti.
    detection_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    face_locations = fr.face_locations(detection_rgb, model="hog")

    # Disegna un rettangolo attorno a ogni volto rilevato.
    for top, right, bottom, left in face_locations:
        cv.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

    # Mostra il numero di volti rilevati.
    cv.putText(
        frame,
        f"Volti rilevati: {len(face_locations)}",
        (10, 30),
        cv.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )
    cv.imshow("Training - Press 'c' to capture or 'q' to quit", frame)
    frame = original_frame
    # Aspetta 1 millisecondo e controlla se viene premuto un tasto
    key = cv.waitKey(1) & 0xFF   #0xFF serve perchè così il codice ASCII 113 associato a q arriva pulito (poicheè fa un operazione AND bit a bit)
                                    #mette in colonna i 2 numeri e per ogni coppia di cifre restituisce 1 solo se entrambi sono 1, 0 altrimenti
    # Se premi 'q', esce dal ciclo
    if key == ord('q'):
        break
    # Se premi 'c', qui in futuro salveremo la foto
    elif key == ord('c'):     #Con c scatto la foto
        print("Foto catturata!")
        img_path = f'faces\{name}.jpg'      #prepariamo il salvataggio dello scatto, scrivendo il path, ovvero dove andrà a finre l'immagine
                                                #usiamo {name} per riprendere il nome dell'input
        cv.imwrite(img_path,frame)         #salva il frame scattato nel path, ovvero dentro faces
        img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  #convertiamo il frame da BGR a RGB per il face encoding (codifica del viso)
        encodings = fr.face_encodings(img_rgb)   #codifica del frame, quindi codifica del viso

        if encodings:     # se l'encoding va a buon fine
            np.save(f'faces\{name}_encodings.npy', encodings[0])      #salviamo l'encoding in un file .npy (numpy)
            print(f"Encoding saved for {name}")
        else:
            print("No face detected")

cam.release()                 #Usciti dal while toglie la cam e chiude la finestra
cv.destroyAllWindows()




