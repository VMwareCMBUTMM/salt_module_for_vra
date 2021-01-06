create_network_profile_aws:
  module.run:
    - name: vra.create_network_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: AWS-Networks
    - region_name: us-west-1
    
add_network_to_profile_aws:
  module.run:
    - name: vra.add_network_to_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: AWS-Networks
    - region_name: us-west-1
    - fabric_net_name: appnet-public-dev
    
create_network_profile_azure:
  module.run:
    - name: vra.create_network_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: Azure-Networks
    - region_name: eastus
    
add_network_to_profile_azure:
  module.run:
    - name: vra.add_network_to_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: Azure-Networks
    - region_name: eastus
    - fabric_net_name: SPC-50
    
create_network_profile_vsphere:
  module.run:
    - name: vra.create_network_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: vSphere-Networks
    - region_name: Datacenter:datacenter-2
    
add_network_to_profile_vsphere:
  module.run:
    - name: vra.add_network_to_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: vSphere-Networks
    - region_name: Datacenter:datacenter-2
    - fabric_net_name: App
    
add_nsxt_network_to_profile_vsphere:
  module.run:
    - name: vra.add_nsxt_network_to_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: vSphere-Networks
    - region_name: Datacenter:datacenter-2
    - fabric_net_name: Web
    
tag_fabric_network_vsphere:
  module.run:
    - name: vra.tag_fabric_network
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - fabric_net_name: Web
    - tag_key: env
    - tag_value: vsphere
    
add_security_group_vsphere_web:
  module.run:
    - name: vra.add_sec_group_vsphere_net_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: vSphere-Networks
    - secgroup_name: Web
    
add_security_group_vsphere_db:
  module.run:
    - name: vra.add_sec_group_vsphere_net_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: vSphere-Networks
    - secgroup_name: DB
    
configure_ondemand_secgroups_vsphere:
  module.run:
    - name: vra.config_ondemand_sec_groups_vsphere_network_profile
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - net_profile_name: vSphere-Networks
    - edge_router_name: "Edge - Cluster"
    - t0_router_name: T0