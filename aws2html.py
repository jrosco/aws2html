#!/usr/bin/env python
from __future__ import print_function

import sys
import os
import tempfile
import json
from string import Template
import webbrowser

__html_template='templates/aws_template.html'
__html_header='templates/header.html'
__html_footer='templates/footer.html'
__output_html=tempfile.mkstemp(dir='/tmp/', prefix='AWS-HTML-', suffix='.html')[1]

# HTML Wrapper
def build_html(obj):
    def ec2_wrapper(output):
    	template_engine(ec2_stuff=output)
    return ec2_wrapper

@build_html
def build_ec2(*args, **kwargs):
    return

# Template Engine
def template_engine(ec2_stuff=None, rds_stuff=None):
    try:
        html_file = open(__html_template)
        src = Template(html_file.read())
        ec2_id = ec2_stuff[0]['InstanceId']
        launch_time = ec2_stuff[0]['LaunchTime']
        public_dns_name = ec2_stuff[0]['PublicDnsName']
        instance_type = ec2_stuff[0]['InstanceType']
        #tags = ec2_stuff[0]['Tags']
        list = ['first', 'second', 'third']
        d={'ec2_id':ec2_id, 'launch_time':launch_time, 'list':'\n'.join(list), 'public_dns_name':public_dns_name, 'instance_type':instance_type}
        result = src.substitute(d)

        with open(__output_html, 'a') as body:
            body.write(result)
    except Exception, e:
        print(e)

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
                    build_ec2(output=value)
                except Exception, e:
                    print(e)
        header_footer(source_type='footer')
        webbrowser.open('file://' + os.path.realpath(__output_html))
    except Exception, e:
        print('Incorrect Output Used - %s' % e)


if '__main__' == __name__:
    main()


