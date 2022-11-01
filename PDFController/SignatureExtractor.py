

"""
Usage Example:
file2 = open('embedded.pdf', 'rb')
extractor = SignatureExtractor(file2)
print(extractor.getSignature())
"""


from PyPDF2 import PdfFileReader

class SignatureExtractor:

  def __init__(self, file):
    self.file = file

  def getSignature(self):
    pdfReader = PdfFileReader(self.file) 
    pageObj = pdfReader.getPage(pdfReader.numPages - 1) 
    return ''.join(pageObj.extractText().strip().split('\n'))

  def setFile(self, file):
    self.file = file

  def getFile(self):
    return self.file
