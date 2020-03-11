PK       ! �I��  �  4   __pycache__/identify_instrument_files.cpython-36.pyc3
�~a^&  �               @   sb   d dl Z d dlZd dlmZ dd� Zedkr^ed� i Zi Zded< d	ed
< ded< eee� dS )�    N)�S3IOc             C   sv   t d� t | � t |dd� t| d �}|j| d | d d�}t dj|�dd� tj| �}i }||d	< d
tj|�d�S )NzRunning the envent handlerT)�flushzbucket-namezinstrument-input-folder�pattern)�prefixr   � �output��   )Z
statusCodeZbody)�printr   Z	list_keys�join�json�dumps)�event�contextZs3_L0Z	file_listZjson_strr   � r   �v/home/ubuntu/src/ausseabed-processing-pipeline/infra/src/lambda/identify_instrument_files/identify_instrument_files.py�lambda_handler   s    
r   �__main__ZStartingzausseabed-public-bathymetryzbucket-namez1L0/20fcc1c2-67c3-4d21-a0b2-5e9d16613211/Multibeamzinstrument-input-folderz*.allr   )	r   ZargparseZs3ior   r   �__name__r	   r   r   r   r   r   r   �<module>   s   PK       ! ��
L�  �     __pycache__/s3io.cpython-36.pyc3
�a^�  �               @   s^   d dl Z d dlZd dlmZ d dlmZ d dlZd dlZd dlZd dlm	Z	 G dd� d�Z
dS )�    N)�fnmatch)�Path)�ClientErrorc               @   s�   e Zd ZdZejd�ZdZdd� Zddd	�Z	d d
d�Z
dd� Zdd� Zdd� Zdd� Zd!dd�Zd"dd�Zdd� Zdd� Zdd� ZdS )#�S3IOz,
    From Wenjun's MB System's pipeline
    �s3Nc             C   s
   || _ dS )z5
        :param bucket: Name of a S3 bucket.
        N)�b_name)�selfZbucket� r	   �a/home/ubuntu/src/ausseabed-processing-pipeline/infra/src/lambda/identify_instrument_files/s3io.py�__init__   s    zS3IO.__init__� �*c             c   s&   x | j ||d�D ]}|d V  qW dS )z�
        Generate the matching keys (iterable) in an S3 bucket.

        :param prefix: required matching prefix (optional).
        :param pattern: required Unix filename matching pattern (optional).
        )�prefix�pattern�KeyN)�list_objects)r   r   r   �objr	   r	   r
   �	list_keys   s    zS3IO.list_keysc             c   s�   d| j i}t|t�r||d< xp| jjf |�}d|j� kr<dS x$|d D ]}t|d |�rF|V  qFW y|d |d< W q tk
r�   P Y qX qW dS )z�
        Generate the matching objects (iterable) in an S3 bucket.

        :param prefix: required matching prefix (optional).
        :param pattern: required Unix filename matching pattern (optional).
        �BucketZPrefixZContentsNr   ZNextContinuationTokenZContinuationToken)r   �
isinstance�strr   Zlist_objects_v2�keysr   �KeyError)r   r   r   �argsZrespr   r	   r	   r
   r   !   s    


zS3IO.list_objectsc             C   s@   y| j j| j|d�}W n  tk
r6 } zdS d}~X nX |d S )z�
        Retrieve an open StreamingBody object for a given key

        :param key: string
        :return: botocore.response.StreamingBody object.
                 If error, return None.
        )r   r   N�Body)r   �
get_objectr   r   )r   �keyZresponse�er	   r	   r
   r   8   s
    
zS3IO.get_objectc             C   s*   d}| j |�}|dk	r&|j� }|j�  |S )zk
        Retrieve the content of a given object

        :param key: string
        :return: bytes
        N)r   �read�close)r   r   �result�streamr	   r	   r
   �get_contentK   s    
