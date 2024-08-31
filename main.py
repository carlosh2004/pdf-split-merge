import os.path

from python.merge import merge_pdf
from python.split import split_pdf
from python.utils import get_pdf_files


def main():
    while True:
        pages_per_split = input('Cantidad de paginas a separar por archivo (default 5000): ')

        if pages_per_split.strip() == "":
            pages_per_split = 5000
            break
        else:
            try:
                pages_per_split = int(pages_per_split)
                if pages_per_split <= 0:
                    raise ValueError("El numero de paginas debe ser mayor que 0.")
                break
            except ValueError as e:
                print(f"Entrada no valida: {e}. Por favor, introduce un numero entero positivo.")

    pdf_files = get_pdf_files('pdf')
    if len(pdf_files) == 0:
        print("No se encontraron archivos PDF en el directorio.")
    elif len(pdf_files) == 1:
        file_path = os.path.join('pdf', pdf_files[0])
        split_pdf(file_path, pages_per_split)
    else:
        output_file = merge_pdf(pdf_files)
        if output_file:
            split_pdf(output_file, pages_per_split)
        else:
            print("No se pudo completar el proceso de unión de PDFs.")


if __name__ == "__main__":
    main()
