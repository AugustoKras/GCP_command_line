
Cloud DNS - Traffic Steering using Geolocation Policy 

You can list the active account name with this command:
*gcloud auth list

You can list the project ID with this command:
*gcloud config list project

Enable Compute Engine API
*gcloud services enable compute.googleapis.com

Enable Cloud DNS API
*gcloud services enable dns.googleapis.com

Verify that the APIs are enabled
*gcloud services list | grep -E 'compute|dns'

Configure the firewall
To be able to SSH into the client VMs, run the following to create a firewall rule to allow SSH traffic from Identity Aware Proxies (IAP):

*gcloud compute firewall-rules create fw-default-iapproxy \
--direction=INGRESS \
--priority=1000 \
--network=default \
--action=ALLOW \
--rules=tcp:22,icmp \
--source-ranges=35.235.240.0/20

To allow HTTP traffic on the web servers, each web server will have a "http-server" tag associated with it. You will use this tag to apply the firewall rule only to your web servers:

*gcloud compute firewall-rules create allow-http-traffic --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0 --target-tags=http-server

Launch client VMs
Run the gcloud compute instances create command to create the client VMs:
*gcloud compute instances create us-client-vm --machine-type=e2-micro --zone us-east4-b

Launch a client in Europe
*gcloud compute instances create europe-client-vm --machine-type=e2-micro --zone "europe-central2-a"

Launch a client in Asia
*gcloud compute instances create asia-client-vm --machine-type=e2-micro --zone asia-south1-a
observation
If you receive an error indicating resources are not available in the asia-south1-a zone, then you will try to create the VM in a different zone in Asia. First, run this command to see all of the zones in Asia.
*gcloud compute zones list | grep -iE 'NAME.*asia' | sed 's/NAME: //i' | sort

Select a zone (other than asia-south1-a) from the list of regions returned by the list command - and try to create a VM within that zone. In other words, in the command below, replace <SELECTED-ZONE> with another zone in Asia.
*gcloud compute instances create asia-client-vm --machine-type=e2-micro --zone <SELECTED-ZONE>


Launch Server VMs
*gcloud compute instances create us-web-vm \
--machine-type=e2-micro \
--zone us-east4-b \
--network=default \
--subnet=default \
--tags=http-server \
--metadata=startup-script='#! /bin/bash
 apt-get update
 apt-get install apache2 -y
 echo "Page served from: us-east4" | \
 tee /var/www/html/index.html
 systemctl restart apache2'


Create Cloud DNS Routing Policy
*gcloud dns record-sets create geo.example.com \
--ttl=5 --type=A --zone=example \
--routing-policy-type=GEO \
--routing-policy-data="us-east4=$US_WEB_IP;europe-central2=$EUROPE_WEB_IP"

Verify

    Use the dns record-sets list command to verify that the geo.example.com DNS record is configured as expected:

*gcloud dns record-sets list --zone=example
