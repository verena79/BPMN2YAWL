from xml.dom import minidom

def parser(bpmnProcess, path):
    doc = minidom.parse(bpmnProcess)
    yawl = minidom.Document()

    # general structure of YAWL Process
    specificationSet = yawl.createElement('specificationSet')
    specificationSet.setAttribute('xmlns', 'http://www.yawlfoundation.org/yawlschema')
    specificationSet.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    specificationSet.setAttribute('version', '4.0') 
    specificationSet.setAttribute('xsi:schemaLocation', 'http://www.yawlfoundation.org/yawlschema http://www.yawlfoundation.org/yawlschema/YAWL_Schema4.0.xsd') 
    yawl.appendChild(specificationSet)

    # specification
    specification = yawl.createElement('specification')
    specification.setAttribute('uri', 'Prozess')
    specificationSet.appendChild(specification) 

    documentation = yawl.createElement('documentation')
    documentation.appendChild( yawl.createTextNode("No description provided") )
    specification.appendChild(documentation)   

    #metaData
    meta = yawl.createElement('metaData')
    specification.appendChild(meta) 

    creator = yawl.createElement('creator')
    creator.appendChild( yawl.createTextNode("user") )
    meta.appendChild(creator) 

    descr = yawl.createElement('description')
    descr.appendChild( yawl.createTextNode("No description provided") )
    meta.appendChild(descr)

    coverage = yawl.createElement('coverage')
    coverage.appendChild( yawl.createTextNode("4.5.785") )
    meta.appendChild(coverage)
    
    version = yawl.createElement('version')
    version.appendChild( yawl.createTextNode("0.1") )
    meta.appendChild(version)

    persistent = yawl.createElement('persistent')
    persistent.appendChild( yawl.createTextNode("false") )
    meta.appendChild(persistent)

    ident = yawl.createElement('identifier')
    ident.appendChild( yawl.createTextNode("UID_bffb3593-eb04-49f0-b6ae-84e6e06fc949") )
    meta.appendChild(ident)

    #schema
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

    locale = yawl.createElement('locale')
    locale.setAttribute('language', 'de')
    locale.setAttribute('country', 'AT')
    layout.appendChild(locale)

    specificationL = yawl.createElement('specification')
    specificationL.setAttribute('id', 'Prozess')
    layout.appendChild(specificationL)

    size = yawl.createElement('size')
    size.setAttribute('w', '800')
    size.setAttribute('h', '650')
    specificationL.appendChild(size)

    net = yawl.createElement('net')
    net.setAttribute('id', 'Net')
    specificationL.appendChild(net)

    bounds = yawl.createElement('bounds')
    bounds.setAttribute('x', '0')
    bounds.setAttribute('y', '0')
    bounds.setAttribute('w', '1045')
    bounds.setAttribute('h', '390')
    net.appendChild(bounds)

    frame = yawl.createElement('frame')
    frame.setAttribute('x', '0')
    bounds.setAttribute('y', '0')
    frame.setAttribute('w', '1050')
    frame.setAttribute('h', '400')
    net.appendChild(frame)

    viewport = yawl.createElement('viewport')
    viewport.setAttribute('x', '0')
    viewport.setAttribute('y', '0')
    viewport.setAttribute('w', '1050')
    viewport.setAttribute('h', '400')
    net.appendChild(viewport)


    #Tasks, Gateways etc.

    #start
    starts = doc.getElementsByTagName("startEvent")
    for start in starts:
        startYawl = yawl.createElement("inputCondition")
        startYawl.setAttribute("id", start.getAttribute("id"))
        processControlElements.appendChild(startYawl) 

        # name
        name = yawl.createElement('name')
        if start.getAttribute("name") != "":
            name.appendChild(yawl.createTextNode(start.getAttribute("name")))
            startYawl.appendChild(name)   

        # flowsInto
        flowsInto = yawl.createElement('flowsInto')
        startYawl.appendChild(flowsInto) 

        #nextElementRef
        nextElementRef = yawl.createElement('nextElementRef')
        #get next Element
        outgoing = start.getElementsByTagName("outgoing")
        flows = doc.getElementsByTagName("sequenceFlow")
        for flow in flows:
            if outgoing[0].firstChild.nodeValue == flow.getAttribute("id"):
                nextElementRef.setAttribute("id", flow.getAttribute("targetRef"))
        flowsInto.appendChild(nextElementRef)

        #layout
        container = yawl.createElement('container')
        container.setAttribute('id', start.getAttribute("id"))
        net.appendChild(container)

        vertex = yawl.createElement('vertex')
        container.appendChild(vertex)

        attributes = yawl.createElement('attributes')
        vertex.appendChild(attributes)

        bounds = yawl.createElement('bounds')
        #get Bounds from BPMN
        shapes = doc.getElementsByTagName("bpmndi:BPMNShape")
        for shape in shapes:
            if shape.getAttribute("bpmnElement") == start.getAttribute("id"):
                shapeBounds = shape.getElementsByTagName("omgdc:Bounds")[0]      

                bounds.setAttribute('x', shapeBounds.getAttribute("x"))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', shapeBounds.getAttribute("width"))
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)

                if len(shape.getElementsByTagName("omgdc:Bounds")) > 1:
                    labelBounds = shape.getElementsByTagName("omgdc:Bounds")[1]
                    labelE = yawl.createElement('label')
                    container.appendChild(labelE)

                    attributes = yawl.createElement('attributes')
                    labelE.appendChild(attributes)

                    bounds = yawl.createElement('bounds')    
                    bounds.setAttribute('x', labelBounds.getAttribute("x"))
                    bounds.setAttribute('y', labelBounds.getAttribute("y"))
                    bounds.setAttribute('w', labelBounds.getAttribute("width"))
                    bounds.setAttribute('h', labelBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

    # task  
    tasks = doc.getElementsByTagName("task")
    for task in tasks:
        newtaskYawl = yawl.createElement("task")
        newtaskYawl.setAttribute("id", task.getAttribute("id"))
        processControlElements.appendChild(newtaskYawl)

        # name
        name = yawl.createElement('name')
        if task.getAttribute("name") != "":
            name.appendChild(yawl.createTextNode(task.getAttribute("name")))
            newtaskYawl.appendChild(name)   

        # flowsInto
        flowsInto = yawl.createElement('flowsInto')
        newtaskYawl.appendChild(flowsInto) 

        #nextElementRef
        nextElementRef = yawl.createElement('nextElementRef')
        #get next Element
        outgoing = task.getElementsByTagName("outgoing")
        flows = doc.getElementsByTagName("sequenceFlow")
        for flow in flows:
            if outgoing[0].firstChild.nodeValue == flow.getAttribute("id"):
                nextElementRef.setAttribute("id", flow.getAttribute("targetRef"))
                flowsInto.appendChild(nextElementRef)

        #join
        join = yawl.createElement('join')
        join.setAttribute("code", "xor")
        newtaskYawl.appendChild(join) 

        #split
        split = yawl.createElement('split')
        split.setAttribute("code", "and")
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

        vertex = yawl.createElement('vertex')
        containerTask.appendChild(vertex)

        attributes = yawl.createElement('attributes')
        vertex.appendChild(attributes)

        bounds = yawl.createElement('bounds')
        #get Bounds from BPMN
        shapes = doc.getElementsByTagName("bpmndi:BPMNShape")
        for shape in shapes:
            if shape.getAttribute("bpmnElement") == task.getAttribute("id"):
                shapeBounds = shape.getElementsByTagName("omgdc:Bounds")[0]    

                bounds.setAttribute('x', shapeBounds.getAttribute("x"))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', shapeBounds.getAttribute("width"))
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)

                if len(shape.getElementsByTagName("omgdc:Bounds")) > 1:
                    labelBounds = shape.getElementsByTagName("omgdc:Bounds")[1]
                    labelE = yawl.createElement('label')
                    containerTask.appendChild(labelE)

                    attributes = yawl.createElement('attributes')
                    labelE.appendChild(attributes)

                    bounds = yawl.createElement('bounds')    
                    bounds.setAttribute('x', labelBounds.getAttribute("x"))
                    bounds.setAttribute('y', labelBounds.getAttribute("y"))
                    bounds.setAttribute('w', labelBounds.getAttribute("width"))
                    bounds.setAttribute('h', labelBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

            # if task has two incomings - set XOR Join
            # decorator
                countIncoming = len(task.getElementsByTagName("incoming"))
                if countIncoming > 1:
                    # join
                    decorator = yawl.createElement('decorator')
                    decorator.setAttribute('type', 'XOR_join')
                    containerTask.appendChild(decorator)
                
                    position = yawl.createElement('position') 
                    position.appendChild( yawl.createTextNode('12') )
                    decorator.appendChild(position)

                    attributes = yawl.createElement('attributes')
                    decorator.appendChild(attributes)
                   
                    bounds = yawl.createElement('bounds')    
                    x = float(shapeBounds.getAttribute("x"))-10    
                    bounds.setAttribute('x', str(x))
                    bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                    bounds.setAttribute('w', '11')
                    bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

    
    # end
    ends = doc.getElementsByTagName("endEvent")
    for end in ends:
        endYawl = yawl.createElement("outputCondition")
        endYawl.setAttribute("id", end.getAttribute("id"))
        processControlElements.appendChild(endYawl)

        # name
        name = yawl.createElement('name')
        if end.getAttribute("name") != "":
            name.appendChild(yawl.createTextNode(end.getAttribute("name")))
            endYawl.appendChild(name) 

        #layout
        container = yawl.createElement('container')
        container.setAttribute('id', end.getAttribute("id"))
        net.appendChild(container)

        vertex = yawl.createElement('vertex')
        container.appendChild(vertex)

        attributes = yawl.createElement('attributes')
        vertex.appendChild(attributes)

        bounds = yawl.createElement('bounds')
        #get Bounds from BPMN
        shapes = doc.getElementsByTagName("bpmndi:BPMNShape")
        for shape in shapes:
            if shape.getAttribute("bpmnElement") == end.getAttribute("id"):
                shapeBounds = shape.getElementsByTagName("omgdc:Bounds")[0]      

                bounds.setAttribute('x', shapeBounds.getAttribute("x"))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', shapeBounds.getAttribute("width"))
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)

                if len(shape.getElementsByTagName("omgdc:Bounds")) > 1:
                    labelBounds = shape.getElementsByTagName("omgdc:Bounds")[1]
                    labelE = yawl.createElement('label')
                    container.appendChild(labelE)

                    attributes = yawl.createElement('attributes')
                    labelE.appendChild(attributes)

                    bounds = yawl.createElement('bounds')    
                    bounds.setAttribute('x', labelBounds.getAttribute("x"))
                    bounds.setAttribute('y', labelBounds.getAttribute("y"))
                    bounds.setAttribute('w', labelBounds.getAttribute("width"))
                    bounds.setAttribute('h', labelBounds.getAttribute("height"))
                    attributes.appendChild(bounds)
    
    # sub process
    subProcesses = doc.getElementsByTagName("subProcess")
    for subP in subProcesses:
        compositeTask = yawl.createElement("task")
        compositeTask.setAttribute("id", subP.getAttribute("id"))
        processControlElements.appendChild(compositeTask)

        # name
        name = yawl.createElement('name')
        if subP.getAttribute("name") != "":
            name.appendChild(yawl.createTextNode(subP.getAttribute("name")))
            compositeTask.appendChild(name)   

        # flowsInto
        flowsInto = yawl.createElement('flowsInto')
        compositeTask.appendChild(flowsInto) 

        #nextElementRef
        nextElementRef = yawl.createElement('nextElementRef')
        #get next Element
        outgoing = subP.getElementsByTagName("outgoing")
        flows = doc.getElementsByTagName("sequenceFlow")
        for flow in flows:
            if outgoing[0].firstChild.nodeValue == flow.getAttribute("id"):
                nextElementRef.setAttribute("id", flow.getAttribute("targetRef"))
                flowsInto.appendChild(nextElementRef)
        
        #is Default Flow
        default = yawl.createElement('isDefaultFlow')
        flowsInto.appendChild(default)

        #join
        join = yawl.createElement('join')
        join.setAttribute("code", "xor")
        compositeTask.appendChild(join) 

        #split
        split = yawl.createElement('split')
        split.setAttribute("code", "and")
        compositeTask.appendChild(split)

        #decomposesTo
        decompose = yawl.createElement('decomposesTo')
        decompose.setAttribute("id", "")
        compositeTask.appendChild(decompose)  

        #layout
        containerTask = yawl.createElement('container')
        containerTask.setAttribute('id', subP.getAttribute("id"))
        net.appendChild(containerTask)

        vertex = yawl.createElement('vertex')
        containerTask.appendChild(vertex)

        attributes = yawl.createElement('attributes')
        vertex.appendChild(attributes)

        bounds = yawl.createElement('bounds')
        #get Bounds from BPMN
        shapes = doc.getElementsByTagName("bpmndi:BPMNShape")
        for shape in shapes:
            if shape.getAttribute("bpmnElement") == subP.getAttribute("id"):
                shapeBounds = shape.getElementsByTagName("omgdc:Bounds")[0]      

                bounds.setAttribute('x', shapeBounds.getAttribute("x"))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', shapeBounds.getAttribute("width"))
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)

                if len(shape.getElementsByTagName("omgdc:Bounds")) > 1:
                    labelBounds = shape.getElementsByTagName("omgdc:Bounds")[1]
                    labelE = yawl.createElement('label')
                    containerTask.appendChild(labelE)

                    attributes = yawl.createElement('attributes')
                    labelE.appendChild(attributes)

                    bounds = yawl.createElement('bounds')    
                    bounds.setAttribute('x', labelBounds.getAttribute("x"))
                    bounds.setAttribute('y', labelBounds.getAttribute("y"))
                    bounds.setAttribute('w', labelBounds.getAttribute("width"))
                    bounds.setAttribute('h', labelBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

    # parallel gateway
    pGateways = doc.getElementsByTagName("parallelGateway")
    for pGateway in pGateways:
        AND = yawl.createElement("task")
        AND.setAttribute("id", pGateway.getAttribute("id"))
        processControlElements.appendChild(AND)

        # name
        name = yawl.createElement('name')
        if pGateway.getAttribute("name") != "":
            name.appendChild(yawl.createTextNode(pGateway.getAttribute("name")))
            AND.appendChild(name)  

        # flowsInto
        #countOutgoing = len(pGateway.getElementsByTagName("outgoing"))
        for out in pGateway.getElementsByTagName("outgoing"):
            flowsInto = yawl.createElement('flowsInto')
            AND.appendChild(flowsInto) 

            #nextElementRef
            nextElementRef = yawl.createElement('nextElementRef')
            #get next Element
            flows = doc.getElementsByTagName("sequenceFlow")
            for flow in flows:
                if out.firstChild.nodeValue == flow.getAttribute("id"):
                    nextElementRef.setAttribute("id", flow.getAttribute("targetRef"))
                    flowsInto.appendChild(nextElementRef)

        #join
        join = yawl.createElement('join')
        join.setAttribute("code", "and")
        AND.appendChild(join) 

        #split
        split = yawl.createElement('split')
        split.setAttribute("code", "and")
        AND.appendChild(split) 

        # #ressourcing
        # ressourcing = yawl.createElement('ressourcing')
        # AND.appendChild(ressourcing) 

        # offer = yawl.createElement('offer')
        # offer.setAttribute("initiator", "user")
        # ressourcing.appendChild(offer) 

        # allocate = yawl.createElement('allocate')
        # allocate.setAttribute("initiator", "user")
        # ressourcing.appendChild(allocate) 

        # start = yawl.createElement('start')
        # start.setAttribute("initiator", "user")
        # ressourcing.appendChild(start) 

        #layout
        containerTask = yawl.createElement('container')
        containerTask.setAttribute('id', pGateway.getAttribute("id"))
        net.appendChild(containerTask)

        vertex = yawl.createElement('vertex')
        containerTask.appendChild(vertex)

        attributes = yawl.createElement('attributes')
        vertex.appendChild(attributes)

        bounds = yawl.createElement('bounds')
        #get Bounds from BPMN
        shapes = doc.getElementsByTagName("bpmndi:BPMNShape")
        for shape in shapes:
            if shape.getAttribute("bpmnElement") == pGateway.getAttribute("id"):
                shapeBounds = shape.getElementsByTagName("omgdc:Bounds")[0]

                bounds.setAttribute('x', shapeBounds.getAttribute("x"))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', shapeBounds.getAttribute("width"))
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)

                if len(shape.getElementsByTagName("omgdc:Bounds")) > 1:
                    labelBounds = shape.getElementsByTagName("omgdc:Bounds")[1]
                    labelE = yawl.createElement('label')
                    containerTask.appendChild(labelE)

                    attributes = yawl.createElement('attributes')
                    labelE.appendChild(attributes)

                    bounds = yawl.createElement('bounds')    
                    bounds.setAttribute('x', labelBounds.getAttribute("x"))
                    bounds.setAttribute('y', labelBounds.getAttribute("y"))
                    bounds.setAttribute('w', labelBounds.getAttribute("width"))
                    bounds.setAttribute('h', labelBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

                # decorator
                countOutgoing = len(pGateway.getElementsByTagName("outgoing"))
                if countOutgoing > 1:
                    # split
                    decorator = yawl.createElement('decorator')
                    decorator.setAttribute('type', 'AND_split')
                    containerTask.appendChild(decorator)
                    position = yawl.createElement('position') 
                    position.appendChild( yawl.createTextNode('13') )
                    decorator.appendChild(position)

                    attributes = yawl.createElement('attributes')
                    decorator.appendChild(attributes)

                    bounds = yawl.createElement('bounds')
                    x = float(shapeBounds.getAttribute("x"))+30   
                    bounds.setAttribute('x', str(x))
                    bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                    bounds.setAttribute('w', '11')
                    bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                    attributes.appendChild(bounds)
                else:
                    # join
                    decorator = yawl.createElement('decorator')
                    decorator.setAttribute('type', 'AND_join')
                    containerTask.appendChild(decorator)
                
                    position = yawl.createElement('position') 
                    position.appendChild( yawl.createTextNode('12') )
                    decorator.appendChild(position)

                    attributes = yawl.createElement('attributes')
                    decorator.appendChild(attributes)
                   
                    bounds = yawl.createElement('bounds')    
                    x = float(shapeBounds.getAttribute("x"))-10    
                    bounds.setAttribute('x', str(x))
                    bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                    bounds.setAttribute('w', '11')
                    bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

    # exklusive gateway
    eGateways = doc.getElementsByTagName("exclusiveGateway")
    for eGateway in eGateways:
        XOR = yawl.createElement("task")
        XOR.setAttribute("id", eGateway.getAttribute("id"))
        processControlElements.appendChild(XOR)

        # name
        name = yawl.createElement('name')
        if eGateway.getAttribute("name") != "":
            name.appendChild(yawl.createTextNode(eGateway.getAttribute("name")))
            XOR.appendChild(name)  

        # flowsInto
        for out in eGateway.getElementsByTagName("outgoing"):
            flowsInto = yawl.createElement('flowsInto')
            XOR.appendChild(flowsInto) 

            #nextElementRef
            nextElementRef = yawl.createElement('nextElementRef')
            #get next Element
            flows = doc.getElementsByTagName("sequenceFlow")
            for flow in flows:
                if out.firstChild.nodeValue == flow.getAttribute("id"):
                    nextElementRef.setAttribute("id", flow.getAttribute("targetRef"))
                    flowsInto.appendChild(nextElementRef)

                    #predicate
                    predicate = yawl.createElement('predicate')
                    predicate.setAttribute('ordering', "0")
                    predicate.appendChild( yawl.createTextNode('true()') )
                    flowsInto.appendChild(predicate)

        #join
        join = yawl.createElement('join')
        join.setAttribute("code", "xor")
        XOR.appendChild(join) 

        #split
        split = yawl.createElement('split')
        split.setAttribute("code", "xor")
        XOR.appendChild(split) 

        # #ressourcing
        # ressourcing = yawl.createElement('ressourcing')
        # XOR.appendChild(ressourcing) 

        # offer = yawl.createElement('offer')
        # offer.setAttribute("initiator", "user")
        # ressourcing.appendChild(offer) 

        # allocate = yawl.createElement('allocate')
        # allocate.setAttribute("initiator", "user")
        # ressourcing.appendChild(allocate) 

        # start = yawl.createElement('start')
        # start.setAttribute("initiator", "user")
        # ressourcing.appendChild(start) 

        #layout
        containerTask = yawl.createElement('container')
        containerTask.setAttribute('id', eGateway.getAttribute("id"))
        net.appendChild(containerTask)

        vertex = yawl.createElement('vertex')
        containerTask.appendChild(vertex)

        attributes = yawl.createElement('attributes')
        vertex.appendChild(attributes)

        bounds = yawl.createElement('bounds')
        #get Bounds from BPMN
        shapes = doc.getElementsByTagName("bpmndi:BPMNShape")
        for shape in shapes:
            if shape.getAttribute("bpmnElement") == eGateway.getAttribute("id"):
                shapeBounds = shape.getElementsByTagName("omgdc:Bounds")[0]

                bounds.setAttribute('x', shapeBounds.getAttribute("x"))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', shapeBounds.getAttribute("width"))
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)

                if len(shape.getElementsByTagName("omgdc:Bounds")) > 1:
                    labelBounds = shape.getElementsByTagName("omgdc:Bounds")[1]
                    labelE = yawl.createElement('label')
                    containerTask.appendChild(labelE)

                    attributes = yawl.createElement('attributes')
                    labelE.appendChild(attributes)

                    bounds = yawl.createElement('bounds')    
                    bounds.setAttribute('x', labelBounds.getAttribute("x"))
                    bounds.setAttribute('y', labelBounds.getAttribute("y"))
                    bounds.setAttribute('w', labelBounds.getAttribute("width"))
                    bounds.setAttribute('h', labelBounds.getAttribute("height"))
                    attributes.appendChild(bounds)

                # decorator
                
                decorator = yawl.createElement('decorator')
                decorator.setAttribute('type', 'XOR_split')
                containerTask.appendChild(decorator)
                position = yawl.createElement('position') 
                position.appendChild( yawl.createTextNode('13') )
                decorator.appendChild(position)

                attributes = yawl.createElement('attributes')
                decorator.appendChild(attributes)

                bounds = yawl.createElement('bounds')
                x = float(shapeBounds.getAttribute("x"))+30 
                bounds.setAttribute('x', str(x))
                bounds.setAttribute('y', shapeBounds.getAttribute("y"))
                bounds.setAttribute('w', '11' )
                bounds.setAttribute('h', shapeBounds.getAttribute("height"))
                attributes.appendChild(bounds)   

    # Sequence Flow
    flows = doc.getElementsByTagName("sequenceFlow")
    for flow in flows:
        flowYawl = yawl.createElement("flow")
        flowYawl.setAttribute("source", flow.getAttribute("sourceRef"))
        flowYawl.setAttribute("target", flow.getAttribute("targetRef"))
        net.appendChild(flowYawl)

        #ports
        ports = yawl.createElement('ports')
        ports.setAttribute("in", "13")
        ports.setAttribute("out", "12")
        flowYawl.appendChild(ports)

        #attributes
        attributes = yawl.createElement('attributes')
        flowYawl.appendChild(attributes)

        linestyle = yawl.createElement('lineStyle')
        linestyle.appendChild(yawl.createTextNode("11"))
        attributes.appendChild(linestyle)
        
        #label
        if flow.getAttribute("name") != "":
            label = yawl.createElement('label')
            label.appendChild(yawl.createTextNode(flow.getAttribute("name"))) 
            flowYawl.appendChild(label)
            
            offset = yawl.createElement('offset')
            offset.setAttribute("x", "0")
            offset.setAttribute("y", "0")
            attributes.appendChild(offset) 

    yawl_str = yawl.toprettyxml(indent ="\t") 
    save_path_file = path
  
    with open(save_path_file, "w") as f:
        f.write(yawl_str) 

