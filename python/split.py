import os
import threading
from datetime import datetime

from PyPDF2 import PdfReader, PdfWriter

from python.utils import show_loading_message


def split_pdf_main(file_path: str, max_pages_per_split: int = 1000):
    """
    Divide un archivo PDF en partes más pequeñas.

    :param file_path: Ruta del archivo PDF a dividir.
    :param max_pages_per_split: Número máximo de páginas por archivo dividido.
    """
    folder_name = os.path.join('pdf', datetime.now().strftime('%Y%m%d%H%M%S'))
    os.makedirs(folder_name, exist_ok=True)

    try:
        # Abrir el archivo PDF
        pdf_reader = PdfReader(file_path)
        total_pages = len(pdf_reader.pages)

        # Calcular cuántos archivos se necesitan
        num_splits = (total_pages + max_pages_per_split - 1) // max_pages_per_split

        for i in range(num_splits):
            pdf_writer = PdfWriter()
            start_page = i * max_pages_per_split
            end_page = min(start_page + max_pages_per_split, total_pages)

            # Añadir páginas al nuevo archivo PDF
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            # Guardar el archivo dividido
            split_file_path = os.path.join(folder_name, f"part_{i + 1}.pdf")
            with open(split_file_path, "wb") as output_pdf:
                pdf_writer.write(output_pdf)
    except Exception as e:
        print(f"Error al dividir el archivo PDF: {e}")


def split_pdf(file_path: str, pages_per_split: int):
    """
    Maneja la separación de un archivo PDF en un hilo y muestra un mensaje de carga.

    :param file_path: Ruta del archivo PDF a dividir.
    :param pages_per_split: Número máximo de páginas por archivo dividido.
    """
    print("Iniciando la separación de PDF")

    # Crear un evento de parada para el hilo de carga
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=show_loading_message, args=("Procesando archivo", stop_event))

    # Iniciar el hilo de carga
    loading_thread.start()

    try:
        # Ejecutar la separación del PDF
        split_pdf_main(file_path, pages_per_split)
    finally:
        # Detener el hilo de carga
        stop_event.set()
        loading_thread.join()

    print("Proceso completado.")
