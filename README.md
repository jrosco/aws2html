#  aws2html

####Under Development (2.0)

Use the aws-cli and pipe output to this script and it will convert the json output to html and open in the OS's default browser (see example below)

##Install:

```
sudo python setup.py install
```

##Usage:
example:
```
aws ec2 describe-instances --filters Name=tag-value,Values="*serverName*"  | aws2html
```

*Note:* _Currently only works with ec2 describe-instances, I'll be developing this tool to support rds, cloudformtion, route53 and more_
