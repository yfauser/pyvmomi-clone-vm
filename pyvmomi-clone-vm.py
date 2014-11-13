'''
Created on 25.10.2014

@author: yfauser
'''
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import vmutils

username = 'root'
password = 'vmware'
vcenter_ip = 'localhost'
vcenter_port = '10504'
cluster_name = 'Management'
template_name = 'Windows2008R2-Template'
customization_spec_name = 'Windows2008Prep'
new_vm_name = 'MyClonedWin2008'

# This will connect us to vCenter
s = SmartConnect(host=vcenter_ip, user=username, pwd=password, port=vcenter_port)

# With this we are searching for the MOID of the VM to clone from
template_vm = vmutils.get_vm_by_name(s, template_name)

# This gets the MOID of the Guest Customization Spec that is saved in the vCenter DB
guest_customization_spec = s.content.customizationSpecManager.GetCustomizationSpec(name=customization_spec_name)

# This will retrieve the Cluster MOID
cluster = vmutils.get_cluster(s, cluster_name)

# This constructs the reloacate spec needed in a later step by specifying the default resource pool (name=Resource) of the Cluster
# Alternatively one can specify a custom resource pool inside of a Cluster
relocate_spec = vim.vm.RelocateSpec(pool=cluster.resourcePool)

# This constructs the clone specification and adds the customization spec and location spec to it
cloneSpec = vim.vm.CloneSpec(powerOn=True, template=False, location=relocate_spec, customization=guest_customization_spec.spec)

# Finally this is the clone operation with the relevant specs attached
clone = template_vm.Clone(name=new_vm_name, folder=template_vm.parent, spec=cloneSpec)

Disconnect(s)

