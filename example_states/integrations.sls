create_ansibletower_integration:
  module.run:
    - name: vra.create_ansibletower_integration
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: "Ansible Tower"
    - private_key: {{ pillar['vars']['password'] }}
    - private_id: admin
    - hostname: 10.176.144.176
    
create_ansible_oss_integration:
  module.run:
    - name: vra.create_ansible_oss_integration
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: "Field Demo Ansible OSS"
    - private_key: {{ pillar['vars']['password'] }}
    - private_id: root
    - hostname: ansiblecm.cmbu.local
    - inventory_path: "/etc/ansible/hosts"
    
create_github_saas_integration:
  module.run:
    - name: vra.create_github_saas_integration
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: Field_Demo_Github
    - private_key: {{ pillar['vars']['github_key'] }}
    
create_actions_content_source:
  module.run:
    - name: vra.create_actions_content_source
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: Field_Demo_Actions
    - int_name: Field_Demo_Github
    - proj_name: "Field Demo"
    - repo: mcclanc/vra8-content
    - branch: master
    - path: actions

create_blueprint_content_source:
  module.run:
    - name: vra.create_blueprint_content_source
    - url: {{ pillar['vars']['url'] }}
    - username: {{ pillar['vars']['username'] }}
    - password: {{ pillar['vars']['password'] }}
    - m_name: Field_Demo_Blueprints
    - int_name: Field_Demo_Github
    - proj_name: "Field Demo"
    - repo: mcclanc/vra8-content
    - branch: master
    - path: blueprints