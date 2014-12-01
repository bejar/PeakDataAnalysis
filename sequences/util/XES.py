"""
.. module:: XES

XES
*************

:Description: XES

    

:Authors: bejar
    

:Version: 

:Created on: 01/12/2014 13:43 

"""

__author__ = 'bejar'

import codecs
import os

file_header = u"""
<?xml version="1.0" encoding="UTF-8" ?>
<!-- This file has been generated with the OpenXES library. It conforms -->
<!-- to the XML serialization of the XES standard for log storage and -->
<!-- management. -->
<!-- XES standard version: 1.0 -->
<!-- OpenXES library version: 1.0RC7 -->
<!-- OpenXES is available from http://www.openxes.org/ -->
<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7" xmlns="http://www.xes-standard.org/">
<extension name="Lifecycle" prefix="lifecycle" uri="http://www.xes-standard.org/lifecycle.xesext"/>
<extension name="Organizational" prefix="org" uri="http://www.xes-standard.org/org.xesext"/>
<extension name="Time" prefix="time" uri="http://www.xes-standard.org/time.xesext"/>
<extension name="Concept" prefix="concept" uri="http://www.xes-standard.org/concept.xesext"/>
<extension name="Semantic" prefix="semantic" uri="http://www.xes-standard.org/semantic.xesext"/>
<global scope="trace">
<string key="concept:name" value="__INVALID__"/>
</global>
<global scope="event">
<string key="concept:name" value="__INVALID__"/>
<string key="lifecycle:transition" value="complete"/>
</global>
<classifier name="MXML Legacy Classifier" keys="concept:name lifecycle:transition"/>
<classifier name="Event Name" keys="concept:name"/>
<classifier name="Resource" keys="org:resource"/>
<string key="source" value="CPN Tools"/>
<string key="concept:name" value="{name}.mxml"/>
<string key="description" value="Log file created in CPN Tools"/>
<string key="lifecycle:model" value="standard"/>
""".strip()

file_footer = u"""</log>"""

trace_start = u"""
<trace>
<string key="concept:name" value="{key}"/>
<string key="description" value="JIRA issue"/>
""".strip()

trace_end = u"""</trace>"""
event = u"""
<event>
<string key="org:resource" value="{who}"/>
<date key="time:timestamp" value="{when}"/>
<string key="concept:name" value="{what}"/>
<string key="lifecycle:transition" value="complete"/>
</event>
""".strip()


def write_xes(basename, dir, issues):
    output = codecs.open(os.path.join(dir, basename + '-process.xes'), 'w', encoding='utf-8')

    output.write(file_header.format(name=basename).strip())
    for issue in issues:
        output.write(trace_start.format(key=issue['key']).strip())
        for log in issue['transitions']:
            output.write(event.format(who=log['who'], when=log['when'], what=log['to']).strip())
        output.write(trace_end)

    output.write(file_footer)
