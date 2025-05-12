# utils/csv_handler.py
import csv
import os
from typing import List, Dict, Optional

def read_csv(filepath: str) -> List[Dict[str, str]]:
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except csv.Error as e:
        raise RuntimeError(f"Error de lectura en CSV '{filepath}': {e}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado al leer el archivo CSV '{filepath}': {e}")

def write_csv(filepath: str, data: List[Dict[str, str]], headers: Optional[List[str]] = None):
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            if data:
                fieldnames = data[0].keys()
            elif headers:
                fieldnames = headers
            else:
                raise ValueError("No se proporcionaron datos ni encabezados para escribir el CSV.")

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            if data:
                writer.writerows(data)
    except csv.Error as e:
        raise RuntimeError(f"Error de escritura en CSV '{filepath}': {e}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado al escribir el archivo CSV '{filepath}': {e}")

def ensure_csv_exists(filepath: str, headers: List[str]):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
    except Exception as e:
        raise RuntimeError(f"No se pudo asegurar la existencia del archivo CSV '{filepath}': {e}")