zS3IO.get_contentc             C   s>   y| j j| j||d� W n  tk
r8 } zdS d}~X nX dS )z�
        Add an object to an Amazon S3 bucket.
        The object_data argument must be of type bytes.

        :param dest_key: string
        :param object_data: bytes of data
        :return: True if src_data was added, otherwise False
        )r   r   r   FNT)r   �
put_objectr   r   )r   Zdest_keyZobject_datar   r	   r	   r
   r#   Y   s    	
zS3IO.put_objectc             C   s*   |j jddd� | jj| j|t|�� dS )z�
        Download an object and save to the specified file.

        :param key: the key of an S3 object
        :param filepath: the destination Path object
        T)�parents�exist_okN)�parent�mkdirr   �download_filer   r   )r   r   �filepathr	   r	   r
   r(   m   s    zS3IO.download_filer   c             C   sJ   xD|D ]<}t |�}dj|jj|d� �}t |||j�}| j||� qW dS )a   
        Download objects and save to the specified directory.

        :param keys: a list of keys
        :param directory: the destination directory to save files
        :param cut_dirs: specified the number of directories to be ommited
                         to from a key
        �/N)r   �joinr&   �parts�namer(   )r   r   Z	directoryZcut_dirsr   ZpkZndir�pr	   r	   r
   �download_filesw   s
    	
zS3IO.download_filesc             C   s   | j jt|�| j||d� dS )z�
        Upload a file to the S3 bucket with a specified s3 key.

        :param local_filepath: the source file (Path object)
        :param s3_key: the key of the destination S3 object
        )Z	ExtraArgsN)r   �upload_filer   r   )r   Zlocal_filepathZs3_keyZ
extra_argsr	   r	   r
   r0   �   s    zS3IO.upload_filec             C   s6   dddt |�dj| j|�dg}tj|tjtjd� dS )z�
        Upload all files under a local directory
        to the S3 bucket with a specified s3 prefix.

        :param local_dirpath: the source directory (Path object)
        :param s3_prefix: the s3 prefix of the destination
        Zawsr   �synczs3://{}/{}/z--sse)�stdout�stderrN)r   �formatr   �
subprocessZ
check_callZDEVNULL)r   Zlocal_dirpathZ	s3_prefix�cmdr	   r	   r
   �upload_directory�   s
    
zS3IO.upload_directoryc             C   sd   dd� |D �}d}d}xH|| }|t ||� }t|�dkr<P | jj| j|dd�d� ||7 }qW dS )	zX
        Delete objects from an S3 bucket.

        :param keys: a list of keys
        c             S   s   g | ]}d |i�qS )r   r	   )�.0r   r	   r	   r
   �
<listcomp>�   s    z$S3IO.delete_keys.<locals>.<listcomp>i�  r   T)ZObjectsZQuiet)r   ZDeleteN)�slice�lenr   Zdelete_objectsr   )r   r   ZobjsZs_maxZs_startZs_stopZs_objsr	   r	   r
   �delete_keys�   s    zS3IO.delete_keysc             C   s   |d |d kS )z�
        Return True if obj1 is newer than obj2

        :param obj1: an S3 object return by list_objects()
        :param obj2: an S3 object return by list_objects()
        ZLastModifiedr	   )r   Zobj1Zobj2r	   r	   r
   �is_newer�   s    zS3IO.is_newer)r   r   )r   r   )r   )N)�__name__�
__module__�__qualname__�__doc__�boto3Zclientr   r   r   r   r   r   r"   r#   r(   r/   r0   r7   r<   r=   r	   r	   r	   r
   r   
   s   






r   )ZloggingrB   r   Zpathlibr   r5   ZtempfileZtimeZbotocore.exceptionsr   r   r	   r	   r	   r
   �<module>   s   PK       ! ���<	  <	     identify_instrument_files.pyimport json
import argparse
import re
from s3io import S3IO

