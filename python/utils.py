import os
import sys
import time


def get_pdf_files(directory):
    # Listar todos los archivos en el directorio
    all_files = os.listdir(directory)

    # Filtrar solo los archivos PDF
    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]

    return pdf_files


def show_loading_message(message, stop_event):
    """Muestra un mensaje de carga con puntos animados."""
    sys.stdout.write(message)
    sys.stdout.flush()
    while not stop_event.is_set():
        for char in ['.', '..', '...']:
            if stop_event.is_set():
                break
            sys.stdout.write(f'\r{message}{char}')
            sys.stdout.flush()
            time.sleep(0.5)
    sys.stdout.write('\r' + ' ' * (len(message) + 3) + '\r')
    sys.stdout.flush()
