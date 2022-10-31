import hashlib
import os
from random import getrandbits
from gmpy2 import is_prime
from gmpy2 import powmod
import decimal

L = 512
N = 160

def no_bits(p):
  return len(bin(p)) - 2

def is_valid(p,q,g):
  print(no_bits(p), no_bits(q))
  return (
    is_prime(p) and is_prime(q) and no_bits(p) == 512 and no_bits(q) == 160 and (p-1) % q == 0 and powmod(g,q,p) == 1 and g > 1
  )

def display_commands():
  print("List of commands:")
  print("1. sign \{document\}")
  print("2. verify \{document\}")

def main():
  msg = input()
  cmd = msg.split(" ")

  try:
    data = get_file(cmd[0], 'rb')
  except IndexError:
    print("Index error")
    return
  except FileNotFoundException:
    print("File not found!")
    return

  # Get resources needed for verification
  hashed = hashlib.sha256(data).hexdigest()
  p, q, g = get_dsa_parameters()

  # Get signature
  with open('dsa_signature.dsa', 'r') as f:
    params = f.read().split(':')
    r, s = int(params[0]), int(params[1])

  # Get public key
  with open('keys/dsa_y', 'r') as f:
    y = int(f.read())
  print(verify(hashed, p, q, g, r, s, y))

def get_file(filepath, modes):
  if os.path.isfile(filepath):
    f = open(filepath, modes)
    f_data = f.read()
    f.close()

    return f_data
  
  return FileNotFoundException

def get_dsa_parameters():
  # print("P value : ")
  p = 13232376895198612407547930718267435757728527029623408872245156039757713029036368719146452186041204237350521785240337048752071462798273003935646236777459223
  # print("Q value : ")
  q = 857393771208094202104259627990318636601332086981
  # print(p, q)
  g = 5421644057436475141609648488325705128047428394380474376834667300766108262613900542681289080713724597310673074119355136085795982097390670890367185141189796

  if not is_valid(p, q, g):
    print('invalid')
    exit(-1)

  return (p,q,g)


def verify(hash, p, q, g, r, s, y):
  w = pow(s, -1 , q)
  z = int(hash, 16)
  u1 = (z * w) % q
  u2 = (r * w) % q
  v = ((powmod(g,u1,p) * powmod(y,u2,p)) % p) % q
  return v == r

class FileNotFoundException(Exception):
  pass

class InverseErrorException(Exception):
  pass

main()