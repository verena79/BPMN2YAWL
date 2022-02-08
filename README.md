# BPMN2YAWL

**Motivation**

In the course of a bachelor thesis at the FH Joanneum Graz with the title "BPMN2YAWL- Workflowmodellierung mit Workflow-Netzen" a prototype is implemented which should tranform a BPMN process automatically to a YAWL workflow net.

**Limitations**

Due to the fact that this is a prototype the BPMN symbols are limited to the sybmbols of the of the BPMN symbol palette level 1 (start events, end events, tasks, exclusive gateways, parallel gateways, sub processes). Also is the transformation of closed sub process not quiet possible due to the fact that YAWL would need the information of the sub process which is a seperate file in BPMN. As of this sub processes will be shown as atomic tasks instead of as composite tasks which would be the correct transformation. Further to simplify the transformation BPMN Gateways will be shown as seperate tasks.
Another limitation is that the BPMN Process can only have one start event and one end event because YAWL does not support multiple input condition respectively output conditions.

**How to run the prototype**

*Requirements:* 
- Python installation
- PySimpleGUI installation --> run 'pip install PySimpleGUI' in your cmd  

Navigate in the cmd to the corresponding folder and run 'python Application.py'
