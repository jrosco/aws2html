# aws2html

Under Development

Example Usage:
```
aws ec2 describe-instances --filters Name=tag-value,Values="*serverName*"  | aws2html.py
```

*Note:* _Currently only works with ec2 describe-instances, I'll be developing this tool to support rds, cloudformtion, route53 and more_
