import os
import json
import tempfile
import datetime
from arnparse import arnparse
from cwsearch_utils import infinstor_lock, infinstor_dbutils
import sqlite3

def my_sort_fnx(a):
    return a[0]

def my_filelisting_sort_fnx(a):
    return a[2]

def get_files_list_one_group(s3client, bucket, prefix, olg, resources, rv):
    print(f"get_files_list_one_group: Entered. prefix={prefix}, group={olg}, resources={resources}")
    if olg:
        prefix = prefix + olg
    nextContinuationToken = None
    while True:
        if nextContinuationToken:
            resp = s3client.list_objects_v2(Bucket=bucket, Delimiter='/', Prefix=prefix, ContinuationToken=nextContinuationToken)
        else:
            resp = s3client.list_objects_v2(Bucket=bucket, Delimiter='/', Prefix=prefix)
        if 'Contents' in resp:
            for one in resp['Contents']:
                nm = one['Key']
                if not nm[-1] == '/':
                    if resources:
                        for res in resources:
                            arn = arnparse(res)
                            munged_resource_id = arn.resource.replace('/', '_')
                            if munged_resource_id in nm:
                                print(f"get_files_list_one_group: Adding. munged_resource_id={munged_resource_id}, nm={nm}")
                                rv.append([nm, one['Size'], one['LastModified']])
                            else:
                                print(f"get_files_list_one_group: Skipping. munged_resource_id={munged_resource_id}, nm={nm}")
                    else:
                        rv.append([nm, one['Size'], one['LastModified']])
        if not resp['IsTruncated']:
            break
        else:
            nextContinuationToken = resp['NextContinuationToken']

def resources_for_tag(resources, tag):
    retval = []
    if tag == 'notag':
        for res in resources:
            retval.append(res['ResourceARN'])
        print(f"resources_for_tag: tag={tag}, rv={retval}")
        return retval
    else:
        ind = tag.find('=')
        if ind == -1:
            print('resources_for_tag: tag does not have = ???')
            return None
        tagkey = tag[:ind]
        tagval = tag[ind+1:]
        for res in resources:
            for tg in res['Tags']:
                if tg['Key'] == tagkey:
                    retval.append(res['ResourceARN'])
        print(f"resources_for_tag: tag={tag}, rv={retval}")
        return retval

def get_files_list(s3client, bucket, prefix, log_groups, tag, resources):
    rv = []
    if log_groups:
        lga = log_groups.split(',')
        for olg in lga:
            get_files_list_one_group(s3client, bucket, prefix, olg.replace('/', '_'), None, rv)
    elif tag:
        rft = resources_for_tag(resources, tag)
        if rft:
            get_files_list_one_group(s3client, bucket, prefix, None, rft, rv)
        else:
            print(f"tag specified={tag}, but could not get resources for tag. Ignoring tag..")
            get_files_list_one_group(s3client, bucket, prefix, None, None, rv)
    else:
        get_files_list_one_group(s3client, bucket, prefix, None, None, rv)
    rv.sort(reverse=True, key=my_filelisting_sort_fnx)
    print(f"get_files_list: log_groups={log_groups}, tag={tag}, rv={rv}")
    return rv

def process_file(client, bucket, key, dstcon, infinstor_time_spec, tag):
    if tag:
        use_tag=tag
    else:
        use_tag='notag'
    try:
        dstcur = dstcon.cursor()

        dnm = os.path.join('/tmp', key[key.rindex('/') + 1:])
        print(f"Downloading object {key} to local file {dnm}")
        client.download_file(bucket, key, dnm)

        srccon = sqlite3.connect(dnm)
        srccur = srccon.cursor()
        res = srccur.execute(f"SELECT name, timestamp, link, msg FROM links WHERE tag='{use_tag}'")
        while True:
            one_entry = res.fetchone()
            if not one_entry:
                break
            name = one_entry[0]
            estr = f"INSERT INTO links VALUES ('{use_tag}', '{one_entry[0]}', '{one_entry[1]}', '{one_entry[2]}', '{one_entry[3]}')"
            print(f"process_file: executing {estr}")
            dstcur.execute(estr)
        dstcon.commit()
        os.remove(dnm)
        return True
    except Exception as e:
        print(f"Caught {e} while downloading {key} from bucket {bucket}. Ignoring and trying next object..")
    return False

def populate_names(bucket, prefix, infinstor_time_spec, resources, log_groups, tag):
    print(f'populate_names: Entered. bucket={bucket}, prefix={prefix}, infinstor_time_spec={infinstor_time_spec}, log_groups={log_groups}, tag={tag}')
    start_time = datetime.datetime.utcnow()

    prefix = prefix.rstrip('/') + '/'

    import boto3
    # first list files in reverse chrono order
    try:
        s3client = boto3.client('s3', infinstor_time_spec=infinstor_time_spec)
        files = get_files_list(s3client, bucket, prefix, log_groups, tag, resources)
    except Exception as ex:
        print(f'Caught {ex} while list_objects_v2 of {bucket} prefix {prefix} time {infinstor_time_spec}', flush=True)
        return False

    if not files:
        print(f'No files found. bucket={bucket}, prefix={prefix}, infinstor_time_spec={infinstor_time_spec}, log_groups={log_groups}, tag={tag}')
        return False

    # next, read each file and fill aggregated db
    if tag:
        tfname = f"names-{tag}.db"
    else:
        tfname = "names.db"
    tdir = tempfile.mkdtemp()
    tfile = os.path.join(tdir, tfname)
    con = sqlite3.connect(tfile)
    infinstor_dbutils.create_table(con)

    total_sz = 0
    for one_entry in files:
        print(f"Processing file {one_entry[0]} last_modified {one_entry[2]}")
        if process_file(s3client, bucket, one_entry[0], con, infinstor_time_spec, tag):
            total_sz = total_sz + one_entry[1]
        if total_sz > (512 * 1024 * 1024):
            print(f"Stopping after processing files of size {total_sz}")
            break
        else:
            print(f"Continuing after processing {total_sz} bytes")
        tnow = datetime.datetime.utcnow()
        delta = tnow - start_time
        if delta.total_seconds() > 600:
            print(f"Stopping after working for {delta.total_seconds()} seconds")
            break
        else:
            print(f"Continuing after working for {delta.total_seconds()} seconds")
    con.close()

    # finally, write ner_entites to s3
    object_name = f"{prefix}index/{infinstor_time_spec}/{tfname}"
    try:
        response = s3client.upload_file(tfile, bucket, object_name)
    except Exception as ex:
        print(f"Caught {ex} while uploading names entry for timespec {infinstor_time_spec}. Objectname={object_name}")

    return True
