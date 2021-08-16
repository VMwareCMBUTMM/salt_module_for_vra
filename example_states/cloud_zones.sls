create_aws_cloud_zone:
  module.run:
    - name: vra.create_cloudzone
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - czname: AWS-Cloud-Account
    - region_name: us-west-1
    - caname: AWS-Cloud-Account
    
create_azure_cloud_zone:
  module.run:
    - name: vra.create_cloudzone
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - czname: Azure-Cloud-Account
    - region_name: eastus
    - caname: Azure-Cloud-Account
    
create_vsphere_cloud_zone:
  module.run:
    - name: vra.create_cloudzone
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - czname: vSphere-Cloud-Account
    - region_name: Datacenter:datacenter-2
    - caname: vSphere-Cloud-Account
    - folder: Demo
    
tag_aws_cloud_zone:
  module.run:
    - name: vra.tag_cloudzone
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - czname: AWS-Cloud-Account
    - tag_key: env
    - tag_value: aws
    
tag_azure_cloud_zone:
  module.run:
    - name: vra.tag_cloudzone
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - czname: Azure-Cloud-Account
    - tag_key: env
    - tag_value: azure
    
tag_vsphere_cloud_zone:
  module.run:
    - name: vra.tag_cloudzone
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - czname: vSphere-Cloud-Account
    - tag_key: env
    - tag_value: vsphere
