# StackStorm Integration Pack for Cisco Application Centric Infrastructure (ACI)

## Configuration
Example Configuration
```
---
cobra:
  download_location: "http://aci-cl01-apic01/cobra/_downloads/"
  eggs:
    cobra: "acicobra-x-py2.7.egg"
    model: "acimodel-x-py2.7.egg"
username: aciuser
password: acipassword
clusters:
  - name: ACICluster01
    apics:
      - https://aci-cl01-apic01
      - https://aci-cl01-apic02
      - https://aci-cl01-apic03
  - name: ACICluster02
    username: cluster2user
    password: cluster2password
    apics:
      - http://aci-cl02-apic01
      - http://aci-cl02-apic02
      - http://aci-cl02-apic03
```

`username` and `password` can be defined either globally, or per-cluster in the event that credentials are not stored centrally.

## Actions

## Sensors
* Tenant Sensor
