import json
import os
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

def decrypt(key, filename):
    chunksize = 64 * 1024
    outputFile="/dest/"+entry.split("_")[0]
#    outputFile = filename[11:]

    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        IV = infile.read(16)

        decryptor = AES.new(key, AES.MODE_CBC, IV)

        with open(outputFile, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break

                outfile.write(decryptor.decrypt(chunk))
            outfile.truncate(filesize)


def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()


entries = os.listdir('/dest')
password="keepitsecure"
for entry in entries:
    encfile="/dest/"+entry

    decrypt(getKey(password), encfile)
