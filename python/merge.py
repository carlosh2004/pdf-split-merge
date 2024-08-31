import os
import threading
from datetime import datetime

import PyPDF2

from python.utils import show_loading_message


def merge_pdfs(pdf_files, output_dir='pdf') -> str | None:
    """
    Une varios archivos PDF en un solo archivo PDF.

    :param pdf_files: Lista de rutas a archivos PDF que se van a unir.
    :param output_dir: Directorio donde guardar el archivo PDF combinado.
    :return: Ruta del archivo PDF combinado o None en caso de error.
    """
    pdf_writer = PyPDF2.PdfWriter()
    os.makedirs(output_dir, exist_ok=True)  # Asegurarse de que el directorio de salida existe

    for pdf_file in pdf_files:
        path_pdf_file = os.path.join(os.getcwd(), 'pdf', pdf_file)
        if os.path.isfile(path_pdf_file):
            try:
                pdf_reader = PyPDF2.PdfReader(path_pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            except Exception as e:
                print(f"Error al leer el archivo {path_pdf_file}: {e}. Saltando...")
        else:
            print(f"El archivo {path_pdf_file} no se encuentra. Saltando...")

    if not pdf_writer.pages:
        print("No se han añadido páginas al archivo PDF combinado.")
        return None

    output_file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    output_file_path = os.path.join(output_dir, output_file_name)

    try:
        with open(output_file_path, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)
    except Exception as e:
        print(f"Error al guardar el archivo PDF combinado: {e}")
        return None

    return output_file_path


def merge_pdf(pdf_files, output_dir='pdf'):
    """
    Maneja la unión de varios archivos PDF en un hilo y muestra un mensaje de carga.

    :param pdf_files: Lista de rutas a archivos PDF que se van a unir.
    :param output_dir: Directorio donde guardar el archivo PDF combinado.
    """
    print("Iniciando la unión de PDFs")

    # Crear un evento de parada para el hilo de carga
    stop_event = threading.Event()
    loading_thread = threading.Thread(target=show_loading_message, args=("Procesando archivos PDF", stop_event))

    # Iniciar el hilo de carga
    loading_thread.start()

    try:
        # Ejecutar la unión de los archivos PDF
        output_file = merge_pdfs(pdf_files, output_dir)
        if output_file:
            print(f"PDFs unidos exitosamente en {output_file}")
            return output_file
        else:
            print("No se pudo completar el proceso de unión de PDFs.")
    finally:
        # Detener el hilo de carga
        stop_event.set()
        loading_thread.join()

    print("Proceso completado.")
