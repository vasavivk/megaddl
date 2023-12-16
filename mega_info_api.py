import re
import json 
from requests import post
import base64
import struct
import codecs
from Crypto.Cipher import AES
from math import floor,pow,log
#pycryptodome>=3.9.6
def size(num, suffix='B'):
    magnitude = int(floor(log(num, 1024)))
    val = num / pow(1024, magnitude)
    return '{:3.1f} {}{}'.format(val, ['', ' K', 'M', 'G', 'T'][magnitude], suffix)
# pattern = r"(folder|file)/(.+?)#([^\s]+)"
def makebyte(x):
    return codecs.latin_1_encode(x)[0]

def makestring(x):
    return codecs.latin_1_decode(x)[0]

def base64_to_a32(s):
    return str_to_a32(base64_url_decode(s))

def base64_url_decode(data):
    data += '=='[(2 - len(data) * 3) % 4:]
    for search, replace in (('-', '+'), ('_', '/'), (',', '')):
        data = data.replace(search, replace)
    return base64.b64decode(data)

def str_to_a32(b):
    if isinstance(b, str):
        b = makebyte(b)
    if len(b) % 4:
        # pad to multiple of 4
        b += b'\0' * (4 - len(b) % 4)
    return struct.unpack('>%dI' % (len(b) / 4), b)

def a32_to_str(a):
    return struct.pack('>%dI' % len(a), *a)

def decrypt_attr(attr, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = makestring(attr)
    attr = attr.rstrip('\0')
    return json.loads(attr[4:]) if attr[:6] == 'MEGA{"' else False

def aes_cbc_decrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.decrypt(data)

def get_mega_info(url):
    pattern = r"file/(.+?)#(.+)"
    match = re.search(pattern, url)
    file_id,file_key = match.group(1),match.group(2)
    data = {"a": "g", "g": 1, "ssl": 2,  'ssm': 1,"p": file_id}
    resp = post(f"https://eu.api.mega.co.nz/cs?domain=meganz&lang=en",data=json.dumps([data]))
    key = base64_to_a32(file_key)
    k = (key[0] ^ key[4], key[1] ^ key[5], key[2] ^ key[6],
             key[3] ^ key[7])
    unencrypted_attrs = decrypt_attr(base64_url_decode(resp.json()[0]["at"]), k)
    return unencrypted_attrs['n'], resp.json()[0]["g"], size(resp.json()[0]["s"])
if __name__ == "__main__":
    url = input("URL: ")
    name,dl,size = get_mega_info(url)
    print(name,dl,size)
    
