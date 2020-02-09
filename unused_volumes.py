import boto3

client = boto3.client('ec2')

volumes = client.describe_volumes( Filters=[{'Name': 'status', 'Values': ['available']}])

for volume in volumes['Volumes']:
    #print(volume['Size'])
    print(volume['VolumeId'])
    #print(volume['Iops'])
    #print(volume['VolumeType'])

    snapshots = client.describe_snapshots( Filters=[{'Name': 'volume-id', 'Values': [volume['VolumeId']]}])
    print(snapshots)

    if volume['VolumeType']=='io1':
        print('volume is io1')