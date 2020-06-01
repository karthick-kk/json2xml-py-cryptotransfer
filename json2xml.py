import json
import os
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def encrypt(key, filename):
    chunksize = 64 * 1024
    outputFile = filename+"_encrypted"
    filesize = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)

    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

def getKey(password):
    hasher = SHA256.new(password.encode('utf-8'))
    return hasher.digest()

def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)

## Perform target cleanup
entries = os.listdir('/dest')
for entry in entries:
    exfile="/dest/"+entry
    if os.path.exists(exfile):
        os.remove(exfile)

## Read, convert and encrypt files
entries = os.listdir('/src')
password="keepitsecure"
for entry in entries:
    jsonfile="/src/"+entry
    with open(jsonfile, 'r') as f:
        jsonString = f.read()
    j = json.loads(jsonString)
    xmlString = json2xml(j)
    outfile="/dest/"+entry.split(".")[0]+".xml"

    with open(outfile, 'w') as f:
        f.write(xmlString)
    print(outfile)
    encrypt(getKey(password), outfile)
    if os.path.exists(outfile):
        os.remove(outfile)
