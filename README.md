# swinds-ansible-inv
Dynamic Inventory for Solar Winds hosts in Ansible

This python script connects to Solar Winds via rest API to create a dynamic inventory in Ansible.  JSON data is pulled into the python script via rest https API call to Orion.   Groups  are based on Vendor.  It pulls the IPAddress for hosts field.  The impetus for this script was for network devices.  As such if the IPAddress was chosen over say hostname.  If one wanted to use hostnames replacing the IPAdrress string to SysName should produce that result.  One could also change the Vendor to somethign else.  I would recommend downloading the SWQL Studio and look under Orion.Nodes table for more options.

Any suggestions/code to improve would be awesome. 
