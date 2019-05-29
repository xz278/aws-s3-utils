# -*- coding: utf-8 -*-
"""
Utility functions for connecting to s3.
"""
import boto3
import pandas as pd
import os
import re
import traceback


class Client:
    """
    A wrapper class for boto3.client.S3 object.
    """
    def __init__(self):
        self.client = boto3.client('s3')
        self.list_type = 'dataframe'
        
    def set_list_type(ret_type):
        if ret_type not in ['dataframe', 'list']:
            raise Exception("Only 'dataframe' and 'list' are supported, met '{}'".format(ret_type))
        else:
            self.list_type = ret_type

    def list_bucket(self, ret_type=None):
        """
        Return the name and creation date for all buckets in current s3 account. 
        """
        response = self.client.list_buckets()
        bucket_list = [[r['Name'], r['CreationDate'].strftime('%Y/%m/%d %H:%M:%S')]
                       for r in response['Buckets']]

        if ret_type is None:
            ret_type = self.list_type
        else:
            if ret_type not in ['dataframe', 'list']:
                raise Exception("Only 'dataframe' and 'list' are supported, met '{}'".format(ret_type))

        if ret_type == 'dataframe':
            bucket_list = pd.DataFrame(bucket_list, columns=['Name', 'CreationDate'])
        return bucket_list

    def list_object(self, bucket, prefix=None, reg_match=None, show_all=False, **kwargs):
        """
        List objects (files) in a bucket.
        
        >>> objects = s3_client.list_object(Bucket='nanchong',
                                            Prefix='MCR.REPORTS/LOANS/',
                                            reg_match=r'.*/MCR.LOAN.REP.*')
        """
        paginator = self.client.get_paginator('list_objects')
        pages = paginator.paginate(Bucket=bucket, Prefix=prefix, **kwargs)
        tmp = []
        for page in pages:
            tmp.extend(page['Contents'])

        objects = pd.DataFrame(tmp)
        
        if reg_match is not None:
            r = re.compile(reg_match)
            objects = objects.loc[objects['Key'].apply(lambda x: r.match(x) is not None)]

        objects['LastModified'] = objects['LastModified']\
                                  .apply(lambda x: x.strftime('%Y/%m/%d %H:%M:%S'))
        objects['Owner'] = objects['Owner'].apply(lambda x: x['ID'])
        objects['Basename'] = objects['Key'].apply(lambda x: os.path.basename(x))
        objects = objects.sort_values('Key')
        
        if not show_all:
            return objects[['Basename', 'Key']]
        else:
            return objects
        
    def download_object(self, bucket, key, filename):
        """
        Download object.
        """
        try:
            with open(filename, 'wb') as f:
                self.client.download_fileobj(bucket, key, f)
            print("'{}' saved to '{}'".format(key, filename))
        except:
            raise Exception(traceback.format_exc())


def get_client():
    """
    Return a s3 client wrapper.
    """
    return Client()
