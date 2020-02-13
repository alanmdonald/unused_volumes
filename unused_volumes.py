import boto3

client = boto3.client('ec2')

av_volumes=[]

for region in client.describe_regions()['Regions']:

    regions=region['RegionName']

    client = boto3.client('ec2', region_name=regions)
    volumes = client.describe_volumes( Filters=[{'Name': 'status', 'Values': ['available']}])
    
    if volumes['Volumes']:
        print ("\033[1m" + "\nRegion: " + regions)
    else:
        print ("\033[0m"+ "\nRegion: "+ regions + "\tNo volumes in available state")
    snap="None"
    start=""
    creation=""
    for volume in volumes['Volumes']:
        #print(volume['Size'])
        #print(volume['VolumeId'])
        #print(volume['Iops'])
        #print(volume['VolumeType'])

        av_volumes.append(volume['VolumeId'])
        av_volumes.append(regions)
        snapshots = client.describe_snapshots( Filters=[{'Name': 'volume-id', 'Values': [volume['VolumeId']]}])
        if snapshots['Snapshots']:
            snap=snapshots['Snapshots'][0]['SnapshotId'] 
            start=str(snapshots['Snapshots'][0]['StartTime'])
            creation="Creation:"

        print ("Volume:  " + volume['VolumeId'] + "\tSnapshot:  " + snap + "\t" + creation + " "  + start)

if av_volumes:
    print ("\nYou have "+str(len(av_volumes)) +" volumes in an available state")
    option=int(input("\nOptions \n\t[1] Delete volumes  \n\t[2] Take snapshot of volumes  \n\t[3] Take snapshot then delete  \n\t[4] Quit\n\n\t: "))
else:
    print("\nYou have no volumes in an available state")

if option == 1:
    for vol in av_volumes:
        print("Deleting: "+vol)
        #response = client.delete_volume(VolumeId=vol)
elif option == 2:
    for vol in av_volumes:
        print("Taking snapshot of: "+vol)
        response = client.create_snapshot(VolumeId=vol)
        print(response)
elif option == 3:
    for vol in av_volumes:
        print("Taking snapshot of: "+vol)
        #response = client.create_snapshot(VolumeId=vol)
    for vol in av_volumes:
        print("Deleting: "+vol)
        #response = client.delete_volume(VolumeId=vol)
else:
    print("Exiting")

