Configuring and Viewing Cloud Audit Logs 

Reference video
https://www.youtube.com/watch?v=fCWLEmNznOA


Check project permissions

Before you begin your work on Google Cloud, you need to ensure that your project has the correct permissions within Identity and Access Management (IAM).

In the Google Cloud console, on the Navigation menu (Navigation menu icon), select IAM & Admin > IAM.

Confirm that the default compute Service Account {project-number}-compute@developer.gserviceaccount.com is present and has the editor role assigned. The account prefix is the project number, which you can find on Navigation menu > Cloud overview > Dashboard.


In the Google Cloud console, on the Navigation menu, click Cloud overview > Dashboard.

Copy the project number (e.g. 729328892908).

On the Navigation menu, select IAM & Admin > IAM.

At the top of the IAM page, click + Grant Access.
For New principals, type:

*{project-number}-compute@developer.gserviceaccount.com
{896819071792}-compute@developer.gserviceaccount.com
896819071792-compute@developer.gserviceaccount.com

Replace {project-number} with your project number.
For Select a role, select Project (or Basic) > Editor.
Click Save.

Enable data access audit logs

In this task, you enable data access audit logs.

Data access audit logs (except for BigQuery) are disabled by default, so you must first enable all audit logs. Logging charges for the volume of log data that exceeds the free monthly logs allotment.

All logs received by Logging count towards the logs allotment limit, except for the Cloud Audit Logs that are enabled by default. This includes all Google Cloud Admin Activity audit logs, System Event logs, plus data access audit logs from BigQuery only.

If you have not activated cloud shell yet then, on the Google Cloud Console title bar, click Activate Cloud Shell (Activate Cloud Shell icon). If prompted, click Continue.

At the command prompt, run this command to retrieve the current IAM policy for your project and save it as policy.json:

*gcloud projects get-iam-policy $DEVSHELL_PROJECT_ID \
--format=json >./policy.json


Click the Open Editor button to view the Cloud Shell code editor.

If an error indicates that the code editor could not be loaded because third-party cookies are disabled, click Open in New Window and switch to the new tab.

In the Cloud Shell code editor, click the policy.json file to expose its contents.

