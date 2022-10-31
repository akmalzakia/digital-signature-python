import hashlib
import os
import rsa

keystore = 'keys/'

def display_commands():
  print("List of commands:")
  print("1. sign \{document\}")
  print("2. verify \{document\}")
  print("3. generate")

def main():
  while(True):
    display_commands()
    try:
      msg = input()
      if not msg:
        continue
    except KeyboardInterrupt:
      break

    cmd = msg.split(" ")


    try:
      data = get_file(cmd[1], 'rb')
    except IndexError:
      print("Index error")
      continue
    except FileNotFoundException:
      print("File not found!")
      continue

    privateKey, publicKey = loadKeys()
    
    if cmd[0] == 'sign':
      sign(cmd[1], data, privateKey)
    elif cmd[0] == 'verify':
      print(verify(data, publicKey))
    else:
      continue

def get_file(filepath, modes):
  if os.path.isfile(filepath):
    f = open(filepath, modes)
    f_data = f.read()
    f.close()

    return f_data
  
  return FileNotFoundException

def generate_keys():
  (publicKey, privateKey) = rsa.newkeys(1024)
  with open('keys/publicKey.pem', 'wb') as p:
    p.write(publicKey.save_pkcs1('PEM'))
  with open('keys/privateKey.pem', 'wb') as p:
    p.write(privateKey.save_pkcs1('PEM'))

def loadKeys():
  with open('keys/publicKey.pem', 'rb') as p:
    publicKey = rsa.PublicKey.load_pkcs1(p.read())
  with open('keys/privateKey.pem', 'rb') as p:
    privateKey = rsa.PrivateKey.load_pkcs1(p.read())

  return privateKey, publicKey

def sign(filename, data, privateKey):
  encrypted_hash = rsa.sign(data, privateKey, 'SHA-256')
  with open('signature.rsa', 'wb') as f:
    f.write(encrypted_hash)
  return

def verify(data, publicKey):
  try:
    with open('signature.rsa', 'rb') as f:
      res = rsa.verify(data, f.read(), publicKey)
    return res
  except:
    return False

class FileNotFoundException(Exception):
  pass

main()