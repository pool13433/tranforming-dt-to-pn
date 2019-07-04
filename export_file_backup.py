from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.dom import minidom

# create the file structure
data = Element('data')
items = SubElement(data, 'items')
item1 = SubElement(items, 'item')
item2 = SubElement(items, 'item')
item1.set('name','item1')
item2.set('name','item2')
item1.text = 'item1abc'
item2.text = 'item2abc'

# create a new XML file with the results
xmlstr = minidom.parseString(tostring(data)).toprettyxml(indent="   ")
with open("./xml/items2.xml", "w") as f:
    f.write(xmlstr)
