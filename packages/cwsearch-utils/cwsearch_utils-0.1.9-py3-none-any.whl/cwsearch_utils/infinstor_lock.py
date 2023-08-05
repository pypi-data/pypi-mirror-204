import datetime
import tempfile
import json
import os
import sqlite3

def set_start(s3client, bucket, prefix, infinstor_time_spec):
    import botocore
    # this is not really a locking mechanism - the prev ddb conditional put based code was
    status_object_name = f"{prefix}/index/{infinstor_time_spec}/names.db.creating"
    try:
        metadata = s3client.head_object(Bucket=bucket, Key=status_object_name)
        creation_time = metadata['LastModified']
        tnow = datetime.datetime.utcnow()
        delta = tnow - creation_time
        if delta.total_seconds() > 900:
            print(f"Status object {creation_time} older than 900 seconds {tnow} for {infinstor_time_spec}. This lambda invocation continuing ..")
            return True
        else:
            print(f"Status object {creation_time} less than 900 seconds old {tnow} for {infinstor_time_spec}. This lambda invocation exiting ..")
            return False
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{status_object_name} does not exist. This lambda invocation creating status object and continuing..")
        else:
            print(f"Caught {e} while reading {status_object_name}. This lambda invocation exiting..")
            return False

    fd, tfile = tempfile.mkstemp()
    try:
        response = s3client.upload_file(tfile, bucket, status_object_name)
        print(f"{status_object_name} does not exist. This lambda invocation successfully created status object {status_object_name} and continuing..")
        return True
    except botocore.exceptions.ClientError as e:
        print(f"Caught {e} while creating status file {status_object_name}. This lambda invocation exiting..")
        return False

def load_from_db(fn, tag):
    rv = {}
    con = sqlite3.connect(fn)
    cur = con.cursor()
    if not tag:
        tag = 'notag'
    print(f'load_from_db: Loading fn={fn}, tag={tag}')
    res = cur.execute(f"SELECT name, timestamp, link, msg FROM links WHERE tag='{tag}'")
    while True:
        one_entry = res.fetchone()
        if not one_entry:
            break
        name = one_entry[0]
        if name in rv:
            rv[name].append((one_entry[1], one_entry[2], one_entry[3]))
        else:
            rv[name] = [(one_entry[1], one_entry[2], one_entry[3])]
    return rv

# returns 'NotPresent'|'Creating'|'Ready'|'CreationFailed', names|None
def get_cache_entry(bucket, prefix, infinstor_time_spec, tag, head_only):
    import boto3
    import botocore
    s3client = boto3.client('s3')
    if tag:
        object_name = f"{prefix}/index/{infinstor_time_spec}/names-{tag}.db"
    else:
        object_name = f"{prefix}/index/{infinstor_time_spec}/names.db"

    print(f'get_cache_entry: object={object_name}, head_only={head_only}')

    if head_only:
        try:
            metadata = s3client.head_object(Bucket=bucket, Key=object_name)
            return 'Ready', {}
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"{object_name} does not exist. Trying status object")
            else:
                print(f"Caught {e} while reading {object_name}. Returning NotPresent")
                return 'NotPresent', None
    else:
        lfn = "/tmp/names.db"
        try:
            s3client.download_file(bucket, object_name, lfn)
            dct = load_from_db(lfn, tag)
            os.remove(lfn)
            if dct:
                return 'Ready', dct
            else:
                return 'Ready', {}
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print(f"{object_name} does not exist. Trying status object")
            else:
                print(f"Caught {e} while reading {object_name}. Returning NotPresent")
                return 'NotPresent', None

    status_object_name = f"{prefix}/index/{infinstor_time_spec}/names.db.creating"
    try:
        metadata = s3client.head_object(Bucket=bucket, Key=status_object_name)
        creation_time = metadata['LastModified']
        tnow = datetime.datetime.utcnow()
        delta = creation_time - tnow
        if delta.total_seconds() > 900:
            print(f"Status object {creation_time} older than 900 seconds {tnow} for {infinstor_time_spec}. CreationFailed..")
            return 'CreationFailed', None
        else:
            print(f"Status object {creation_time} less than 900 seconds old {tnow} for {infinstor_time_spec}. waiting..")
            return 'Creating', None
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(f"{status_object_name} does not exist. Returning NotPresent")
            return 'NotPresent', None
        else:
            print(f"Caught {e} while reading {status_object_name}. Returning CreationFailed")
            return 'CreationFailed', None