def lambda_handler(event, context):
    print("Running the envent handler")

    print (event)
    print (context, flush=True)

    bucket_name=re.sub("/.*", "",event["src-instrument-location"].replace("s3://",""))
    instrument_input_folder=event["src-instrument-location"].replace("s3://{}/".format(bucket_name),"")

    print (bucket_name)
    print (instrument_input_folder)

    s3_L0 = S3IO(bucket_name)
    file_list = [ long_file.replace(instrument_input_folder,"").replace(event["pattern"],"") \
         for long_file in \
        s3_L0.list_keys(prefix=instrument_input_folder,pattern="*{}".format(event["pattern"]))]

    start = 0
    end = 1
    if ("start" in event):
        start=int(event["start"])
        
    if ("end" in event):
        end=int(event["end"])

    file_list = file_list[start:end] ## TODO Currently limited to ten to avoid input over capacity

    print (" ".join(file_list), flush=True)
    input_instructions = {"instrument-files":{ \
        "coverage-file":event["coverage-file"], \
        "instrument-file":[{\
        "s3_src_instrument":"{}{}{}".format(event["src-instrument-location"],name,event["pattern"]), \
        "s3_dest_las":"{}{}{}".format(event["src-las-location"],name,".las"), \
        "s3_dest_shp":{\
            "Name":"INPUT_FILES_{}".format(index),\
                "Value":"{}{}{}".format(event["src-shp-location"],name,".shp") \
                    }} \
            for (index,name) in zip(range(len(file_list)),file_list)]}}

    json_str = json.dumps(input_instructions, sort_keys=True, indent=4)
    print(json_str)

    output={}
    output["output"]=json_str
    return {
        'statusCode': 200,
        'body': input_instructions
    }


if __name__ == "__main__":
    print("Starting")
    event={}
    context={}
    event["src-instrument-location"]="s3://ausseabed-public-bathymetry/L0/20fcc1c2-67c3-4d21-a0b2-5e9d16613211/Multibeam/"
    #event["src-instrument-location"]="s3://bathymetry-survey-288871573946-1/Rawdata/"
    event["src-las-location"]="s3://bathymetry-survey-288871573946/L0Coverage/"
    event["src-shp-location"]="s3://bathymetry-survey-288871573946/L0Coverage/"
    event["pattern"]=".all"
    event["coverage-file"]="..."
    event["start"]=111
    event["end"]=111
    lambda_handler(event, context)

PK       ! �$�R�  �     s3io.pyimport logging
import boto3
from fnmatch import fnmatch
from pathlib import Path
import subprocess
import tempfile
import time
from botocore.exceptions import ClientError

