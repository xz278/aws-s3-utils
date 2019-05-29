# aws-utils

Utility functions for aws services:

- s3

## Usage

### s3_utils
```python
from aws_utils import s3_utils as s3

# create a client wrapper
s3_client = s3.get_client()

# list all buckets available in current s3 account
buckets = s3_client.list_bucket()

# list all object in one bucket
objects = s3_client.list_object(
    bucket='nanchong',
    prefix='MCR.REPORTS/LOANS/',
    reg_match=r'.*/MCR.LOAN.REP.*'
)

# download an object
s3_client.download_object(
    bucket='nanchong',
    key='MCR.REPORTS/LOANS/MCR.LOAN.REP_20140531',
    filename='test_s3_dl.txt'
)
```