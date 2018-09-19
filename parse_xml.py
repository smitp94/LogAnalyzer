# XML Parse
import xml.etree.ElementTree as ET
from xml.dom import minidom

e = ET.parse('data/test.xml').getroot()


root = ET.parse('data/test.xml').getroot()
for neighbor in root.getiterator('body'):
    print(neighbor.text)
    break

