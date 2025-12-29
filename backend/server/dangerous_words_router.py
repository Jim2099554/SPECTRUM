from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
import json
import os
from pathlib import Path

dangerous_words_router = APIRouter()

class DangerousWord(BaseModel):
    id: int
    word: str
    category: str
    added_date: str

# Ruta al archivo JSON de frases de riesgo
JSON_FILE_PATH = Path(__file__).parent.parent / "data" / "risk_phrases_corrected.json"

def load_words_from_json():
    """Carga las palabras/frases desde risk_phrases_corrected.json"""
    if not JSON_FILE_PATH.exists():
        return []
    
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    words_list = []
    word_id = 1
    
    # Cargar palabras por categoría
    for category, phrases in data.get("categories", {}).items():
        for phrase in phrases:
            words_list.append(DangerousWord(
                id=word_id,
                word=phrase,
                category=category,
                added_date="2025-12-28"  # Fecha por defecto para palabras existentes
            ))
            word_id += 1
    
    return words_list

def save_words_to_json(words: List[DangerousWord]):
    """Guarda las palabras/frases de vuelta al archivo JSON"""
    # Cargar estructura existente
    if JSON_FILE_PATH.exists():
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"flat": [], "categories": {}}
    
    # Reorganizar palabras por categoría
    categories = {}
    flat_list = []
    
    for word in words:
        if word.category not in categories:
            categories[word.category] = []
        categories[word.category].append(word.word)
        if word.word not in flat_list:
            flat_list.append(word.word)
    
    # Actualizar datos
    data["categories"] = categories
    data["flat"] = sorted(set(flat_list))  # Lista plana única y ordenada
    
    # Guardar archivo
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Cargar palabras al iniciar
dangerous_words_db = load_words_from_json()

@dangerous_words_router.get("/dangerous-words", response_model=List[DangerousWord])
def get_dangerous_words():
    """Obtiene todas las palabras/frases peligrosas registradas"""
    return dangerous_words_db

@dangerous_words_router.post("/dangerous-words", response_model=DangerousWord)
def add_dangerous_word(word: str, category: str = "general"):
    """Agrega una nueva palabra/frase peligrosa al directorio y actualiza el JSON"""
    if any(w.word.lower() == word.lower() for w in dangerous_words_db):
        raise HTTPException(status_code=400, detail="Esta palabra ya existe en el directorio")
    
    new_id = max(w.id for w in dangerous_words_db) + 1 if dangerous_words_db else 1
    new_word = DangerousWord(
        id=new_id,
        word=word.strip(),
        category=category,
        added_date=datetime.now().strftime("%Y-%m-%d")
    )
    dangerous_words_db.append(new_word)
    
    # Guardar cambios al JSON
    save_words_to_json(dangerous_words_db)
    
    return new_word

@dangerous_words_router.delete("/dangerous-words/{word_id}")
def delete_dangerous_word(word_id: int):
    """Elimina una palabra/frase del directorio y actualiza el JSON"""
    global dangerous_words_db
    for w in dangerous_words_db:
        if w.id == word_id:
            dangerous_words_db = [word for word in dangerous_words_db if word.id != word_id]
            
            # Guardar cambios al JSON
            save_words_to_json(dangerous_words_db)
            
            return {"ok": True, "message": "Palabra eliminada correctamente"}
    raise HTTPException(status_code=404, detail="Palabra no encontrada")
