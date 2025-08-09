#!/usr/bin/env python3
"""
Script to update all language files with missing keys from the English template
"""

import json
import os
from typing import Dict, Any

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """Save JSON file with proper formatting"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def get_all_keys_from_dict(data: Dict[str, Any], prefix: str = "") -> set:
    """Recursively get all keys from nested dictionary"""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys_from_dict(value, full_key))
        else:
            keys.add(full_key)
    return keys

def set_nested_key(data: Dict[str, Any], key_path: str, value: str):
    """Set a value in nested dictionary using dot notation"""
    parts = key_path.split('.')
    current = data
    
    # Navigate to the parent of the target key
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    
    # Set the final key
    current[parts[-1]] = value

def get_nested_value(data: Dict[str, Any], key_path: str) -> str:
    """Get value from nested dictionary using dot notation"""
    parts = key_path.split('.')
    current = data
    
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return key_path  # Return key as fallback
    
    return str(current) if current is not None else key_path

def translate_key_to_language(key: str, english_value: str, target_lang: str) -> str:
    """Basic translation mapping for common keys"""
    
    # German translations
    german_translations = {
        'Admin access': 'Administratorzugang',
        'User Management': 'Benutzerverwaltung',
        'Search Items': 'Elemente suchen',
        'Search items by name or description...': 'Elemente nach Name oder Beschreibung suchen...',
        'ID': 'ID',
        'Username': 'Benutzername',
        'Email': 'E-Mail',
        'Full Name': 'Vollständiger Name',
        'Role': 'Rolle',
        'Status': 'Status',
        'Created': 'Erstellt',
        'Updated': 'Aktualisiert',
        'Actions': 'Aktionen',
        'View': 'Ansehen',
        'Edit': 'Bearbeiten',
        'Delete': 'Löschen',
        'Activate': 'Aktivieren',
        'Deactivate': 'Deaktivieren',
        'Active': 'Aktiv',
        'Inactive': 'Inaktiv',
        'User Dashboard': 'Benutzer-Dashboard',
        'Search and manage your items': 'Suchen und verwalten Sie Ihre Elemente'
    }
    
    # Spanish translations
    spanish_translations = {
        'Admin access': 'Acceso de administrador',
        'User Management': 'Gestión de usuarios',
        'Search Items': 'Buscar elementos',
        'Search items by name or description...': 'Buscar elementos por nombre o descripción...',
        'ID': 'ID',
        'Username': 'Nombre de usuario',
        'Email': 'Correo electrónico',
        'Full Name': 'Nombre completo',
        'Role': 'Rol',
        'Status': 'Estado',
        'Created': 'Creado',
        'Updated': 'Actualizado',
        'Actions': 'Acciones',
        'View': 'Ver',
        'Edit': 'Editar',
        'Delete': 'Eliminar',
        'Activate': 'Activar',
        'Deactivate': 'Desactivar',
        'Active': 'Activo',
        'Inactive': 'Inactivo',
        'User Dashboard': 'Panel de usuario',
        'Search and manage your items': 'Buscar y gestionar sus elementos'
    }
    
    # French translations
    french_translations = {
        'Admin access': 'Accès administrateur',
        'User Management': 'Gestion des utilisateurs',
        'Search Items': 'Rechercher des éléments',
        'Search items by name or description...': 'Rechercher des éléments par nom ou description...',
        'ID': 'ID',
        'Username': "Nom d'utilisateur",
        'Email': 'E-mail',
        'Full Name': 'Nom complet',
        'Role': 'Rôle',
        'Status': 'Statut',
        'Created': 'Créé',
        'Updated': 'Mis à jour',
        'Actions': 'Actions',
        'View': 'Voir',
        'Edit': 'Modifier',
        'Delete': 'Supprimer',
        'Activate': 'Activer',
        'Deactivate': 'Désactiver',
        'Active': 'Actif',
        'Inactive': 'Inactif',
        'User Dashboard': 'Tableau de bord utilisateur',
        'Search and manage your items': 'Rechercher et gérer vos éléments'
    }
    
    # Select the appropriate translation dictionary
    if target_lang == 'de':
        translations = german_translations
    elif target_lang == 'es':
        translations = spanish_translations
    elif target_lang == 'fr':
        translations = french_translations
    else:
        return english_value  # Return original if no translation available
    
    # Return translated value or original if not found
    return translations.get(english_value, english_value)

def update_language_file(english_data: Dict[str, Any], target_lang: str) -> bool:
    """Update a specific language file with missing keys"""
    
    target_file = f'locales/{target_lang}/messages.json'
    print(f"\n=== UPDATING {target_lang.upper()} ===")
    
    # Load existing target language data
    target_data = load_json_file(target_file)
    if not target_data:
        print(f"Could not load {target_file}, creating new structure")
        target_data = {}
    
    # Get all keys from English
    english_keys = get_all_keys_from_dict(english_data)
    target_keys = get_all_keys_from_dict(target_data)
    
    missing_keys = english_keys - target_keys
    
    print(f"Total English keys: {len(english_keys)}")
    print(f"Current {target_lang} keys: {len(target_keys)}")
    print(f"Missing keys: {len(missing_keys)}")
    
    if not missing_keys:
        print(f"✅ {target_lang.upper()} is already up to date!")
        return True
    
    print(f"Adding missing keys: {sorted(list(missing_keys))}")
    
    # Add missing keys with translations
    added_count = 0
    for key in missing_keys:
        # Get the English value
        english_value = get_nested_value(english_data, key)
        translated_value = translate_key_to_language(key, english_value, target_lang)
        set_nested_key(target_data, key, translated_value)
        added_count += 1
    
    # Save updated file
    if save_json_file(target_file, target_data):
        print(f"✅ Successfully updated {target_file} with {added_count} new keys")
        return True
    else:
        print(f"❌ Failed to save {target_file}")
        return False

def main():
    """Main function to update all language files"""
    
    print("=== UPDATING ALL LANGUAGE FILES ===")
    
    # Load English as template
    english_file = 'locales/en/messages.json'
    english_data = load_json_file(english_file)
    
    if not english_data:
        print(f"❌ Could not load English template from {english_file}")
        return
    
    print(f"✅ Loaded English template with {len(get_all_keys_from_dict(english_data))} keys")
    
    # Languages to update
    languages_to_update = ['de', 'es', 'fr']
    
    success_count = 0
    for lang in languages_to_update:
        if update_language_file(english_data, lang):
            success_count += 1
    
    print(f"\n=== SUMMARY ===")
    print(f"Successfully updated: {success_count}/{len(languages_to_update)} languages")
    
    if success_count == len(languages_to_update):
        print("🎉 All language files are now up to date!")
    else:
        print("⚠️  Some updates failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
