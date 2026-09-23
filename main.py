import cv2 as cv
import face_recognition as fr
import os
import numpy as np

os.makedirs("faces", exist_ok=True)   #crea una cartella "faces", e se già esiste va avanti
name = input("Enter your name: ")
cam = cv.VideoCapture(0)   #inizializza la cam predefinita del sistema

# Prepariamo i percorsi una sola volta.
img_path = os.path.join("faces", f"{name}.jpg")
encoding_path = os.path.join("faces", f"{name}_encodings.npy")

try:
    while True:                    # ciclo che permette di continuare a catturare frame dalla cam
        success, frame = cam.read()     #cam.read() cattura il frame, e se c'è un errore fermiamo il ciclo
        if not success:
            print("Failed to capture frame")
            break

        # Converte il fotogramma in RGB per rilevare i volti.
        # useremo questa immagine senza rettangoli anche per il face encoding
        img_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        face_locations = fr.face_locations(img_rgb, model="hog")

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

        # Aspetta 1 millisecondo e controlla se viene premuto un tasto
        key = cv.waitKey(1) & 0xFF   #0xFF serve perchè così il codice ASCII 113 associato a q arriva pulito (poicheè fa un operazione AND bit a bit)
                                    #mette in colonna i 2 numeri e per ogni coppia di cifre restituisce 1 solo se entrambi sono 1, 0 altrimenti

        # Se premi 'q', esce dal ciclo
        if key == ord('q'):
            break

        # Se premi 'c', salviamo la foto
        elif key == ord('c'):     #Con c scatto la foto
            # Il path preparato sopra indica dove andrà a finire l'immagine.
            # usiamo name per riprendere il nome dell'input

            # Ricava la foto senza rettangoli dall'immagine RGB già disponibile.
            photo = cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR)
            if not cv.imwrite(img_path, photo):  #salva il frame scattato nel path, ovvero dentro faces
                print("Failed to save photo")
                continue

            print("Foto catturata!")

            if face_locations:
                #codifica del frame, quindi codifica del viso
                # Riutilizza la posizione del primo volto, perché salviamo solo il suo encoding.
                encodings = fr.face_encodings(
                    img_rgb,
                    known_face_locations=face_locations[:1]
                )

                if encodings:     # se l'encoding va a buon fine
                    np.save(encoding_path, encodings[0])  #salviamo l'encoding in un file .npy (numpy)
                    print(f"Encoding saved for {name}")
                else:
                    print("No face encoding generated")
            else:
                print("No face detected")

finally:
    cam.release()                 #Usciti dal while toglie la cam e chiude la finestra
    cv.destroyAllWindows()