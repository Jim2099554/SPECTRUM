"""
Script de limpieza automática de código para SENTINELA
Elimina:
- Prints de debug (excepto en scripts de utilidad)
- Console.logs innecesarios
- Código comentado obsoleto
"""

import os
import re
from pathlib import Path


def clean_python_file(file_path: Path) -> tuple[int, list]:
    """Limpiar archivo Python"""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        removed_count = 0
        
        for i, line in enumerate(lines, 1):
            # Mantener prints en scripts de utilidad
            if 'scripts/' in str(file_path) and 'print(' in line:
                new_lines.append(line)
                continue
            
            # Eliminar prints de debug en código de producción
            if 'print(' in line and 'logger' not in line and 'scripts/' not in str(file_path):
                # Verificar si es un print de debug obvio
                if any(debug_word in line.lower() for debug_word in ['debug', 'test', 'todo', 'fixme', '[debug]']):
                    changes.append(f"Línea {i}: Eliminado print de debug")
                    removed_count += 1
                    continue
            
            new_lines.append(line)
        
        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        
        return removed_count, changes
    
    except Exception as e:
        return 0, [f"Error: {e}"]


def clean_typescript_file(file_path: Path) -> tuple[int, list]:
    """Limpiar archivo TypeScript/JavaScript"""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        removed_count = 0
        
        for i, line in enumerate(lines, 1):
            # Eliminar console.log de debug
            if 'console.log' in line:
                # Mantener solo si es parte de manejo de errores crítico
                if 'error' not in line.lower() and 'catch' not in line.lower():
                    changes.append(f"Línea {i}: Eliminado console.log")
                    removed_count += 1
                    continue
            
            new_lines.append(line)
        
        if removed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        
        return removed_count, changes
    
    except Exception as e:
        return 0, [f"Error: {e}"]


def remove_commented_code(file_path: Path) -> tuple[int, list]:
    """Eliminar bloques grandes de código comentado"""
    changes = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        in_comment_block = False
        comment_block_start = 0
        consecutive_comments = 0
        removed_blocks = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detectar comentarios
            is_comment = (stripped.startswith('#') or stripped.startswith('//')) and len(stripped) > 2
            
            if is_comment:
                consecutive_comments += 1
                if consecutive_comments == 1:
                    comment_block_start = i
            else:
                # Si terminó un bloque de comentarios largo
                if consecutive_comments > 10:
                    # Verificar si es código comentado vs documentación
                    block = lines[comment_block_start:i]
                    if any(keyword in ''.join(block).lower() for keyword in ['def ', 'class ', 'import ', 'return ', 'if ', 'for ']):
                        changes.append(f"Líneas {comment_block_start+1}-{i}: Eliminado bloque de código comentado")
                        removed_blocks += 1
                        # No agregar estas líneas
                        consecutive_comments = 0
                        continue
                
                consecutive_comments = 0
            
            new_lines.append(line)
        
        if removed_blocks > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
        
        return removed_blocks, changes
    
    except Exception as e:
        return 0, [f"Error: {e}"]


def main():
    """Función principal"""
    root_path = Path(__file__).parent.parent.parent
    
    print("🧹 Iniciando limpieza de código...")
    print(f"📁 Ruta: {root_path}\n")
    
    total_changes = 0
    files_modified = 0
    
    # Limpiar backend
    print("🐍 Limpiando backend (Python)...")
    backend_path = root_path / 'backend'
    if backend_path.exists():
        for file_path in backend_path.rglob('*.py'):
            if any(ignore in str(file_path) for ignore in ['venv', '__pycache__', '.git']):
                continue
            
            removed, changes = clean_python_file(file_path)
            if removed > 0:
                print(f"  ✓ {file_path.name}: {removed} líneas eliminadas")
                total_changes += removed
                files_modified += 1
    
    # Limpiar frontend
    print("\n⚛️  Limpiando frontend (TypeScript/React)...")
    frontend_path = root_path / 'frontend' / 'src'
    if frontend_path.exists():
        for file_path in frontend_path.rglob('*'):
            if file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                if 'node_modules' in str(file_path):
                    continue
                
                removed, changes = clean_typescript_file(file_path)
                if removed > 0:
                    print(f"  ✓ {file_path.name}: {removed} console.logs eliminados")
                    total_changes += removed
                    files_modified += 1
    
    print("\n" + "=" * 60)
    print("RESUMEN DE LIMPIEZA")
    print("=" * 60)
    print(f"\n✅ Archivos modificados: {files_modified}")
    print(f"✅ Total de cambios: {total_changes}")
    
    if total_changes > 0:
        print("\n🎉 Limpieza completada exitosamente")
        print("💡 Se recomienda ejecutar tests para verificar que todo funciona")
    else:
        print("\n✅ No se encontraron elementos para limpiar")


if __name__ == "__main__":
    main()
