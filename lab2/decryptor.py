# Ciber Forensics Course IST-MEIC ==> Group XX <==
# ================================================
# This is a decryptor script to allow restore files
# that have been encrypted by Jason Halloween malware (ransomware)
#
#
# TIPS: The cryptographic algorithm used by the malware was AES in 
#       AES_CTR_MODE with a 128 bit key size. The initial value for
#       the AES counter corresponds to the first 128 bits of each 
#       encrypted file.
import os
import array
from Crypto.Cipher import AES
from base64 import b64decode
from Crypto.Util import Counter
from Crypto.Util.number import bytes_to_long
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KNOWN_KEY = b'47683b9a9663c065353437b35c5d8519'
MODE      = AES.MODE_CTR

def decrypt_file(path, newpath):
    #We need to fetch the first 128 bits of the file to be used as
    # initialization vector
    f = open(path, "rb")
    
    #Just read a whole 128 bits = 16 bytes
    value = f.read(16)

    counter = Counter.new(128, initial_value = bytes_to_long(value))

    decrypt_engine = AES.new(KNOWN_KEY, MODE, counter=counter)
    f.seek(0)
    file_content = f.read()
    
    f.close()
    file_data = decrypt_engine.decrypt(file_content)

    f = open(newpath, "wb")
    f.write(file_data)
    f.close()


    
