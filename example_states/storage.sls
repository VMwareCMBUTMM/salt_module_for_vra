create_storage_profile_aws:
  module.run:
    - name: vra.create_aws_storage_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: AWS-Storage
    - region_name: us-west-1
    - tag_key: env
    - tag_value: aws
    
create_storage_profile_azure:
  module.run:
    - name: vra.create_azure_storage_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: Azure-Storage
    - region_name: eastus
    - tag_key: env
    - tag_value: azure
    
create_storage_profile_vsphere:
  module.run:
    - name: vra.create_vsphere_storage_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: vSphere-Storage
    - region_name: Datacenter:datacenter-2
    - datastore_name: sc2c01vsan01
    - tag_key: env
    - tag_value: vsphere