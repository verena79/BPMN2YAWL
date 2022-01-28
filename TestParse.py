import re
from xml.dom import minidom
from xml.etree.ElementTree import tostring

def parser(bpmnProcess, path):
    doc = minidom.parse(bpmnProcess)
    yawl = minidom.Document()

    print(doc)
    print(yawl)
    # general structure of YAWL Process
    specificationSet = yawl.createElement('specificationSet') 
    yawl.appendChild(specificationSet)

    # specification
    specification = yawl.createElement('specification')
    specification.setAttribute('uri', 'Prozess')
    specificationSet.appendChild(specification) 

    documentation = yawl.createElement('documentation')
    documentation.appendChild( yawl.createTextNode("No description provided") )
    specification.appendChild(documentation)   

        #metaData?

    schema = yawl.createElement('xs:schema')
    schema.setAttribute('xmlns:xs', 'http://www.w3.org/2001/XMLSchema')
    specification.appendChild(schema)

    dec = yawl.createElement('decomposition')
    dec.setAttribute('id', 'Net')
    dec.setAttribute('isRootNet', 'true')
    dec.setAttribute('xsi:type', 'NetFactsType')
    specification.appendChild(dec)

    processControlElements = yawl.createElement('processControlElements')
    dec.appendChild(processControlElements)

    # layout
    layout = yawl.createElement('layout')
    specificationSet.appendChild(layout)

    specificationL = yawl.createElement('specification')
    specificationL.setAttribute('id', 'Prozess')
    layout.appendChild(specificationL)

    net = yawl.createElement('net')
    net.setAttribute('id', 'Net')
    specificationL.appendChild(net)


    #Tasks, Gateways etc.

    #start
    starts = doc.getElementsByTagName("startEvent")
    for start in starts:
        startYawl = yawl.createElement("inputCondition")
        startYawl.setAttribute("id", start.getAttribute("id"))
        processControlElements.appendChild(startYawl) 

        # name
        name = yawl.createElement('name')
        name.appendChild(yawl.createTextNode(start.getAttribute("name")))
        startYawl.appendChild(name)  

        #layout
        container = yawl.createElement('container')
        container.setAttribute('id', start.getAttribute("id"))
        net.appendChild(container)

    # task  
    tasks = doc.getElementsByTagName("task")
    for task in tasks:
        newtaskYawl = yawl.createElement("task")
        newtaskYawl.setAttribute("id", task.getAttribute("id"))
        processControlElements.appendChild(newtaskYawl)

        # name
        name = yawl.createElement('name')
        name.appendChild(yawl.createTextNode(task.getAttribute("name")))
        newtaskYawl.appendChild(name)  

        # flowsInto
        flowsInto = yawl.createElement('flowsInto')
        #TODO: id of next Element (not Sequenzflow!)
        # newtaskYawl.setAttribute("id", task.getAttribute("id"))
        newtaskYawl.appendChild(flowsInto) 

        #nextElementRef
        nextElementRef = yawl.createElement('nextElementRef')
        
        flowsInto.appendChild(nextElementRef)

        incoming = task.getElementsByTagName("incoming")

        #join
        join = yawl.createElement('join')
        join.setAttribute("code", task.getAttribute("xor"))
        newtaskYawl.appendChild(join) 

        #split
        split = yawl.createElement('split')
        split.setAttribute("code", task.getAttribute("and"))
        newtaskYawl.appendChild(split) 

        #ressourcing
        ressourcing = yawl.createElement('ressourcing')
        newtaskYawl.appendChild(ressourcing) 

        offer = yawl.createElement('offer')
        offer.setAttribute("initiator", "user")
        ressourcing.appendChild(offer) 

        allocate = yawl.createElement('allocate')
        allocate.setAttribute("initiator", "user")
        ressourcing.appendChild(allocate) 

        start = yawl.createElement('start')
        start.setAttribute("initiator", "user")
        ressourcing.appendChild(start) 

        #layout
        containerTask = yawl.createElement('container')
        containerTask.setAttribute('id', task.getAttribute("id"))
        net.appendChild(containerTask)
    
    # end
    ends = doc.getElementsByTagName("endEvent")
    for end in ends:
        endYawl = yawl.createElement("outputCondition")
        endYawl.setAttribute("id", end.getAttribute("id"))
        processControlElements.appendChild(endYawl)

        # name
        name = yawl.createElement('name')
        name.appendChild(yawl.createTextNode(end.getAttribute("name")))
        endYawl.appendChild(name)

        #layout
        container = yawl.createElement('container')
        container.setAttribute('id', end.getAttribute("id"))
        net.appendChild(container)
    


    yawl_str = yawl.toprettyxml(indent ="\t") 
    save_path_file = path
  
    with open(save_path_file, "w") as f:
        f.write(yawl_str) 

