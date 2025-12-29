from cryptography.fernet import Fernet
import os
import tempfile
from typing import Optional, Tuple

def generate_key():
    return Fernet.generate_key()

def get_key() -> bytes:
    from backend.config import ENCRYPTION_KEY
    if not ENCRYPTION_KEY:
        raise ValueError('ENCRYPTION_KEY environment variable not set')
    return ENCRYPTION_KEY.encode()

def encrypt_data(data: str) -> bytes:
    cipher = Fernet(get_key())
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, key: Optional[bytes] = None) -> str:
    cipher = Fernet(key or get_key())
    decrypted = cipher.decrypt(encrypted_data)
    return decrypted.decode('utf-8')

def encrypt_file(input_path: str, output_path: str) -> None:
    with open(input_path, 'rb') as f:
        data = f.read()
    encrypted_data = encrypt_data(data.decode(errors='replace'))
    with open(output_path, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(input_path: str, output_path: str) -> None:
    with open(input_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data)
    with open(output_path, 'wb') as f:
        f.write(decrypted_data.encode())

# Secure temp file handling        
def secure_tempfile(prefix: str = 'spectrum') -> Tuple[str, bytes]:
    """Create encrypted temporary file"""
    fd, path = tempfile.mkstemp(prefix=prefix)
    os.close(fd)
    return path, get_key()
