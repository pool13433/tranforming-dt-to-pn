import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring, XML
from xml.dom import minidom
import logging
from logging.handlers import TimedRotatingFileHandler
import json
from utility import *

from collections import OrderedDict

# logging
# https://docs.python.org/2/howto/logging.html
path_excel = './excel/DT.xlsx'
path_xml = "./xml/test002.xml";
path_log = "./log/transform.log"
logging.basicConfig(filename=path_log,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')


'''####################### Function Read File #######################'''
df = pd.read_excel(path_excel,sheet_name='Sheet1')
'''####################### Function Read File #######################'''

'''####################### Function Write File #######################'''
## -----------------------------------------------------------------------------------
def create_graphics(parent,positionDict=None,offsetDict=None):
    graphics = SubElement(parent,'graphics')
    if positionDict is not None:
        position = SubElement(graphics,'position')
        for k in positionDict:
            position.set(k,positionDict[k])
    if offsetDict is not None:
        offset = SubElement(graphics,'offset')
        for k in offsetDict:
            offset.set(k,offsetDict[k])
    return graphics
def create_name(parent,placeDict=None):
    name = SubElement(parent,'name')
    value = SubElement(name,'value')
    if placeDict is not None:
        value.text = placeDict['id']
    graphics = create_graphics(name,None,{'x' : '23.0' , 'y' : '-10.0'})
    return name
def create_initialMarking(parent):
    initialMarking = SubElement(parent,'initialMarking')
    value = SubElement(initialMarking,'value')
    value.text = '0'
    create_graphics(initialMarking,None,{'x' : '0.0' ,'y' : '0.0'})
    return initialMarking

def create_capacity(parent):
    capacity = SubElement(parent,'capacity')
    return capacity

def create_place(net,placeDict=None,positionDict=None):
    place = SubElement(net, 'place')
    if placeDict is not None:
        place.set('id', placeDict['id']) # 'A1')

    if positionDict is not None:
        # position = {'x': '870.0', 'y': '105.0'}
        graphics = create_graphics(place, positionDict, None)

    name = create_name(place,placeDict)

    initialMarking = create_initialMarking(place)
    capacity = create_capacity(place)
    value = SubElement(capacity,'value')
    value.text = "0"

def create_transition(parent,transitionDict=None,graphicsDict=None):
    transition = SubElement(parent,'transition')
    if transitionDict is not None:
        transition.set("id",transitionDict['id'])

    graphics = create_graphics(transition,graphicsDict,None)

    name = create_name(transition,transitionDict)

    orientation = SubElement(transition,'orientation')
    orientation_value = SubElement(orientation,'value')
    orientation_value.text = '0'

    rate = SubElement(transition,'rate')
    rate_value = SubElement(rate, 'value')
    rate_value.text = '1.0'

    timed = SubElement(transition, 'timed')
    timed_value = SubElement(timed, 'value')
    timed_value.text = 'false'

    infiniteServer = SubElement(transition, 'infiniteServer')
    infiniteServer_value = SubElement(infiniteServer, 'value')
    infiniteServer_value.text = 'false'

    priority = SubElement(transition, 'priority')
    priority_value = SubElement(priority, 'value')
    priority_value.text = '1'


def create_arc(parent,arcDict=None,tagged_valueText=None,arcpathList=None):
    arc = SubElement(parent,'arc')
    if arcDict is not None:
        for k in arcDict:
            arc.set(k,arcDict[k])
    graphics = SubElement(arc,'graphics')
    inscription = create_inscription(arc,"1")
    tagged = SubElement(arc,'tagged')
    value = SubElement(tagged,'value')
    value.text = tagged_valueText
    if arcpathList is not None:
        for arcpath in arcpathList:
            create_arcpath(arc, arcpath)
    type = SubElement(arc,'type')
    type.set("value","normal")

def create_inscription(parent,valueText=None):
    inscription = SubElement(parent,'inscription')
    value = SubElement(inscription,'value')
    if valueText is not None:
        value.text = valueText
    graphics = SubElement(inscription,'graphics')

def create_arcpath(parent,arcpathDict=None):
    arcpath = SubElement(parent,'arcpath')
    for k in arcpathDict:
        arcpath.set(k,arcpathDict[k])


## -----------------------------------------------------------------------------------
# create the file structure
def execute_writeFile(excelDict=None):
    pnml = Element('pnml')
    logging.info('createElement:: pnml')

    net = SubElement(pnml, 'net')
    logging.info('createElement:: net')
    net.set('id','Net-One')
    net.set('type','P/T net')

    token = SubElement(net,'token')
    logging.info('createElement:: token')
    #id="Default" enabled="true" red="0" green="0" blue="0"
    token.set('id','Default')
    token.set('enabled','true')
    token.set('red','0')
    token.set('green','0')
    token.set('blue','0')

    # --------------- Place -----------
    if excelDict is not None:
        #for k in range(15):
        x_gap = 200
        y_gap = 100
        driver_name = 'P'
        immediate_name = 'T'
        x_position = 200
        y_position = 0
        columnDict = excelDict['columns']
        rowsDict = excelDict['rows']
        object_positionDict = {}

        print('len columnDict::=='+str(len(columnDict)))
        print('len rowsDict::==' + str(len(rowsDict)))

        # Loop Columns (Rules)
        rules_y_position = y_position
        rules_x_position = x_position+(x_gap*2)
        p_y_position = y_position
        for index_col,key_col in enumerate(sorted_dict(columnDict)):
            print('keyCol ::=='+str(key_col)+' index_col::=='+str(index_col))

            # object P
            p_place_alias = driver_name+str(index_col)
            p_y_position = p_y_position+y_gap
            p_placeDict = {'id' : p_place_alias}
            p_positionDict = {'x': str(x_position), 'y': str(p_y_position)}
            place0 = create_place(net,p_placeDict,p_positionDict)
            object_positionDict[p_place_alias] = p_positionDict
            #logging.info('createElement:: place['+str(k)+']')

            # object R
            rules_place_alias = key_col
            rules_y_position = rules_y_position + y_gap
            rules_placeDict = {'id': rules_place_alias}
            rules_positionDict = {'x': str(rules_x_position), 'y': str(rules_y_position)}
            place0 = create_place(net, rules_placeDict, rules_positionDict)
            object_positionDict[rules_place_alias] = rules_positionDict

        # Loop Rows (Stub)
        #stub_x_position = x_position
        a_x_position  = x_position + (x_gap*3)
        a_y_position = y_position
        c_x_position = x_position + (x_gap*1)
        c_y_position  = y_position
        for indexRow, keyRow in enumerate(sorted_dict(rowsDict)):#enumerate(rowsDict):
            stub_placeDict = {'id': keyRow}
            #print('keyDict ::==' + keyRow + ' indexDict ::==' + str(indexRow))
            index_c = keyRow.find('C')
            index_a = keyRow.find('A')

            # object C
            if index_c > -1:
                a_y_position = a_y_position + y_gap
                stub_positionDict = {'x': str(c_x_position), 'y': str(a_y_position)}

            # object A
            elif index_a > -1:
                c_y_position = c_y_position + y_gap
                stub_positionDict = {'x': str(a_x_position), 'y': str(c_y_position)}
            create_place(net, stub_placeDict, stub_positionDict)
            object_positionDict[keyRow] = stub_positionDict
    # --------------- Place -----------

    # --------------- Transition -----------
        t_group = 3
        t_index_runnig = 0
        t_x_position = x_position
        t_y_position = y_position
        for indexGroup in range(t_group):
            #print('indexGroup ::=='+str(indexGroup)+' t_x_position ::=='+str(t_x_position))
            t_x_position = (x_position*(indexGroup+1))+100
            #print('t_x_position ::=='+str(t_x_position))
            t_y_position = y_position
            for indexRules,keyRules in enumerate(columnDict):
                t_y_position = t_y_position+ y_gap
                transition_name = immediate_name+str(t_index_runnig)
                transitionDict = {'id' : transition_name}
                graphicsDict= {'x' : str(t_x_position),'y' : str(t_y_position)}
                create_transition(net,transitionDict,graphicsDict)
                #logging.info('createElement:: transition[' + str(k) + ']')
                t_index_runnig += 1
                object_positionDict[transition_name] = graphicsDict
    # --------------- Transition -----------

    # --------------- Arc -----------
        condition_dict = fine_drive2immediate(rowsDict)
        print('condition_dict json::=='+json.dumps(condition_dict))
        #for k in range(35):
        for index_cond in range(len(columnDict)):
            #print('index_cond ::=='+str(index_cond)+' key_cond::=='+str(key_cond))
            print('index_cond ::==' + str(index_cond))
            tagged_valueText = "false"
            #print('immediate_name ::=='+immediate_name+'  driver_name::=='+driver_name)
            # object drive => immediate
            driver_actor = driver_name + str(index_cond)
            immediate_actor = immediate_name + str(index_cond)
            print('driver_actor::=='+driver_actor+' immediate_actor::=='+immediate_actor)
            drive2immediate_arcDict = {
                "id":driver_actor+" to "+immediate_actor,
                "source":driver_actor,
                "target":immediate_actor}
            #driver_dict = {"id": "000", "x": "430", "y": "155", "curvePoint": "false"}
            #immediate_dict = {"id": "001", "x": "547", "y": "201", "curvePoint": "false"}
            driver_dict = object_positionDict[driver_actor]
            immediate_dict = object_positionDict[immediate_actor]
            driver_dict['id'] = "000"
            driver_dict['curvePoint'] = "false"
            immediate_dict['id'] = "001"
            immediate_dict['curvePoint'] = "false"
            arcpathList = [driver_dict,immediate_dict]
            create_arc(net, drive2immediate_arcDict, tagged_valueText, arcpathList)
            #logging.info('createElement:: arc[' + str(k) + ']')

        for x in sorted(object_positionDict):
            print('x::=='+x+' position::=='+json.dumps(object_positionDict[x]))
            print('')
    # --------------- Arc -----------

    # create a new XML file with the results
    xmlstr = minidom.parseString(tostring(pnml)).toprettyxml(encoding="ISO-8859-1",indent="    ")
    with open(path_xml, "w") as f:
        f.write(xmlstr)
        logging.info('write:: '+path_xml)
'''####################### Function Write File #######################'''

def main():
    print("execute main export xml")
    excelDict = get_read_file(df)
    for x in excelDict:
        print(x)
    execute_writeFile(excelDict)

#------- execute main -----------
if __name__ == "__main__":
    main()
print("finish export xml")