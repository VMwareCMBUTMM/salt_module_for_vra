create_aws_cloud_account:
  module.run:
    - name: vra.create_aws_ca
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - aws_key_id: {{ pillar['vars']['aws_key_id'] }}
    - aws_access_key: {{ pillar['vars']['aws_access_key'] }}
    - m_name: AWS-Cloud-Account
    - region_name: us-west-1,us-west-2
    
create_azure_cloud_account:
  module.run:
    - name: vra.create_azure_ca
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - sub_id: {{ pillar['vars']['sub_id'] }}
    - ten_id: {{ pillar['vars']['ten_id'] }}
    - app_id: {{ pillar['vars']['app_id'] }}
    - app_key: {{ pillar['vars']['app_key'] }}
    - m_name: Azure-Cloud-Account
    - region_name: eastus
    
create_vsphere_cloud_account:
  module.run:
    - name: vra.create_vsphere_ca
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - vc_hostname: {{ pillar['vars']['vc_hostname'] }}
    - vc_username: {{ pillar['vars']['vc_username'] }}
    - vc_password: {{ pillar['vars']['vc_password'] }}
    - m_name: vSphere-Cloud-Account
    - region_name: Datacenter:datacenter-2
    
create_nsxt_cloud_account:
  module.run:
    - name: vra.create_nsxt_ca
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - nsx_hostname: {{ pillar['vars']['nsx_hostname'] }}
    - nsx_username: {{ pillar['vars']['nsx_username'] }}
    - nsx_password: {{ pillar['vars']['nsx_password'] }}
    - m_name: NSXT-Cloud-Account
    - ca_name: vSphere-Cloud-Account
