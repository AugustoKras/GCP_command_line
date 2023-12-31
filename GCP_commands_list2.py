Verify that the load balancer is deployed and registered by executing the following command:
*gcloud compute backend-services get-health web-backend --global

Retrieve the load balancer IP address by executing the following command:
*gcloud compute forwarding-rules describe web-rule --global

Copy the value for the IPAddress property, later it will be used as [IP_ADDRESS_OF_LOAD_BAL].
35.227.194.130
*while true; do curl -m1 [IP_ADDRESS_OF_LOAD_BAL]; done
*while true; do curl -m1 35.227.194.130; done

The responses will alternate randomly among the instances.

    Press CTRL+C to stop the previous command.

Click Create Instance
Once launched, click the SSH button to connect to the instance.
curl -m1 [IP_ADDRESS_OF_LOAD_BAL]
curl -m1 35.227.194.130

output must be like that
<!doctype html><html><body><h1>Web server</h1><h2>This server is in zone: projects/104716457480/zones/us-central1-f</h2> </body></html>

Verify the security policy

    Return to the SSH session of the access-test VM.
    Run the curl command again on the instance to access the load balancer:

*curl -m1 [IP_ADDRESS_OF_LOAD_BAL]
*curl -m1 35.227.194.130

output must be like that
<!doctype html><meta charset="utf-8"><meta name=viewport content="width=device-width, initial-scale=1"><title>404</title>404 Not Found


View Google Cloud Armor logs
*In the Console, navigate to Navigation menu > Network Security > Cloud Armor
Click blocklist-access-test.
Click Logs.
Click View policy logs and go to the latest logs. If prompted, close the notification.
Locate a log with a 404 and expand the log entry.
Expand httpRequest.
The request should be from the access-test VM IP address.
Explore some of the other log entries.
