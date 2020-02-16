import boto3
import time

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
        av_volumes.append([volume['VolumeId'], regions])
        
        snapshots = client.describe_snapshots( Filters=[{'Name': 'volume-id', 'Values': [volume['VolumeId']]}])
        
        if snapshots['Snapshots']:
            snap=snapshots['Snapshots'][0]['SnapshotId'] 
            start=str(snapshots['Snapshots'][0]['StartTime'])
            creation="Creation:"

        print ("Volume:  " + volume['VolumeId'] + "\tSnapshot:  " + snap + "\t" + creation + " "  + start)

def deleteVolumes(av_volumes):
    for av in av_volumes:
        client = boto3.client('ec2', region_name=av[1])
        response = client.delete_volume(VolumeId=av[0])
        print("Volume "+av[0]+ " deleted") 

def snapshotVolumes(av_volumes):
    for av in av_volumes:
        client = boto3.client('ec2', region_name=av[1])
        response = client.create_snapshot(VolumeId=av[0])
        print("Taking snapshot " + response['SnapshotId'] + " of volume "+ av[0]+" in "+av[1] )
    print("\nSnapshots of all volumes in an available state complete")

if av_volumes:
    print ("\nYou have "+str(len(av_volumes)) +" volumes in an available state")
    option=int(input("\nOptions \n\t[1] Delete volumes  \n\t[2] Take snapshot of volumes  \n\t[3] Take snapshot then delete  \n\t[4] Quit\n\n\t: "))
else:
    print("\nYou have no volumes in an available state")
    print("\nExiting")
    exit()

if option == 1:
    deleteVolumes(av_volumes)
elif option == 2:
    snaps=snapshotVolumes(av_volumes)
elif option == 3:
    snapshotVolumes(av_volumes)
    print("Deleting volumes\n")
    deleteVolumes(av_volumes)
else:
    print("\nExiting")
    exit()



