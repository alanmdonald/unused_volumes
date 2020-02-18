import boto3
import random

#Initiate boto3
client = boto3.client('ec2')

#Create array to hold all volumes in an available state
av_volumes=[]

#Loop through regions
for region in client.describe_regions()['Regions']:
    
    regions=region['RegionName']
    
    #Initiate boto3 fro each region
    client = boto3.client('ec2', region_name=regions)
    
    #Describe volumes that are in an available state
    volumes = client.describe_volumes( Filters=[{'Name': 'status', 'Values': ['available']}])

    if volumes['Volumes']:
        #If there are volumes in an available state set font to bold and print region
        print ("\033[1m" + "\nRegion: " + regions)
    else:
        #If there are no volumes in an available state print region that
        print ("\033[0m"+ "\nRegion: "+ regions + "\tNo volumes in available state")
    
    #Loop through volumes in an available state
    for volume in volumes['Volumes']:

        #Add volume and its region to av_volumes array
        av_volumes.append([volume['VolumeId'], regions])
        
        #Get the snapshots of this volume
        snapshots = client.describe_snapshots( Filters=[{'Name': 'volume-id', 'Values': [volume['VolumeId']]}])
        

        if snapshots['Snapshots']:
            #If there are snapshot print the snapshot id and latest creation date 
            snap=snapshots['Snapshots'][0]['SnapshotId'] 
            start=str(snapshots['Snapshots'][0]['StartTime'])
            creation="Creation:"
        else:
            #If there are no snapshots print just None
            snap="None"
            start=""
            creation=""

        print ("Volume:  " + volume['VolumeId'] + "\tSnapshot:  " + snap + "\t" + creation + " "  + start)

def deleteVolumes(av_volumes):
    #Loop through all volumes with regions in av_volumes and delete them
    for av in av_volumes:
        client = boto3.client('ec2', region_name=av[1])
        response = client.delete_volume(VolumeId=av[0])
        print("\nVolume "+av[0]+ " deleted") 

def snapshotVolumes(av_volumes):
    #Loop through all volumes with regions in av_volumes and take a snapshot of them
    for av in av_volumes:
        client = boto3.client('ec2', region_name=av[1])
        response = client.create_snapshot(VolumeId=av[0],Description='Created by alanmdonald/unused_volumes', TagSpecifications=[{'ResourceType':'snapshot', 'Tags': [{'Key': 'CreatedBy','Value': 'alanmdonald/unused_volumes'}]}])
        print("Taking snapshot " + response['SnapshotId'] + " of volume "+ av[0]+" in "+av[1] )
    print("\nSnapshots of all volumes in an available state complete")

def confirmDelete(av_volumes):
    #Safety question to eunsure volume deletion is not a mistake
    print("\nAre you sure that you want to delete the following volumes that are in an available state? \n")
    for av in av_volumes:
        print (av[0])

    #Create random number
    checksum=random.randint(100, 999)
    confirm=int(input("\n To confirm deletion please enter this randomly generated number "+ str(checksum)+ " :"))
    if confirm == checksum:
        return
    else:
        print("\nIncorrect number "+str(confirm)+" is not equal to "+str(checksum)+". Exiting\n")
        exit()

if av_volumes:
    #Options of what to do with volumes
    print ("\nYou have "+str(len(av_volumes)) +" volumes in an available state")
    option=int(input("\nOptions \n\t[1] Delete volumes  \n\t[2] Take snapshot of volumes  \n\t[3] Take snapshot then delete  \n\t[4] Quit\n\n\t: "))
else:
    #Exit if no volumes
    print("\nYou have no volumes in an available state")
    print("\nExiting")
    exit()

#Invoke options based on selection
if option == 1:
    confirmDelete(av_volumes)
    deleteVolumes(av_volumes)
elif option == 2:
    snapshotVolumes(av_volumes)
elif option == 3:
    snapshotVolumes(av_volumes)
    print("\nMoving to delete volumes\n")
    confirmDelete(av_volumes)
    deleteVolumes(av_volumes)
else:
    print("\nExiting\n")
    exit()
