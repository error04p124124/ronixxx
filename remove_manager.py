#!/usr/bin/env python
"""
Скрипт для удаления всех упоминаний менеджера из кода.
"""

import re
from pathlib import Path

def replace_in_file(file_path, replacements):
    """Замена текста в файле."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Обновлен: {file_path}")
        return True
    return False

# Файлы для обработки
files_to_process = [
    'inventory/views.py',
    'orders/views.py',
    'reports/views.py',
]

# Замены
replacements = [
    (' or request.user.is_manager', ''),
    (' or user.is_manager', ''),
    ('request.user.is_manager or ', ''),
    ('user.is_manager or ', ''),
    (' or request.user.is_manager or', ' or'),
]

base_dir = Path(__file__).parent

for file_name in files_to_process:
    file_path = base_dir / file_name
    if file_path.exists():
        replace_in_file(file_path, replacements)
    else:
        print(f"✗ Не найден: {file_path}")

print("\nГотово!")
