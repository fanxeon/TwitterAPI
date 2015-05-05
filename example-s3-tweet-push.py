#!/usr/bin/env python
#
# Example tweet push to S3.
# Shows how to save JSON to S3.
# 
# EC2_ACCESS_KEY, EC2_SECRET_KEY, S3_URL
# must be exported environment variables.
# These can be downloaded from NECTAR access and security tab.

import boto.s3.connection
import boto.exception
import boto
from boto.s3.key import Key
import os
import json
from urlparse import urlparse

# This is a workaround to ensure API works for both OpenStack Swift
# and EC2.
# if not boto.config.get('s3', 'use-sigv4'):
#     boto.config.add_section('s3')
#     boto.config.set('s3', 'use-sigv4', 'True')
# if not boto.config.get('Boto', 'emr_region_name'):
#     boto.config.add_section('Boto')
#     boto.config.set('Boto', 'emr_region_name', 'Melbourne')
# This is another workaround (setting environment variable defined below)
# os.environ['S3_USE_SIGV4'] = 'True'

# Build connection
s3_url = urlparse(os.environ['S3_URL'])
conn = boto.s3.connection.S3Connection(
  aws_access_key_id=os.environ['EC2_ACCESS_KEY'],
  aws_secret_access_key=os.environ['EC2_SECRET_KEY'],
  port=s3_url.port,
  host=s3_url.hostname,
  is_secure=True,
  validate_certs=False,
  calling_format=boto.s3.connection.OrdinaryCallingFormat()
)

# Create bucket as idempotent operation
# Ignores bucket-already-exists error (409)
bucket_name = 'twitter'
bucket_already_exist_code = 409
try:
    created_bucket = conn.create_bucket(bucket_name)
except boto.exception.S3CreateError as e:
    if e.status == bucket_already_exist_code:
        pass
    else:
        raise e

# Access bucket
# NOTE: Method get_bucket can fail due to divergence between
#       OpenStack and EC2 API even if signature V4 is used.
#       Use method get_all_buckets() as 
#       workaround for both APIs (undocumented online).
#       This problem is declared in issue #2916 on github.
# bucket = conn.get_bucket(bucket_name)
def get_bucket(conn, bucket_name):
    return filter(lambda x: x.name == bucket_name, conn.get_all_buckets())[0]

bucket = get_bucket(conn, bucket_name)

# Save objects to bucket (idempotent)
with open('./example-tweet.json') as handle:    
    twitter_response = json.load(handle)

for tweet in twitter_response['statuses']:
    key = Key(bucket)
    key.key = tweet['id_str']
    key.set_contents_from_string(json.dumps(tweet))

# And we're done!
