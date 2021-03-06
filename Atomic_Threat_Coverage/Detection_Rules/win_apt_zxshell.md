| Title                    | ZxShell Malware       |
|:-------------------------|:------------------|
| **Description**          | Detects a ZxShell start by the called and well-known function name |
| **ATT&amp;CK Tactic**    |  <ul><li>[TA0002: Execution](https://attack.mitre.org/tactics/TA0002)</li><li>[TA0005: Defense Evasion](https://attack.mitre.org/tactics/TA0005)</li></ul>  |
| **ATT&amp;CK Technique** | <ul><li>[T1059: Command-Line Interface](https://attack.mitre.org/techniques/T1059)</li><li>[T1085: Rundll32](https://attack.mitre.org/techniques/T1085)</li></ul>  |
| **Data Needed**          |  There is no documented Data Needed for this Detection Rule yet  |
| **Trigger**              | <ul><li>[T1059: Command-Line Interface](../Triggers/T1059.md)</li><li>[T1085: Rundll32](../Triggers/T1085.md)</li></ul>  |
| **Severity Level**       | critical |
| **False Positives**      | <ul><li>Unlikely</li></ul>  |
| **Development Status**   |  Development Status wasn't defined for this Detection Rule yet  |
| **References**           | <ul><li>[https://www.hybrid-analysis.com/sample/5d2a4cde9fa7c2fdbf39b2e2ffd23378d0c50701a3095d1e91e3cf922d7b0b16?environmentId=100](https://www.hybrid-analysis.com/sample/5d2a4cde9fa7c2fdbf39b2e2ffd23378d0c50701a3095d1e91e3cf922d7b0b16?environmentId=100)</li></ul>  |
| **Author**               | Florian Roth |
| Other Tags           | <ul><li>attack.g0001</li></ul> | 

## Detection Rules

### Sigma rule

```
title: ZxShell Malware
id: f0b70adb-0075-43b0-9745-e82a1c608fcc
description: Detects a ZxShell start by the called and well-known function name
author: Florian Roth
date: 2017/07/20
references:
    - https://www.hybrid-analysis.com/sample/5d2a4cde9fa7c2fdbf39b2e2ffd23378d0c50701a3095d1e91e3cf922d7b0b16?environmentId=100
tags:
    - attack.g0001
    - attack.execution
    - attack.t1059
    - attack.defense_evasion
    - attack.t1085
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Command:
            - 'rundll32.exe *,zxFunction*'
            - 'rundll32.exe *,RemoteDiskXXXXX'
    condition: selection
fields:
    - CommandLine
    - ParentCommandLine
falsepositives:
    - Unlikely
level: critical

```





### powershell
    
```
Get-WinEvent | where {($_.message -match "Command.*rundll32.exe .*,zxFunction.*" -or $_.message -match "Command.*rundll32.exe .*,RemoteDiskXXXXX") } | select TimeCreated,Id,RecordId,ProcessId,MachineName,Message
```


### es-qs
    
```
Command.keyword:(rundll32.exe\\ *,zxFunction* OR rundll32.exe\\ *,RemoteDiskXXXXX)
```


### xpack-watcher
    
```
curl -s -XPUT -H \'Content-Type: application/json\' --data-binary @- localhost:9200/_watcher/watch/f0b70adb-0075-43b0-9745-e82a1c608fcc <<EOF\n{\n  "metadata": {\n    "title": "ZxShell Malware",\n    "description": "Detects a ZxShell start by the called and well-known function name",\n    "tags": [\n      "attack.g0001",\n      "attack.execution",\n      "attack.t1059",\n      "attack.defense_evasion",\n      "attack.t1085"\n    ],\n    "query": "Command.keyword:(rundll32.exe\\\\ *,zxFunction* OR rundll32.exe\\\\ *,RemoteDiskXXXXX)"\n  },\n  "trigger": {\n    "schedule": {\n      "interval": "30m"\n    }\n  },\n  "input": {\n    "search": {\n      "request": {\n        "body": {\n          "size": 0,\n          "query": {\n            "bool": {\n              "must": [\n                {\n                  "query_string": {\n                    "query": "Command.keyword:(rundll32.exe\\\\ *,zxFunction* OR rundll32.exe\\\\ *,RemoteDiskXXXXX)",\n                    "analyze_wildcard": true\n                  }\n                }\n              ],\n              "filter": {\n                "range": {\n                  "timestamp": {\n                    "gte": "now-30m/m"\n                  }\n                }\n              }\n            }\n          }\n        },\n        "indices": [\n          "winlogbeat-*"\n        ]\n      }\n    }\n  },\n  "condition": {\n    "compare": {\n      "ctx.payload.hits.total": {\n        "not_eq": 0\n      }\n    }\n  },\n  "actions": {\n    "send_email": {\n      "email": {\n        "to": "root@localhost",\n        "subject": "Sigma Rule \'ZxShell Malware\'",\n        "body": "Hits:\\n{{#ctx.payload.hits.hits}}Hit on {{_source.@timestamp}}:\\n      CommandLine = {{_source.CommandLine}}\\nParentCommandLine = {{_source.ParentCommandLine}}================================================================================\\n{{/ctx.payload.hits.hits}}",\n        "attachments": {\n          "data.json": {\n            "data": {\n              "format": "json"\n            }\n          }\n        }\n      }\n    }\n  }\n}\nEOF\n
```


### graylog
    
```
Command.keyword:(rundll32.exe *,zxFunction* rundll32.exe *,RemoteDiskXXXXX)
```


### splunk
    
```
(Command="rundll32.exe *,zxFunction*" OR Command="rundll32.exe *,RemoteDiskXXXXX") | table CommandLine,ParentCommandLine
```


### logpoint
    
```
Command IN ["rundll32.exe *,zxFunction*", "rundll32.exe *,RemoteDiskXXXXX"]
```


### grep
    
```
grep -P '^(?:.*rundll32\\.exe .*,zxFunction.*|.*rundll32\\.exe .*,RemoteDiskXXXXX)'
```



