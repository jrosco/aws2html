#!/usr/bin/env python

'''
Example : aws ec2 describe-instances --filters Name=tag-value,Values="*prod*"  | aws2html.py

'''
from __future__ import print_function

import sys
import os
from os.path import expanduser
import tempfile
import json
from string import Template
import webbrowser
import ConfigParser
import urllib

__html_template = 'templates/aws_template.html'
__html_header = 'templates/header.html'
__html_footer = 'templates/footer.html'
__output_html = tempfile.mkstemp(dir='/tmp/', prefix='AWS-HTML-', suffix='.html')[1]

try:
    config = ConfigParser.ConfigParser()
    config.readfp(open(expanduser('~') + '/.aws/config'))
    default_region = config.get('default', 'region')
    aws_search_link = 'https://'+default_region+'.console.aws.amazon.com/ec2/v2/home?region='+default_region+'#Instances:tag:'
except Exception, e:
    print(e)

class Bunch(object):
  def __init__(self, adict):
    self.__dict__.update(adict)
    
# HTML Wrapper
def build_html(obj):
    def ec2_wrapper(output):
        template_engine(ec2_obj=output)

    return ec2_wrapper


@build_html
def build_ec2(*args, **kwargs):
    return


# Template Engine
def template_engine(ec2_obj=object, rds_obj=None):
    try:
        html_file = open(__html_template)
        src = Template(html_file.read())
        ec2_id = ec2_obj.InstanceId 
        launch_time = ec2_obj.LaunchTime 
        state = ec2_obj.State['Name']
        dns_name = ec2_obj.PrivateDnsName 
        ami_id = ec2_obj.ImageId 
        instance_type = ec2_obj.InstanceType 
        private_key = ec2_obj.KeyName 
        vpc_id = ec2_obj.KeyName 
        region = ec2_obj.Placement['AvailabilityZone']
        sec_grp = ec2_obj.SecurityGroups[0]['GroupId'] 
        ip_address = ec2_obj.PrivateIpAddress 
        tags = ec2_obj.Tags
	
        tag = tableizer(tags)

        d = {'ec2_id': ec2_id, 'launch_time': launch_time, 'list': tag, 'state': state, 'dns_name': dns_name,
             'instance_type': instance_type, 'private_key': private_key, 'region': region, 'vpc_id': vpc_id, 
             'sec_grp': sec_grp, 'ami_id': ami_id, 'ip_address': ip_address, 'default_region': default_region}
        result = src.substitute(d)

        with open(__output_html, 'a') as body:
            body.write(result)
    except Exception, e:
        print(e)


# Create a html table for tags
def tableizer(dict_list):

    tag_table = []

    for x in dict_list:
        tag_table.append('%s => <a href=%s%s=%s target=_blank>%s</a> <br>' % (x['Key'].encode('utf-8'), aws_search_link, x['Key'].encode('utf-8'),
            urllib.quote(x['Value'].encode('utf-8')), x['Value'].encode('utf-8')))
    tag_table.sort()
    return ''.join(tag_table)


# Build header and footer html
def header_footer(source_type=None):
    if source_type is 'header':
        read_header = open(__html_header).read()
        with open(__output_html, 'a') as header:
            header.seek(0)
            header.write(read_header)
    elif source_type is 'footer':
        read_footer = open(__html_footer).read()
        with open(__output_html, 'a') as footer:
            footer.seek(0)
            footer.write(read_footer)
    else:
        print('Incorrect source type given')
        sys.exit(1)


# Main run
def main():
    try:
        json_output = sys.stdin.read()
        aws_dict = json.loads(json_output)
        header_footer(source_type='header')
        for j in aws_dict.itervalues():
            for x in range(len(j)):
                try:
                    value = j[x]['Instances']
                    dict_obj = Bunch(value[0])
                    build_ec2(output=dict_obj)
                except Exception, e:
                    print(e)
        header_footer(source_type='footer')
        webbrowser.open('file://' + os.path.realpath(__output_html))
    except Exception, e:
        print('Incorrect Output Used - %s' % e)


def main_test():
    directories = [{u'Key': u'Name', u'Value': u'EDI Auto Scale'},
                   {u'Key': u'aws:autoscaling:groupName', u'Value': u'EDI Auto Scale Group'}]
    # filter(lambda (key, value): print('%s : %s' % (key[0],value[0])), directories)
    foo = map(lambda x: ('<p>' + x['Key'].encode('utf-8'), x['Value'].encode('utf-8')), directories)
    print(foo)


if '__main__' == __name__:
    main()


