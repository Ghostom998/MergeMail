import docx, csv, os.path

# TODO create as class with 3 arguements

# Get text from word document. This text will hold placeholder text such as <<FIRST>> for first names, etc.
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# TODO method to parse information from CSV to retrieve the text to fill the place holder. i.e. 'john' => <<FIRST>>
def getValues(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        first, last, email, att, ExtraText = ([] for i in range(5))
        for row in reader:
            # Note: CSV must contain headers called FIRST, LAST, etc...
            first.append(row['FIRST'])
            last.append(row['LAST'])
            email.append(row['EMAIL'])
            att.append(os.path.abspath(row['ATTACHMENT']))
            ExtraText.append(row['EXTRATEXT'])
    return first, last, email, att, ExtraText

# Method build new text based on previous
def BuildText(Text, first, last, ExtraText):
    str1 = Text.replace("<<FIRST>>", first)
    str2 = str1.replace("<<LAST>>", last)
    return str2.replace("<<EXTRATEXT>>", ExtraText)

# for testing
# def WriteNewDoc(Text, DocName):
#     doc = docx.Document()
#     doc.add_paragraph(Text)
#     doc.save(DocName)