class S3IO:
    """
    From Wenjun's MB System's pipeline
    """
    s3 = boto3.client('s3')
    b_name = None

    def __init__(self, bucket):
        '''
        :param bucket: Name of a S3 bucket.
        '''
        self.b_name = bucket

    def list_keys(self, prefix='', pattern='*'):
        '''
        Generate the matching keys (iterable) in an S3 bucket.

        :param prefix: required matching prefix (optional).
        :param pattern: required Unix filename matching pattern (optional).
        '''
        for obj in self.list_objects(prefix=prefix, pattern=pattern):
            yield obj['Key']

    def list_objects(self, prefix='', pattern='*'):
        '''
        Generate the matching objects (iterable) in an S3 bucket.

        :param prefix: required matching prefix (optional).
        :param pattern: required Unix filename matching pattern (optional).
        '''
        args = {'Bucket': self.b_name}
        if isinstance(prefix, str):
            args['Prefix'] = prefix

        while True:
            resp = self.s3.list_objects_v2(**args)
            if 'Contents' not in resp.keys():
                return
            for obj in resp['Contents']:
                if fnmatch(obj['Key'], pattern):
                    yield obj
            try:
                args['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    def get_object(self, key):
        '''
        Retrieve an open StreamingBody object for a given key

        :param key: string
        :return: botocore.response.StreamingBody object.
                 If error, return None.
        '''

        # Retrieve the object
        try:
            response = self.s3.get_object(Bucket=self.b_name, Key=key)
        except ClientError as e:
            # AllAccessDisabled error == bucket or object not found
            # logging.error(e)
            return None
        # Return an open StreamingBody object
        return response['Body']

    def get_content(self, key):
        '''
        Retrieve the content of a given object

        :param key: string
        :return: bytes
        '''
        result = None
        stream = self.get_object(key)
        if stream is not None:
            result = stream.read()
            stream.close()
        return result

    def put_object(self, dest_key, object_data):
        '''
        Add an object to an Amazon S3 bucket.
        The object_data argument must be of type bytes.

        :param dest_key: string
        :param object_data: bytes of data
        :return: True if src_data was added, otherwise False
        '''
        try:
            self.s3.put_object(Bucket=self.b_name,
                               Key=dest_key,
                               Body=object_data)
        except ClientError as e:
            # AllAccessDisabled error == bucket not found
            # NoSuchKey or InvalidRequest error
            # logging.error(e)
            return False
        return True

    def download_file(self, key, filepath):
        '''
        Download an object and save to the specified file.

        :param key: the key of an S3 object
        :param filepath: the destination Path object
        '''
        filepath.parent.mkdir(parents=True, exist_ok=True)
        self.s3.download_file(self.b_name, key, str(filepath))

    def download_files(self, keys, directory, cut_dirs=0):
        '''
        Download objects and save to the specified directory.

        :param keys: a list of keys
        :param directory: the destination directory to save files
        :param cut_dirs: specified the number of directories to be ommited
                         to from a key
        '''
        for key in keys:
            pk = Path(key)
            ndir = '/'.join(pk.parent.parts[cut_dirs:])
            p = Path(directory, ndir, pk.name)
            self.download_file(key, p)

    def upload_file(self, local_filepath, s3_key, extra_args=None):
        '''
        Upload a file to the S3 bucket with a specified s3 key.

        :param local_filepath: the source file (Path object)
        :param s3_key: the key of the destination S3 object
        '''
        self.s3.upload_file(str(local_filepath), self.b_name, s3_key,
                            ExtraArgs=extra_args)


    def upload_directory(self, local_dirpath, s3_prefix):
        '''
        Upload all files under a local directory
        to the S3 bucket with a specified s3 prefix.

        :param local_dirpath: the source directory (Path object)
        :param s3_prefix: the s3 prefix of the destination
        '''
        cmd = ['aws', 's3', 'sync', str(local_dirpath),
               's3://{}/{}/'.format(self.b_name, s3_prefix),
               '--sse']
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)

    def delete_keys(self, keys):
        '''
        Delete objects from an S3 bucket.

        :param keys: a list of keys
        '''
        objs = [{'Key': key} for key in keys]
        #
        # make sure only pass maximum 1000 objects to s3.delete_objects()
        #
        s_max = 1000
        s_start = 0
        while True:
            s_stop = s_start + s_max
            s_objs = objs[slice(s_start, s_stop)]
            if len(s_objs) == 0:
                break
            self.s3.delete_objects(
                Bucket=self.b_name,
                Delete={
                    'Objects': s_objs,
                    'Quiet': True
                },
            )
            s_start += s_max

    def is_newer(self, obj1, obj2):
        '''
        Return True if obj1 is newer than obj2

        :param obj1: an S3 object return by list_objects()
        :param obj2: an S3 object return by list_objects()
        '''
        return obj1['LastModified'] >= obj2['LastModified']
PK       ! �I��  �  4           ��    __pycache__/identify_instrument_files.cpython-36.pycPK       ! ��
L�  �             ��$  __pycache__/s3io.cpython-36.pycPK       ! ���<	  <	             ���  identify_instrument_files.pyPK       ! �$�R�  �             ��k%  s3io.pyPK      .  ?=    