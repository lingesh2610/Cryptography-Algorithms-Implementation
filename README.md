Cryptography Algorithms Implementation

A comprehensive Python-based laboratory for exploring and implementing modern cryptographic primitives including Hashing (SHA-256), Symmetric Encryption (AES-GCM), and Asymmetric Encryption (RSA).

🚀 Features

SHA-256 Hashing: Generate deterministic, one-way cryptographic fingerprints for data integrity verification.

AES-256-GCM Symmetric Encryption: Implements authenticated encryption using Galois/Counter Mode (GCM) for high-performance data security and tampering detection.

RSA-2048 Asymmetric Encryption: Demonstrates public-key cryptography for secure messaging and key exchange.

Secure File Encryptor: A utility to encrypt and decrypt local files (TXT, PDF, Images) using password-derived keys via PBKDF2.

Interactive CLI Menu: A user-friendly command-line interface for testing algorithms in real-time.

🛠️ Tech Stack & Skills Learned

Language: Python 3.x

Library: cryptography (The industry-standard library for Python)

Concepts Learned:

Key Derivation Functions (KDF) using PBKDF2HMAC.

The importance of Initialization Vectors (IV) and Authentication Tags.

The difference between Symmetric and Asymmetric key management.

Data integrity and collision resistance in hashing.

📋 Prerequisites

Before running the project, ensure you have the cryptography library installed:

pip install cryptography


📂 Project Structure

crypto_project.py: The main application containing the logic for all algorithms and the interactive menu.

secret.txt: A sample file used for testing the file encryption module.

venv/: Virtual environment folder (local).

🖥️ Usage

Start the Lab:

python crypto_project.py


Hashing: Select Option 1 to see how text is converted into a unique SHA-256 hash.

AES Encryption: Select Option 2 to encrypt text with a password.

RSA Encryption: Select Option 3 to generate a key-pair and encrypt a message that only the private key can decrypt.

File Encryption:

Select Option 4.

Enter secret.txt.

Choose e to encrypt.

Enter a secure password.

Note the creation of secret.txt.enc.

🔒 Security Notes

This project uses AES-GCM, which provides both confidentiality and authenticity.

Passwords are never used directly; they are transformed into 256-bit keys using PBKDF2 with 100,000 iterations to protect against brute-force attacks.

RSA uses OAEP padding, which is the modern standard for secure asymmetric encryption.

Created as part of my Cryptography Internship Project.
