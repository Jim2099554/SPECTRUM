from utils.crypto import encrypt_data, decrypt_data, encrypt_file, decrypt_file
import os

# Local storage functions can be added here if needed, for now all operations are local file reads/writes.

def test_encryption():
    original_text = "TOP SECRET: Drug operation at 34th street"
    try:
        encrypted = encrypt_data(original_text)
        decrypted = decrypt_data(encrypted)
        
        with open("test_clear.txt", "w") as f:
            f.write(original_text)
        
        encrypt_file("test_clear.txt", "test_encrypted.bin")
        decrypt_file("test_encrypted.bin", "test_decrypted.txt")
        
        with open("test_decrypted.txt") as f:
            decrypted_file_text = f.read()
        
        os.remove("test_clear.txt")
        os.remove("test_encrypted.bin")
        os.remove("test_decrypted.txt")
        
        return decrypted == original_text and decrypted_file_text == original_text
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔒 Encryption Test Result:", test_encryption())
