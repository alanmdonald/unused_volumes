# Unused Volumes

### Description:
Save money by identifying EBS volumes that are not in use. Take a snapshot of these volumes and/or delete them. 

### Background:
When deleting an EC2 instance there are 2 options for the EBS volumes attached. The option DeleteOnTermination can be set to true or false [1]. By default, the DeletionOnTermination attribute for the root volume of an instance is set to true [1] and for non root volumes is set to false. As the name suggests, this attribute determined whether or not a volume is deleted when an instance is terminated. 

The attribute can be altered using the modify-instance-attribute API [2]. 

A common scenario occurs when customers terminate instances and have volumes with DeleteOnTermination set to false. In this case the volumes persist. Unlike an instance (which doesn't incurr a cost when it is stopped) volumes that are not in use (in an "available" state) are still incuring the same cost as if they were attached to an instance. This is beacuse with EBS volumes you pay for the provisioned space and/or IOPS. Even if the volume is not in use the space/IOPS is still provisioned for you and therefor charged. 

A volume in an "available" state is one that is provisioned and incuring cost but is not attached to an EC2 instance. 

To help users prevent these costs I have written a short python script.

### Setup:
You will need to have python and boto3 installed. You will also need to have your AWS credientials correctly configured with the appriopriate permissions.  

Running the script will;

Check for all volumes in an available state in every region. 
If there are none the script will exit. 
If there are volumes they will be printed to the screen given the volume id, region, wheter or not the volume has a snapshot and if so the date of the latest snapshot. 

Once listed you will be given 4 options. 

	[1] Delete volumes  
	[2] Take snapshot of volumes  
	[3] Take snapshot then delete  
	[4] Quit

Option 1 will delete all of the available volumes that have been found. You will be asked to confirm this selection.

Option 2 will snapshot all of the available volumes that have been found. 

Option 3 will snapshot all of the available volumes that have been found and then delete them. You will be asked to confirm this selection. 

Option 4 will quit the script.

You re run the script in order to confirm the new snapsnot or that the volumes have been deleted. 


[1] https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#preserving-volumes-on-termination

[2] https://docs.aws.amazon.com/cli/latest/reference/ec2/modify-instance-attribute.html
