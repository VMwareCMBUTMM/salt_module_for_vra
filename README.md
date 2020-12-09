# vRealize Automation SaltStack Module

This vRealize Automation Module for SaltStack provides functionality to configure and perform various functions within vRealize Automation. You can do things like setup cloud accounts, cloud zones, tags, blueprints, flavor mappings, enable services and much more.

## Getting Started

vRealize Automation needs to be installed and running and a version of SaltStack needs to also be up and running. There are lists of various functions at the bottom of this readme.

### Prerequisites

vRealize Automation 8?

```
Give examples
```

### Installing

All salt modules get loaded on the master at /srv/salt/_modules

Once copied then run 

```
saltutil.sync_modules
```

In order to access docstrings: 

```
salt '*' sys.doc
```

## Running Commands from CLI Example 

```
vra.tag_cloudzone myvra.company.local admin password "AWS-Cloud-Account / us-west-1" env aws
```

(args = url, user, password, cloudzone/region, tag_key, tag_value)

### Running vRA Module Jobs from SaltStack Config

FooFooFoo

```
Examples..
```

## Links to Documentation

* [vRealize Automation](https://docs.vmware.com/en/vRealize-Automation/index.html) 
* [SaltStack Config](https://docs.vmware.com/en/vRealize-Automation/8.1/SaltStackConfig_Help_v64.pdf) 

## Contributing


## Versioning

version 1.0.0

## Authors

* **Chris McClanahan** 

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.


## Acknowledgments

## Appendix
 vRealize Automation SaltStack module

 Cloud Accounts:
  Create AWS Cloud Account:
   - required: url,
               access_key,
               aws_key_id,
               aws_access_key,
               name

  Create Azure Clou Account:
   - required: url,
               name,
               access_key,
               sub_id,
               ten_id,
               app_id,
               app_key,
               region_id

 Create vSphere Cloud Account:
   - required: url,
               access_key,
               name,
               vc_hostname,
               vc_username,
               vc_password,
               region_id
