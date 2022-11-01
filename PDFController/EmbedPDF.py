
"""
Usage Example:
file = open('sample.pdf', 'rb')
embedTool = EmbedPDF(file)
embedTool.embedSignature('THIS IS A SIGNATURE')
embedTool.saveFile('embedded.pdf')
"""

from io import FileIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas

class EmbedPDF:

    def __init__(self, file):
        self.file = file

    def splitEveryNth(self, text, n):
        list_strings = [text[i:i+n] for i in range(0, len(text), n)]
        return list_strings

    def saveSignatureAsPDF(self, signature):
        c = canvas.Canvas('signature.pdf', pagesize=(8.5 * 72, 11 * 72))
        c.setStrokeColorRGB(0,0,0)
        c.setFillColorRGB(0,0,0)
        c.setFont("Helvetica", 12)

        v = 10 * 72
        
        for subtline in self.splitEveryNth(signature, 70):
            c.drawString( 1 * 72, v, subtline )
            v -= 12
        c.showPage()
        c.save()

    def embedSignature(self, signature):
        #
        self.saveSignatureAsPDF(signature)

        output = PdfFileWriter()
        input1 = PdfFileReader(self.file)
        input2 = PdfFileReader(open("signature.pdf", "rb"))

        for i in range(input1.getNumPages()):
          output.addPage(input1.getPage(i))
        output.addPage(input2.getPage(0))
        self.embeddedPDF = output

    def saveFile(self, path):
        #
        outputStream = FileIO(path, "wb")
        self.embeddedPDF.write(outputStream)
        outputStream.close()

    def setFile(self, file):
        self.file = file

    def getFile(self):
        return self.file

