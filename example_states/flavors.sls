create_aws_flavor_small:
  module.run:
    - name: vra.create_cloud_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: aws
    - mapping_name: small
    - cloud_instance_name: t2.small
    - region_name: us-west-1
    
update_aws_flavor_medium:
  module.run:
    - name: vra.update_cloud_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: aws
    - mapping_name: medium
    - cloud_instance_name: t2.medium
    
update_aws_flavor_large:
  module.run:
    - name: vra.update_cloud_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: aws
    - mapping_name: large
    - cloud_instance_name: t2.large
    
create_azure_flavor_small:
  module.run:
    - name: vra.create_cloud_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: azure
    - mapping_name: small
    - cloud_instance_name: Standard_B1ms
    - region_name: eastus
    
update_azure_flavor_medium:
  module.run:
    - name: vra.update_cloud_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: azure
    - mapping_name: medium
    - cloud_instance_name: Standard_B2s
    
update_azure_flavor_large:
  module.run:
    - name: vra.update_cloud_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: azure
    - mapping_name: large
    - cloud_instance_name: Standard_B2ms
    
create_vsphere_flavor_small:
  module.run:
    - name: vra.create_vsphere_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: vsphere
    - mapping_name: small
    - cpu_count: 1
    - mem_count: 1
    - region_name: Datacenter:datacenter-2
    
update_vsphere_flavor_medium:
  module.run:
    - name: vra.update_vsphere_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: vsphere
    - mapping_name: medium
    - cpu_count: 1
    - mem_count: 2
    
update_vsphere_flavor_large:
  module.run:
    - name: vra.update_vsphere_flavor
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - flavor_name: vsphere
    - mapping_name: large
    - cpu_count: 2
    - mem_count: 4