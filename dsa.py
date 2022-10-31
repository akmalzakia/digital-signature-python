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

  hashed = hashlib.sha256(data).hexdigest()
  p, q, g = get_dsa_parameters()
  x, y = generate_keys(p, q, g)
  with open('keys/dsa_x', 'w') as f:
    f.write(str(x))
  with open('keys/dsa_y', 'w') as f:
    f.write(str(y))
  with open('dsa_signature.dsa', 'w') as f:
    params = sign(p, q, g, x, hashed)
    f.write(f'{params[0]}:{params[1]}')

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
  print(g)

  if not is_valid(p, q, g):
    print('invalid')
    exit(-1)

  return (p,q,g)


def generate_keys(p, q, g):
  c = getrandbits(N+64)
  x = (c % (q - 1)) + 1 # get random number from 1 ... q-1
  y = powmod(g, x, p) # y = g ^ x mod p
  return (x,y)

def generate_k(p, q, g):
  c = getrandbits(N+64)
  k = (c % (q - 1)) + 1
  try:
    k_ = pow(k, -1 , q)
    return (k, k_)
  except InverseErrorException:
    return generate_k(p, q, g)

def sign(p, q, g, x, hash):
  k, k_ = generate_k(p, q, g)
  r = pow(g, k, p) % q
  z = int(hash, 16)
  s = k_ * (z + x * r)

  return (r, s)


def verify(data, key):
  pass

class FileNotFoundException(Exception):
  pass

class InverseErrorException(Exception):
  pass

main()