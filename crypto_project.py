import os
import base64
import sys
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class CryptoLab:
    """
    Enhanced Cryptography Lab with File Support and Interactive Menu.
    """

    @staticmethod
    def sha256_hash(text: str) -> str:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(text.encode())
        return digest.finalize().hex()

    class AESCipher:
        def __init__(self, password: str):
            # Static salt for education; use unique salt per file in production
            self.salt = b'\x00' * 16 
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
                backend=default_backend()
            )
            self.key = kdf.derive(password.encode())

        def encrypt_data(self, data: bytes) -> bytes:
            iv = os.urandom(12)
            encryptor = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv),
                backend=default_backend()
            ).encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            # Return IV + Tag + Ciphertext as a single blob
            return iv + encryptor.tag + ciphertext

        def decrypt_data(self, blob: bytes) -> bytes:
            iv = blob[:12]
            tag = blob[12:28]
            ciphertext = blob[28:]
            decryptor = Cipher(
                algorithms.AES(self.key),
                modes.GCM(iv, tag),
                backend=default_backend()
            ).decryptor()
            return decryptor.update(ciphertext) + decryptor.finalize()

    class RSACipher:
        def __init__(self):
            self.private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            )
            self.public_key = self.private_key.public_key()

        def encrypt(self, message: str) -> str:
            ct = self.public_key.encrypt(
                message.encode(),
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            )
            return base64.b64encode(ct).decode()

        def decrypt(self, ct_b64: str) -> str:
            ct = base64.b64decode(ct_b64)
            return self.private_key.decrypt(
                ct,
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
            ).decode()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    lab = CryptoLab()
    rsa_instance = None # Lazy load RSA to save time
    
    while True:
        print("\n" + "="*40)
        print("      CRYPTOGRAPHY ALGORITHMS LAB")
        print("="*40)
        print("1. SHA-256 Hashing (Integrity)")
        print("2. AES-GCM (Symmetric Encryption)")
        print("3. RSA-2048 (Asymmetric Encryption)")
        print("4. File Encryptor (Secure local files)")
        print("5. Exit")
        print("="*40)
        
        choice = input("Select an option (1-5): ")

        if choice == '1':
            text = input("\nEnter text to hash: ")
            print(f"Result: {CryptoLab.sha256_hash(text)}")

        elif choice == '2':
            pwd = input("Enter secret password: ")
            msg = input("Enter message to encrypt: ")
            aes = CryptoLab.AESCipher(pwd)
            encrypted = aes.encrypt_data(msg.encode())
            enc_b64 = base64.b64encode(encrypted).decode()
            print(f"\nEncrypted (Base64): {enc_b64}")
            
            if input("\nDecrypt now? (y/n): ").lower() == 'y':
                print(f"Decrypted Result: {aes.decrypt_data(encrypted).decode()}")

        elif choice == '3':
            if not rsa_instance:
                print("Generating 2048-bit RSA keys... please wait.")
                rsa_instance = CryptoLab.RSACipher()
            msg = input("Enter message for RSA encryption: ")
            encrypted = rsa_instance.encrypt(msg)
            print(f"\nEncrypted (RSA): {encrypted[:60]}...")
            print(f"Decrypted Result: {rsa_instance.decrypt(encrypted)}")

        elif choice == '4':
            file_path = input("\nEnter full path of the file (e.g., test.txt): ")
            if not os.path.exists(file_path):
                print("File not found!")
                continue
            
            action = input("Encrypt or Decrypt? (e/d): ").lower()
            pwd = input("Enter password: ")
            aes = CryptoLab.AESCipher(pwd)
            
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                if action == 'e':
                    processed_data = aes.encrypt_data(data)
                    new_path = file_path + ".enc"
                else:
                    processed_data = aes.decrypt_data(data)
                    new_path = file_path.replace(".enc", ".dec")
                
                with open(new_path, 'wb') as f:
                    f.write(processed_data)
                print(f"Success! Saved to: {new_path}")
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()