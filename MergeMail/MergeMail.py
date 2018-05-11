import docx, csv, os.path
import pandas as pd

# Get text from word document. This text will hold placeholder text such as <<FIRST>> for first names, etc.
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getValues(filename):
    return pd.read_csv(filename)

# Method build new text based on previous
def BuildText(Text, dic):
    for key, item in dic.items():
        Text = Text.replace("<<" + key + ">>", item)
    return Text
