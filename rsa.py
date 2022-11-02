import hashlib
import os
import sys
from Crypto.PublicKey import RSA

default_private_path = 'keys/privateKey.pem'
default_public_path = 'keys/publicKey.pem'

def usage():
  print("Usage: rsa.py <command> <file>")
  print("Commands:")
  print("-s, -S, --sign\t\tSign a file")
  print("-v, -V, --verify\tVerify signature")

def main():
  if len(sys.argv) < 3:
    usage()
    exit(-1) 
  
  # Get token
  token = sys.argv[1]
  if token == '-V' or token == '--verify' or token == '-v':
    token = 'verify'
  elif token == '-S' or token == '--sign' or token == '-s':
    token = 'sign'
  else:
    usage()
    exit(-1)

  try:
    data = get_file(sys.argv[2], 'rb')
  except IndexError:
    print("Index error")
    return
  except FileNotFoundException:
    print("File not found!")
    return

  if check_file(default_private_path) and check_file(default_public_path):
    privateKey, publicKey = loadKeys()
    print('x')
  else:
    privateKey, publicKey = generate_keys()
  
    
  if token == 'sign':
    sign(data, privateKey)
  elif token == 'verify':
    verify(data, publicKey)
  else:
    usage()

  print(f'---- {token.upper()} PROCESS DONE ----')

def get_file(filepath, modes):
  if os.path.isfile(filepath):
    f = open(filepath, modes)
    f_data = f.read()
    f.close()

    return f_data
  
  return FileNotFoundException

def generate_keys():
  keys = RSA.generate(bits=1024)
  publicKey = keys.publickey().export_key()
  privateKey = keys.export_key()
  with open(default_public_path, 'wb') as p:
    p.write(publicKey)
  with open(default_private_path, 'wb') as p:
    p.write(privateKey)
  
  return privateKey, publicKey
  

def loadKeys():
  with open(default_public_path, 'rb') as p:
    publicKey = RSA.import_key(p.read())
  with open(default_private_path, 'rb') as p:
    privateKey = RSA.import_key(p.read())

  return privateKey, publicKey

def sign(data, privateKey):
  file = os.path.splitext(sys.argv[2])
  hashed = int.from_bytes(hashlib.sha256(data).digest(), byteorder='big')
  signature = pow(hashed, privateKey.d, privateKey.n).to_bytes(256, 'big')
  with open(f'{file[0]}_signed{file[1]}', 'wb') as f:
    f.write(data + signature)
  return

def verify(data, publicKey):
  signature = data[-256:]
  original = data[:-256]
  res = pow(int.from_bytes(signature, 'big'), publicKey.e, publicKey.n)
  hashed = int.from_bytes(hashlib.sha256(original).digest(), byteorder='big')
  if hashed == res:
    print("Verification Success --- Signature Match")
  else:
    print("Verification Failed --- Signature not match")

def check_file(filepath):
  return os.path.exists(filepath) and not os.stat(filepath).st_size == 0
class FileNotFoundException(Exception):
  pass

main()