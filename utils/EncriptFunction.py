from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from config.JWT_config import SECRET_KEY
import os
import base64

# Secret key (must be kept safe)
# SECRET_KEY = "352a3d4ce12e41af1c098553c8ca87c854c1be987a89cf9331ea8b4c7dc076a4d3e282aeb90f89e9e98e764a5fa40f35fc7605c04f5cd53a14793145ebee4a26"
SECRET_KEY2 = bytes.fromhex(SECRET_KEY)

# Ensure the key is 32 bytes (256 bits)
if len(SECRET_KEY2) < 32:
    SECRET_KEY2 = SECRET_KEY2.ljust(32, b'\0')  # Pad with zeros if the key is shorter than 32 bytes
elif len(SECRET_KEY2) > 32:
    SECRET_KEY2 = SECRET_KEY2[:32]  # Trim the key if it is longer than 32 bytes

IV = os.urandom(16)  # Initialization vector for encryption

# Function to encrypt the client_id and generate API key
def generate_api_key(client_id):
    # Convert client_id to string and pad it
    client_id_str = str(client_id)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(client_id_str.encode('utf-8')) + padder.finalize()
    
    # Create the cipher object
    cipher = Cipher(algorithms.AES(SECRET_KEY2), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    # Combine IV and encrypted data and encode in base64
    api_key = base64.b64encode(IV + encrypted_data).decode('utf-8')
    
    return api_key

# Function to decrypt the API key back to the client_id
def decrypt_api_key(api_key):
    # Decode the base64 encoded API key
    encrypted_data = base64.b64decode(api_key)
    
    # Extract the IV and the encrypted data
    iv = encrypted_data[:16]
    encrypted_client_id = encrypted_data[16:]
    
    # Create the cipher object
    cipher = Cipher(algorithms.AES(SECRET_KEY2), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_client_id) + decryptor.finalize()
    
    # Unpad the decrypted data and return the client_id
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    return int(unpadded_data.decode('utf-8'))

# Example usage
client_id = 125
api_key = generate_api_key(client_id)
print(f"Generated API Key for client_id {client_id}: {api_key}")

# Decrypt the API key back to the client_id
decrypted_client_id = decrypt_api_key(api_key)
print(f"Decrypted client_id from API Key: {decrypted_client_id}")
