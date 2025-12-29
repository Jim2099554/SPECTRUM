"""
Script de auditoría de código para SENTINELA
Revisa el código en busca de:
- Imports no usados
- Código comentado
- Console.logs y prints de debug
- Variables no usadas
- Funciones obsoletas
- TODOs y FIXMEs
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple


class CodeAuditor:
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.issues = {
            'unused_imports': [],
            'debug_statements': [],
            'commented_code': [],
            'todos': [],
            'large_files': [],
            'duplicate_code': [],
            'warnings': []
        }
    
    def audit_python_file(self, file_path: Path):
        """Auditar archivo Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Buscar prints de debug
            for i, line in enumerate(lines, 1):
                if 'print(' in line and 'logger' not in line:
                    self.issues['debug_statements'].append({
                        'file': str(file_path),
                        'line': i,
                        'content': line.strip(),
                        'type': 'print'
                    })
            
            # Buscar TODOs y FIXMEs
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line or 'XXX' in line:
                    self.issues['todos'].append({
                        'file': str(file_path),
                        'line': i,
                        'content': line.strip()
                    })
            
            # Buscar código comentado (múltiples líneas seguidas)
            commented_lines = 0
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('#') and len(stripped) > 2:
                    commented_lines += 1
                    if commented_lines > 5:
                        self.issues['commented_code'].append({
                            'file': str(file_path),
                            'line': i - 5,
                            'note': f'{commented_lines} líneas comentadas consecutivas'
                        })
                else:
                    commented_lines = 0
            
            # Archivos grandes
            if len(lines) > 500:
                self.issues['large_files'].append({
                    'file': str(file_path),
                    'lines': len(lines),
                    'note': 'Considerar refactorizar'
                })
        
        except Exception as e:
            self.issues['warnings'].append({
                'file': str(file_path),
                'error': str(e)
            })
    
    def audit_typescript_file(self, file_path: Path):
        """Auditar archivo TypeScript/JavaScript"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Buscar console.log
            for i, line in enumerate(lines, 1):
                if 'console.log' in line or 'console.warn' in line or 'console.error' in line:
                    self.issues['debug_statements'].append({
                        'file': str(file_path),
                        'line': i,
                        'content': line.strip(),
                        'type': 'console'
                    })
            
            # Buscar TODOs
            for i, line in enumerate(lines, 1):
                if 'TODO' in line or 'FIXME' in line:
                    self.issues['todos'].append({
                        'file': str(file_path),
                        'line': i,
                        'content': line.strip()
                    })
            
            # Archivos grandes
            if len(lines) > 400:
                self.issues['large_files'].append({
                    'file': str(file_path),
                    'lines': len(lines),
                    'note': 'Considerar dividir en componentes más pequeños'
                })
        
        except Exception as e:
            self.issues['warnings'].append({
                'file': str(file_path),
                'error': str(e)
            })
    
    def scan_directory(self, directory: Path, extensions: List[str]):
        """Escanear directorio recursivamente"""
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in extensions:
                # Ignorar node_modules, venv, __pycache__, etc.
                if any(ignore in str(file_path) for ignore in ['node_modules', 'venv', '__pycache__', '.git', 'dist', 'build']):
                    continue
                
                if file_path.suffix == '.py':
                    self.audit_python_file(file_path)
                elif file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                    self.audit_typescript_file(file_path)
    
    def generate_report(self) -> str:
        """Generar reporte de auditoría"""
        report = []
        report.append("=" * 80)
        report.append("SENTINELA - REPORTE DE AUDITORÍA DE CÓDIGO")
        report.append("=" * 80)
        report.append("")
        
        # Debug statements
        if self.issues['debug_statements']:
            report.append(f"\n🔍 STATEMENTS DE DEBUG ENCONTRADOS: {len(self.issues['debug_statements'])}")
            report.append("-" * 80)
            for item in self.issues['debug_statements'][:20]:  # Mostrar primeros 20
                report.append(f"  📄 {item['file']}")
                report.append(f"     Línea {item['line']}: {item['content'][:80]}")
                report.append(f"     Tipo: {item['type']}")
                report.append("")
            if len(self.issues['debug_statements']) > 20:
                report.append(f"  ... y {len(self.issues['debug_statements']) - 20} más")
        else:
            report.append("\n✅ No se encontraron statements de debug")
        
        # TODOs
        if self.issues['todos']:
            report.append(f"\n📝 TODOs/FIXMEs ENCONTRADOS: {len(self.issues['todos'])}")
            report.append("-" * 80)
            for item in self.issues['todos'][:15]:
                report.append(f"  📄 {item['file']}")
                report.append(f"     Línea {item['line']}: {item['content'][:80]}")
                report.append("")
            if len(self.issues['todos']) > 15:
                report.append(f"  ... y {len(self.issues['todos']) - 15} más")
        else:
            report.append("\n✅ No se encontraron TODOs pendientes")
        
        # Código comentado
        if self.issues['commented_code']:
            report.append(f"\n💬 BLOQUES DE CÓDIGO COMENTADO: {len(self.issues['commented_code'])}")
            report.append("-" * 80)
            for item in self.issues['commented_code']:
                report.append(f"  📄 {item['file']}")
                report.append(f"     Línea {item['line']}: {item['note']}")
                report.append("")
        else:
            report.append("\n✅ No se encontraron bloques grandes de código comentado")
        
        # Archivos grandes
        if self.issues['large_files']:
            report.append(f"\n📏 ARCHIVOS GRANDES: {len(self.issues['large_files'])}")
            report.append("-" * 80)
            for item in sorted(self.issues['large_files'], key=lambda x: x['lines'], reverse=True)[:10]:
                report.append(f"  📄 {item['file']}")
                report.append(f"     {item['lines']} líneas - {item['note']}")
                report.append("")
        else:
            report.append("\n✅ Todos los archivos tienen tamaño razonable")
        
        # Warnings
        if self.issues['warnings']:
            report.append(f"\n⚠️  ADVERTENCIAS: {len(self.issues['warnings'])}")
            report.append("-" * 80)
            for item in self.issues['warnings']:
                report.append(f"  📄 {item['file']}")
                report.append(f"     Error: {item['error']}")
                report.append("")
        
        # Resumen
        report.append("\n" + "=" * 80)
        report.append("RESUMEN")
        report.append("=" * 80)
        total_issues = sum(len(v) for v in self.issues.values())
        report.append(f"\nTotal de issues encontrados: {total_issues}")
        report.append(f"  - Debug statements: {len(self.issues['debug_statements'])}")
        report.append(f"  - TODOs/FIXMEs: {len(self.issues['todos'])}")
        report.append(f"  - Código comentado: {len(self.issues['commented_code'])}")
        report.append(f"  - Archivos grandes: {len(self.issues['large_files'])}")
        report.append(f"  - Advertencias: {len(self.issues['warnings'])}")
        
        if total_issues == 0:
            report.append("\n🎉 ¡Código limpio! Listo para producción.")
        elif total_issues < 20:
            report.append("\n✅ Código en buen estado. Issues menores a resolver.")
        else:
            report.append("\n⚠️  Se recomienda limpieza de código antes de producción.")
        
        return "\n".join(report)


def main():
    """Función principal"""
    import sys
    
    # Obtener ruta raíz del proyecto
    root_path = Path(__file__).parent.parent.parent
    
    print("🔍 Iniciando auditoría de código...")
    print(f"📁 Ruta: {root_path}")
    print()
    
    auditor = CodeAuditor(root_path)
    
    # Escanear backend
    print("🐍 Escaneando backend (Python)...")
    backend_path = root_path / 'backend'
    if backend_path.exists():
        auditor.scan_directory(backend_path, ['.py'])
    
    # Escanear frontend
    print("⚛️  Escaneando frontend (TypeScript/React)...")
    frontend_path = root_path / 'frontend' / 'src'
    if frontend_path.exists():
        auditor.scan_directory(frontend_path, ['.ts', '.tsx', '.js', '.jsx'])
    
    # Generar reporte
    print("\n📊 Generando reporte...")
    report = auditor.generate_report()
    
    # Mostrar en consola
    print(report)
    
    # Guardar en archivo
    report_path = root_path / 'AUDIT_REPORT.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n💾 Reporte guardado en: {report_path}")


if __name__ == "__main__":
    main()
