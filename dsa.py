import hashlib
import os
from random import getrandbits
from gmpy2 import is_prime
from gmpy2 import powmod
import sys

from PDFController.EmbedPDF import EmbedPDF
from PDFController.SignatureExtractor import SignatureExtractor

L = 512
N = 160

default_p = 13232376895198612407547930718267435757728527029623408872245156039757713029036368719146452186041204237350521785240337048752071462798273003935646236777459223
default_q = 857393771208094202104259627990318636601332086981
default_g = 5421644057436475141609648488325705128047428394380474376834667300766108262613900542681289080713724597310673074119355136085795982097390670890367185141189796

keystore = './keys'
default_x_path = f'{keystore}/dsa_x'
default_y_path = f'{keystore}/dsa_y'

def no_bits(p):
  return len(bin(p)) - 2

def get_file(filepath, modes):
  if os.path.isfile(filepath):
    f = open(filepath, modes)
    f_data = f.read()
    f.close()

    return f_data
  
  return FileNotFoundException
class DSA:
  def __init__(self, p = default_p, q = default_q, g = default_g) -> None:
    if not self.is_valid(p, q, g):
      print('invalid')
      exit(-1)

    self.p = p
    self.q = q
    self.g = g
  
  def is_valid(self,p,q,g):
    return (
      is_prime(p) and is_prime(q) and no_bits(p) == 512 and no_bits(q) == 160 and (p-1) % q == 0 and powmod(g,q,p) == 1 and g > 1
    )

  def generate_keys(self):
    c = getrandbits(N+64)
    x = (c % (self.q - 1)) + 1 # get random number from 1 ... q-1
    y = powmod(self.g, x, self.p) # y = g ^ x mod p
    return (x,y)

  def generate_k(self):
    c = getrandbits(N+64)
    k = (c % (self.q - 1)) + 1
    try:
      k_ = pow(k, -1 , self.q)
      return (k, k_)
    except InverseErrorException:
      return self.generate_k()

  def sign(self, x, hash):
    k, k_ = self.generate_k()
    r = pow(self.g, k, self.p) % self.q
    z = int(hash, 16)
    s = k_ * (z + x * r)

    return (r, s)
  
  def verify(self, hash, r, s, y):
    w = pow(s, -1 , self.q)
    z = int(hash, 16)
    u1 = (z * w) % self.q
    u2 = (r * w) % self.q
    v = ((powmod(self.g,u1,self.p) * powmod(y,u2,self.p)) % self.p) % self.q
    return v == r

def usage():
  print("Usage: dsa.py <command> <file>")
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

  dsa = DSA()
  hashed = hashlib.sha256(data).hexdigest()

  if token == 'sign':
    signing(dsa, hashed)
  elif token == 'verify':
    verifying(dsa, hashed)
  
  print(f'---- {token.upper()} PROCESS DONE ----')


def verifying(dsa, hashed):
  # Get signature, bisa diganti dengan misahin signature
  print("Insert signature file:")
  print(">>", end=' ', flush=True)
  signature_file = input()
  print('-' * 20)
  
  with open(signature_file, 'r') as f:
    params = f.read().split(':')
    r, s = int(params[0]), int(params[1])

  # Get public key
  print("Insert public key file:")
  print(">>", end=' ', flush=True)
  y_file = input()
  print('-' * 20)

  with open(y_file, 'r') as f:
    y = int(f.read())
  
  if dsa.verify(hashed, r, s, y):
    print("Verification Success --- Signature Match")
  else:
    print("Verification Failed --- Signature not match")

  

def signing(dsa, hashed):
  
  if check_file(default_x_path) and check_file(default_y_path):
    with open(default_x_path, 'r') as f:
      x = int(f.read())
    with open(default_y_path, 'r') as f:
      y = int(f.read())
  else:
    x, y = dsa.generate_keys()
    with open(default_x_path, 'w') as f:
      f.write(str(x))
    with open(default_y_path, 'w') as f:
      f.write(str(y))

  with open('dsa_signature.dsa', 'w') as f:
    params = dsa.sign(x, hashed)
    print(no_bits(params[0]), ':', no_bits(params[1]))
    f.write(f'{params[0]}:{params[1]}')

def check_file(filepath):
  return os.path.exists(filepath) and not os.stat(filepath).st_size == 0

class FileNotFoundException(Exception):
  pass

class InverseErrorException(Exception):
  pass

main()