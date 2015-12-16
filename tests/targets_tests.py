import boto
import pandas as pd

from testfixtures import tempdir
from unittest import TestCase

from moto import mock_s3

from fireflower.targets import S3CSVTarget


class TargetsTests(TestCase):
    @mock_s3
    @tempdir()
    def test_s3_compressed_csv_target(self, tempd):
        conn = boto.connect_s3()
        bucket_name = 'some_bucket'
        file_name = 'some_file.csv.gz'
        dest_path = 's3://%s/%s' % (bucket_name, file_name)
        conn.create_bucket(bucket_name)
        df = pd.DataFrame(index=range(1), data={'a': [1]})
        s = S3CSVTarget(dest_path, compressed=True)
        s.write_csv(df, index=False)
        read_result = s.read_csv()
        self.assertDictEqual(df.to_dict(), read_result.to_dict())

    @mock_s3
    @tempdir()
    def test_s3_uncompressed_csv_target(self, tempd):
        conn = boto.connect_s3()
        bucket_name = 'some_bucket'
        file_name = 'some_file.csv'
        dest_path = 's3://%s/%s' % (bucket_name, file_name)
        conn.create_bucket(bucket_name)
        df = pd.DataFrame(index=range(1), data={'a': [1]})
        s = S3CSVTarget(dest_path, compressed=False)
        s.write_csv(df, index=False)
        read_result = s.read_csv()
        self.assertDictEqual(df.to_dict(), read_result.to_dict())