Add the following text to the policy.json file to enable data Access audit logs for all services. This text should be added just after the first { and before "bindings": [. (Be careful not to change anything else in the file).

*   "auditConfigs": [
      {
         "service": "allServices",
         "auditLogConfigs": [
            { "logType": "ADMIN_READ" },
            { "logType": "DATA_READ"  },
            { "logType": "DATA_WRITE" }
         ]
      }
   ],
   
before "bindings"


Click the Open Terminal button to return to the Cloud Shell command line.
At the command line, run the following command to set the IAM policy:

*gcloud projects set-iam-policy $DEVSHELL_PROJECT_ID \
./policy.json

The command will return and display the new IAM policy.

Generate some account activity

In this task, you create resources that generate log activty that you can view in Cloud Audit logs.

In Cloud Shell, run the following commands to create a few resources. This will generate some activity that you will view in the audit logs:

*gsutil mb gs://$DEVSHELL_PROJECT_ID
echo "this is a sample file" > sample.txt
gsutil cp sample.txt gs://$DEVSHELL_PROJECT_ID
gcloud compute networks create mynetwork --subnet-mode=auto
gcloud compute instances create default-us-vm \
--machine-type=e2-micro \
--zone=us-east4-a --network=mynetwork

*gsutil rm -r gs://$DEVSHELL_PROJECT_ID


View the Admin Activity logs

In this task, you view the Admin Activity logs.

Admin Activity logs contain log entries for API calls or other administrative actions that modify the configuration or metadata of resources. For example, the logs record when VM instances and App Engine applications are created and when permissions are changed.

To view the logs, you must have the Cloud Identity and Access Management roles Logging/Logs Viewer or Project/Viewer.

Admin Activity logs are always enabled so there is no need to enable them. There is no charge for your Admin Activity audit logs.

Use the Cloud Logging page

From the Cloud Console, select Navigation menu > Logging > Logs Explorer.

Paste the following in the Query builder field and replace [PROJECT_ID] with your project ID. You can copy the PROJECT_ID from the Qwiklabs Connection Details.

*logName = ("projects/[PROJECT_ID]/logs/cloudaudit.googleapis.com%2Factivity")

*OMG for me it´s hard to find Logs_queries1.jpg indicated with the red arrows



Click the Run Query button.

Locate the log entry indicating that a Cloud Storage bucket was deleted. This entry will refer to storage.googleapis.com, which calls the storage.buckets.delete method to delete a bucket. The bucket name is the same name as your project id.

Within that entry, click on the storage.googleapis.com text and select Show matching entries.

Notice a line was added to the query preview textbox (located where the query builder had been) to show only storage events.

*logName = ("projects/qwiklabs-gcp-xxxxxxxxx/logs/cloudaudit.googleapis.com%2Factivity")
protoPayload.serviceName="storage.googleapis.com"

You should now see only the cloud storage entries.

Within that entry, click on the storage.buckets.delete text and select Show matching entries.

Notice another line was added to the Query preview textbox and now you can only see storage delete entries.

This technique can be used to easily locate desired events.

In the Query results, expand the Cloud Storage delete entry and then expand the protoPayload field.

Expand the authenticationInfo field and notice you can see the email address of the user that performed this action.

Feel free to explore other fields in the entry.

Use the Cloud SDK

Log entries can also be read using the Cloud SDK command:

Example output:
gcloud logging read [FILTER]

In the Cloud Shell pane, use this command to retrieve only the audit activity for storage bucket deletion:

*gcloud logging read \
"logName=projects/$DEVSHELL_PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity \
AND protoPayload.serviceName=storage.googleapis.com \
AND protoPayload.methodName=storage.buckets.delete"

Export the audit logs

In this task, you export audit logs. Individual audit log entries are kept for a specified length of time and are then deleted. The Cloud Logging Quota Policy explains how long log entries are retained. You cannot otherwise delete or modify audit logs or their entries.

Audit log type 	Retention period
Admin Activity 	400 days
Data Access 	30 days

For longer retention, you can export audit log entries like any other Cloud Logging log entries and keep them for as long as you wish.

Export audit logs

When exporting logs, the current filter will be applied to what is exported.

In Logs Explorer, enter a query string in the Query builder to display all the audit logs. (This can be done by deleting all lines in the filter except the first one.) Your filter will look like what is shown below. (Note that your project ID will be different.)

*logName = ("projects/[PROJECT_ID]/logs/cloudaudit.googleapis.com%2Factivity")


Click the Run Query button.

Click on More actions > Create Sink button.

For the Sink Name name, enter AuditLogsExport and click Next.

For the Sink service, enter BigQuery dataset.

Click Select BigQuery dataset and then select Create new BigQuery dataset.

For the Dataset ID, enter auditlogs_dataset and click Create Dataset.

Uncheck the Use Partitioned Tables checkbox, if it is already selected, and click Next.

In the Build inclusion filter list box, make sure that this filter text is entered logName = 
("projects/[PROJECT_ID]/logs/cloudaudit.googleapis.com%2Factivity").

Click the Create Sink button. The Logs Router Sinks page appears. Now, click on Logs Router.

On this page, you should be able to see the AuditLogsExport sink.

To the right of the AuditLogsExport sink, click the button with three dots (More icon) and select View sink details.

This will show information about the sink that you created.

Click Cancel when done.

In Cloud Shell, run the following commands to generate some more activity that you will view in the audit logs exported to BigQuery:

*gsutil mb gs://$DEVSHELL_PROJECT_ID
gsutil mb gs://$DEVSHELL_PROJECT_ID-test
echo "this is another sample file" > sample2.txt
gsutil cp sample.txt gs://$DEVSHELL_PROJECT_ID-test
gcloud compute instances delete --zone=us-east4-a \
--delete-disks=all default-us-vm

When prompted, enter y.
*gsutil rm -r gs://$DEVSHELL_PROJECT_ID
gsutil rm -r gs://$DEVSHELL_PROJECT_ID-test


Use BigQuery to analyze logs

In this task, you export logs to a BigQuery dataset. You then analyze the logs using Query editor.



Go to Navigation menu > BigQuery. If prompted, log in with the Qwiklabs-provided credentials.

The Welcome to BigQuery in the Cloud Console message box opens. This message box provides a link to the quickstart guide and lists UI updates.

Click Done.

In the left pane, under the Explorer section, click your project. This starts with (qwiklabs-gcp-xxx). You should see an auditlogs_dataset dataset under it.

Verify that the BigQuery dataset has appropriate permissions to allow the export writer to store log entries. Click on the auditlogs_dataset dataset.

From the Sharing dropdown, select Permissions.

On the Dataset Permission page, you will see the service account listed as BigQuery Data Editor member. If it's not already listed, you can add a service account under Add Principal and grant it the data editor role.


Click the Close button to close the Share Dataset screen.

Expand the dataset to see the table with your exported logs. (Click on the expand icon to expand the dataset.)

Click on the table name and take a moment to review the schemas and details of the tables that are being used.
Click the Query > In new tab button.

In Cloud Shell, run the following commands again to generate some more activity that you will view in the audit logs exported to BigQuery:

*gcloud compute instances create default-us-vm \
--zone=us-east4-a --network=mynetwork

*gcloud compute instances delete --zone=us-east4-a \
--delete-disks=all default-us-vm

When prompted, enter y.
*gsutil mb gs://$DEVSHELL_PROJECT_ID
gsutil mb gs://$DEVSHELL_PROJECT_ID-test
gsutil rm -r gs://$DEVSHELL_PROJECT_ID
gsutil rm -r gs://$DEVSHELL_PROJECT_ID-test

Delete the text provided in the Query editor window and paste in the query below. This query will return the users that deleted virtual machines in the last 7 days.
*#standardSQL
SELECT
  timestamp,
  resource.labels.instance_id,
  protopayload_auditlog.authenticationInfo.principalEmail,
  protopayload_auditlog.resourceName,
  protopayload_auditlog.methodName
FROM
`auditlogs_dataset.cloudaudit_googleapis_com_activity_*`
WHERE
  PARSE_DATE('%Y%m%d', _TABLE_SUFFIX) BETWEEN
  DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND
  CURRENT_DATE()
  AND resource.type = "gce_instance"
  AND operation.first IS TRUE
  AND protopayload_auditlog.methodName = "v1.compute.instances.delete"
ORDER BY
  timestamp,
  resource.labels.instance_id
LIMIT
  1000
  

Click the Run button. After a couple of seconds you will see each time someone deleted a virtual machine within the past 7 days. You should see two entries, which is the activity you generated in this lab. Remember, BigQuery is only showing activity since the export was created.

Delete the text in the Query_editor window and paste in the query below. This query will return the users that deleted storage buckets in the last 7 days.

*#standardSQL
SELECT
  timestamp,
  resource.labels.bucket_name,
  protopayload_auditlog.authenticationInfo.principalEmail,
  protopayload_auditlog.resourceName,
  protopayload_auditlog.methodName
FROM
`auditlogs_dataset.cloudaudit_googleapis_com_activity_*`
WHERE
  PARSE_DATE('%Y%m%d', _TABLE_SUFFIX) BETWEEN
  DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND
  CURRENT_DATE()
  AND resource.type = "gcs_bucket"
  AND protopayload_auditlog.methodName = "storage.buckets.delete"
ORDER BY
  timestamp,
  resource.labels.instance_id
LIMIT
  1000
  
Click the Run button. After a couple seconds you will see entries showing each time someone deleted a storage bucket within the past 7 days.