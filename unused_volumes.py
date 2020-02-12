import boto3
from tabulate import tabulate

client = boto3.client('ec2', region_name='eu-west-1')

table=[]
volumes = client.describe_volumes( Filters=[{'Name': 'status', 'Values': ['available']}])

for volume in volumes['Volumes']:
    #print(volume['Size'])
    #print(volume['VolumeId'])
    #vol=volume['VolumeId']
    #print(volume['Iops'])
    #print(volume['VolumeType'])
    table.append(volume['VolumeId'])

    snapshots = client.describe_snapshots( Filters=[{'Name': 'volume-id', 'Values': [volume['VolumeId']]}])
    if not snapshots['Snapshots']:
        #table.append('None')
        snap='None'
    else:
        table.append(snapshots['Snapshots'][0]['SnapshotId'])
        snap=snapshots['Snapshots'][0]['SnapshotId'] 
        #print(snapshots['Snapshots'][0]['StartTime'])
        #print(type(snapshots['Snapshots']))


   # print(tabulate([[volume['VolumeId'],snap]], headers=['Volume','Snapshot']))

    if volume['VolumeType']=='io1':
        print('volume is io1')

print(tabulate([[table[0],table[1]], [table[2],table[3]]], headers=['Volume','Snapshot']))
