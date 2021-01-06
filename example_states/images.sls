create_image_profile_aws:
  module.run:
    - name: vra.create_image_mapping
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - profile_name: aws
    - image_name: Ubuntu
    - image_id: ami-03659409b9c7d0c5f
    - region_name: us-west-1
    
create_image_profile_azure:
  module.run:
    - name: vra.create_image_mapping
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - profile_name: azure
    - image_name: Ubuntu
    - image_id: "Canonical:UbuntuServer:16.04-LTS:latest"
    - region_name: eastus
    
create_image_profile_vsphere:
  module.run:
    - name: vra.create_image_mapping
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - profile_name: vsphere
    - image_name: Ubuntu
    - image_id: ubuntu-16-pod
    - region_name: Datacenter:datacenter-2