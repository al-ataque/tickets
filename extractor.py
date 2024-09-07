import re
import PyPDF2

# Ruta del archivo PDF
pdf_path = 'tickets/ticket_dia_05_09_2024_14_09.pdf'

def load(pdf_path:str) -> str:
    # Abrimos el archivo PDF
    text = ''
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Extraemos el texto de todas las páginas
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    
    return text

def get_data(text) -> list:
    # Limpieza del texto: eliminamos saltos de línea y espacios innecesarios
    text = re.sub(r'\s+', ' ', text)
    
    # Expresión regular mejorada para capturar los nombres de productos, cantidad, precio unitario y total
    producto_regex = r'([A-Z\s0-9%\.]+)\s([0-9]+ ud)\s([0-9,]+ €)\s([0-9,]+ €)'
    
    # Extraemos los productos coincidentes
    productos = re.findall(producto_regex, text)

    # Expresión regular para extraer la fecha en formato DD/MM/AAAA
    date_regex = r'\d{2}/\d{2}/\d{4}'
    date = re.findall(date_regex, text)

    return productos, date[0]

def clean_data(productos) -> list:
    # Lista para almacenar los productos limpios
    productos_limpios = []

    # Procesamos cada producto
    for producto in productos:
        nombre = producto[0].strip()
        cantidad = producto[1]
        precio_unitario = producto[2]
        precio_total = producto[3]
        
        # Limpiamos el nombre del producto eliminando letras sueltas o encabezados

        nombre = re.sub(r'^[A-Z]\s+', '', nombre)  # Elimina letras sueltas al principio del nombre
        nombre = re.sub(r'\b(CANTIDAD|PRECIO|KG|TOTAL)\b', '', nombre).strip()  # Elimina palabras clave no deseadas

        # Agregamos el producto limpio a la lista si tiene un nombre válido
        if nombre:
            productos_limpios.append((nombre, cantidad, precio_unitario, precio_total))

    return productos_limpios

def extract(pdf_path) -> list:
    data = get_data(load(pdf_path))
    return clean_data(data[0]), data[1]

# Mostramos los productos limpios
# for producto in productos_limpios:
#     print(f"Producto: {producto[0]}, Cantidad: {producto[1]}, Precio unitario: {producto[2]}, Total: {producto[3]}")
