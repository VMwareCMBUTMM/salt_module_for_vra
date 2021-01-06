vra_configuration:
  salt.state:
    - tgt: 'sse.cmbu.local-master'
    - tgt_type: glob
    - sls: 
      - vra_config.flavors