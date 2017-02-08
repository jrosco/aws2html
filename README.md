#  aws2html

####Under Development (2.0)

Use the aws-cli and pipe output to this script and it will convert the json output to html and open in the OS's default browser (see example below)

*Note:* _Ensure you have `output = json` in your `~./aws/config` file_

##Install:

####Pull lasest repository

```
git clone https://github.com/jrosco/aws2html.git
```

####Install on local machine
```
sudo python setup.py install
```

##Usage:
####Example:
```
aws ec2 describe-instances --filters Name=tag-value,Values="*serverName*"  | aws2html
```

####Help:
```
aws2html --help
```

*Note:* _Currently only works with ec2 describe-instances, I'll be developing this tool to support rds, cloudformtion, route53 and more_
