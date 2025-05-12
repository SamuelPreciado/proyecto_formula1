# utils/csv_handler.py
import csv
import os
from typing import List, Dict, Optional

def read_csv(filepath: str) -> List[Dict[str, str]]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

def write_csv(filepath: str, data: List[Dict[str, str]], headers: Optional[List[str]] = None):
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        if data:
            fieldnames = data[0].keys()
        elif headers:
            fieldnames = headers
        else:
            raise ValueError("No data provided and headers not specified.")

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        if data:
            writer.writerows(data)

def ensure_csv_exists(filepath: str, headers: List[str]):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)  # ← Esto crea la carpeta si no existe
    if not os.path.exists(filepath):
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
