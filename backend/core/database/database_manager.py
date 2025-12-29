"""
Sistema de gestión de múltiples bases de datos para SENTINELA
Permite conectar y consultar diferentes fuentes de datos usando PIN como clave principal
"""

import json
import os
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseAdapter(ABC):
    """Clase base para adaptadores de bases de datos"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connection = None
        self.is_required = config.get('required', False)
        self.is_connected = False
    
    @abstractmethod
    def connect(self) -> bool:
        """Establecer conexión con la base de datos"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Cerrar conexión"""
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """Probar si la conexión funciona"""
        pass
    
    @abstractmethod
    def search_by_pin(self, pin: str) -> Optional[Dict[str, Any]]:
        """Buscar información por PIN"""
        pass
    
    @abstractmethod
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Buscar información por nombre"""
        pass


class MySQLAdapter(DatabaseAdapter):
    """Adaptador para bases de datos MySQL"""
    
    def connect(self) -> bool:
        try:
            import mysql.connector
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config.get('port', 3306),
                database=self.config['database'],
                user=self.config['username'],
                password=self.config['password']
            )
            self.is_connected = True
            logger.info(f"✅ Conectado a MySQL: {self.config['database']}")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando a MySQL: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.is_connected = False
    
    def test_connection(self) -> bool:
        try:
            if not self.is_connected:
                return self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"❌ Error probando conexión MySQL: {e}")
            return False
    
    def search_by_pin(self, pin: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            table = self.config['tables'].get('inmates', 'inmates')
            pin_field = self.config['fields_mapping'].get('pin', 'pin')
            
            query = f"SELECT * FROM {table} WHERE {pin_field} = %s"
            cursor.execute(query, (pin,))
            result = cursor.fetchone()
            cursor.close()
            
            return result
        except Exception as e:
            logger.error(f"❌ Error buscando por PIN en MySQL: {e}")
            return None
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor(dictionary=True)
            table = self.config['tables'].get('inmates', 'inmates')
            name_field = self.config['fields_mapping'].get('nombre', 'nombre')
            
            query = f"SELECT * FROM {table} WHERE {name_field} LIKE %s"
            cursor.execute(query, (f"%{name}%",))
            results = cursor.fetchall()
            cursor.close()
            
            return results
        except Exception as e:
            logger.error(f"❌ Error buscando por nombre en MySQL: {e}")
            return []


class PostgreSQLAdapter(DatabaseAdapter):
    """Adaptador para bases de datos PostgreSQL"""
    
    def connect(self) -> bool:
        try:
            import psycopg2
            self.connection = psycopg2.connect(
                host=self.config['host'],
                port=self.config.get('port', 5432),
                database=self.config['database'],
                user=self.config['username'],
                password=self.config['password']
            )
            self.is_connected = True
            logger.info(f"✅ Conectado a PostgreSQL: {self.config['database']}")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando a PostgreSQL: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.is_connected = False
    
    def test_connection(self) -> bool:
        try:
            if not self.is_connected:
                return self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"❌ Error probando conexión PostgreSQL: {e}")
            return False
    
    def search_by_pin(self, pin: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            table = self.config['tables'].get('calls', 'calls')
            search_fields = self.config.get('search_fields', ['pin'])
            
            # Buscar en todos los campos posibles
            conditions = " OR ".join([f"{field} = %s" for field in search_fields])
            query = f"SELECT * FROM {table} WHERE {conditions}"
            cursor.execute(query, tuple([pin] * len(search_fields)))
            
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return dict(zip(columns, row))
            return None
        except Exception as e:
            logger.error(f"❌ Error buscando por PIN en PostgreSQL: {e}")
            return None
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            table = self.config['tables'].get('calls', 'calls')
            
            query = f"SELECT * FROM {table} WHERE caller_name ILIKE %s"
            cursor.execute(query, (f"%{name}%",))
            
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"❌ Error buscando por nombre en PostgreSQL: {e}")
            return []


class SQLiteAdapter(DatabaseAdapter):
    """Adaptador para bases de datos SQLite"""
    
    def connect(self) -> bool:
        try:
            import sqlite3
            db_path = self.config.get('database', 'database.db')
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            self.is_connected = True
            logger.info(f"✅ Conectado a SQLite: {db_path}")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando a SQLite: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.is_connected = False
    
    def test_connection(self) -> bool:
        try:
            if not self.is_connected:
                return self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"❌ Error probando conexión SQLite: {e}")
            return False
    
    def search_by_pin(self, pin: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            table = self.config['tables'].get('inmates', 'inmates')
            pin_field = self.config['fields_mapping'].get('pin', 'pin')
            
            query = f"SELECT * FROM {table} WHERE {pin_field} = ?"
            cursor.execute(query, (pin,))
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"❌ Error buscando por PIN en SQLite: {e}")
            return None
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            table = self.config['tables'].get('inmates', 'inmates')
            name_field = self.config['fields_mapping'].get('nombre', 'nombre')
            
            query = f"SELECT * FROM {table} WHERE {name_field} LIKE ?"
            cursor.execute(query, (f"%{name}%",))
            rows = cursor.fetchall()
            cursor.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"❌ Error buscando por nombre en SQLite: {e}")
            return []


class MSSQLAdapter(DatabaseAdapter):
    """Adaptador para bases de datos Microsoft SQL Server"""
    
    def connect(self) -> bool:
        try:
            import pyodbc
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.config['host']},{self.config.get('port', 1433)};"
                f"DATABASE={self.config['database']};"
                f"UID={self.config['username']};"
                f"PWD={self.config['password']}"
            )
            self.connection = pyodbc.connect(conn_str)
            self.is_connected = True
            logger.info(f"✅ Conectado a MSSQL: {self.config['database']}")
            return True
        except Exception as e:
            logger.error(f"❌ Error conectando a MSSQL: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.is_connected = False
    
    def test_connection(self) -> bool:
        try:
            if not self.is_connected:
                return self.connect()
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"❌ Error probando conexión MSSQL: {e}")
            return False
    
    def search_by_pin(self, pin: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            table = self.config['tables'].get('cases', 'cases')
            search_fields = self.config.get('search_fields', ['pin'])
            
            conditions = " OR ".join([f"{field} = ?" for field in search_fields])
            query = f"SELECT * FROM {table} WHERE {conditions}"
            cursor.execute(query, tuple([pin] * len(search_fields)))
            
            columns = [column[0] for column in cursor.description]
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return dict(zip(columns, row))
            return None
        except Exception as e:
            logger.error(f"❌ Error buscando por PIN en MSSQL: {e}")
            return None
    
    def search_by_name(self, name: str) -> List[Dict[str, Any]]:
        try:
            cursor = self.connection.cursor()
            table = self.config['tables'].get('cases', 'cases')
            
            query = f"SELECT * FROM {table} WHERE nombre_investigado LIKE ?"
            cursor.execute(query, (f"%{name}%",))
            
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.error(f"❌ Error buscando por nombre en MSSQL: {e}")
            return []


class DatabaseManager:
    """Gestor central de todas las bases de datos"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 
            '../../config/database_config.json'
        )
        self.adapters: Dict[str, DatabaseAdapter] = {}
        self.ppl_adapter: Optional[DatabaseAdapter] = None
        self.load_config()
    
    def load_config(self):
        """Cargar configuración de bases de datos"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            for db_name, db_config in config.get('databases', {}).items():
                adapter = self._create_adapter(db_config)
                if adapter:
                    self.adapters[db_name] = adapter
                    
                    # Guardar adaptador PPL como principal
                    if db_name == 'ppl':
                        self.ppl_adapter = adapter
            
            logger.info(f"✅ Configuración cargada: {len(self.adapters)} bases de datos")
        except FileNotFoundError:
            logger.warning(f"⚠️  Archivo de configuración no encontrado: {self.config_path}")
        except Exception as e:
            logger.error(f"❌ Error cargando configuración: {e}")
    
    def _create_adapter(self, config: Dict[str, Any]) -> Optional[DatabaseAdapter]:
        """Crear adaptador según el tipo de base de datos"""
        db_type = config.get('type', '').lower()
        
        adapters_map = {
            'mysql': MySQLAdapter,
            'postgresql': PostgreSQLAdapter,
            'postgres': PostgreSQLAdapter,
            'mssql': MSSQLAdapter,
            'sqlserver': MSSQLAdapter,
            'sqlite': SQLiteAdapter,
            'sqlite3': SQLiteAdapter
        }
        
        adapter_class = adapters_map.get(db_type)
        if adapter_class:
            return adapter_class(config)
        else:
            logger.error(f"❌ Tipo de base de datos no soportado: {db_type}")
            return None
    
    def connect_all(self) -> Dict[str, bool]:
        """Conectar a todas las bases de datos configuradas"""
        results = {}
        
        # Primero conectar a PPL (obligatoria)
        if self.ppl_adapter:
            results['ppl'] = self.ppl_adapter.connect()
            if not results['ppl']:
                logger.error("❌ No se pudo conectar a la base de datos PPL (obligatoria)")
                return results
        else:
            logger.error("❌ Base de datos PPL no configurada")
            return {'ppl': False}
        
        # Luego conectar a las demás (opcionales)
        for name, adapter in self.adapters.items():
            if name != 'ppl':
                results[name] = adapter.connect()
                if not results[name] and adapter.is_required:
                    logger.warning(f"⚠️  Base de datos requerida no disponible: {name}")
        
        return results
    
    def get_complete_profile(self, pin: str) -> Dict[str, Any]:
        """
        Obtener perfil completo de un PPL desde todas las bases de datos
        
        Flujo:
        1. Buscar en BD PPL por PIN (obligatorio)
        2. Obtener nombre del PPL
        3. Buscar en otras BDs usando PIN y nombre
        4. Consolidar toda la información
        """
        profile = {
            'pin': pin,
            'ppl_data': None,
            'pbx_data': None,
            'carpetas_data': None,
            'other_data': {},
            'errors': []
        }
        
        # 1. Buscar en BD PPL (obligatorio)
        if not self.ppl_adapter or not self.ppl_adapter.is_connected:
            profile['errors'].append("Base de datos PPL no disponible")
            return profile
        
        ppl_data = self.ppl_adapter.search_by_pin(pin)
        if not ppl_data:
            profile['errors'].append(f"PIN {pin} no encontrado en base de datos PPL")
            return profile
        
        profile['ppl_data'] = ppl_data
        
        # Obtener nombre del PPL
        nombre_field = self.ppl_adapter.config['fields_mapping'].get('nombre', 'nombre')
        nombre = ppl_data.get(nombre_field, '')
        
        # 2. Buscar en otras bases de datos
        for db_name, adapter in self.adapters.items():
            if db_name == 'ppl' or not adapter.is_connected:
                continue
            
            try:
                # Buscar por PIN
                data_by_pin = adapter.search_by_pin(pin)
                
                # Buscar por nombre si está disponible
                data_by_name = []
                if nombre:
                    data_by_name = adapter.search_by_name(nombre)
                
                # Guardar resultados
                if db_name == 'pbx':
                    profile['pbx_data'] = {
                        'by_pin': data_by_pin,
                        'by_name': data_by_name
                    }
                elif db_name == 'carpetas':
                    profile['carpetas_data'] = {
                        'by_pin': data_by_pin,
                        'by_name': data_by_name
                    }
                else:
                    profile['other_data'][db_name] = {
                        'by_pin': data_by_pin,
                        'by_name': data_by_name
                    }
            except Exception as e:
                profile['errors'].append(f"Error consultando {db_name}: {str(e)}")
        
        return profile
    
    def disconnect_all(self):
        """Desconectar todas las bases de datos"""
        for adapter in self.adapters.values():
            adapter.disconnect()
        logger.info("✅ Todas las conexiones cerradas")


# Singleton para uso global
_database_manager_instance = None

def get_database_manager() -> DatabaseManager:
    """Obtener instancia única del gestor de bases de datos"""
    global _database_manager_instance
    if _database_manager_instance is None:
        _database_manager_instance = DatabaseManager()
    return _database_manager_instance
