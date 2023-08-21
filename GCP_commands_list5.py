Configuring and Using Cloud Logging and Cloud Monitoring 

Task 1. Set up resources in your first project

In this task, you create the Google Cloud resources for the first project.

In the Qwiklabs Connection Details section, you will see two projects listed. The first project will contain active Google Cloud resources, which will generate logs and monitoring metric data.

The second project will contain your Monitoring account configuration data.

Make sure that you are working on project 1 for this task!

If you have not activated cloud shell yet then, activate the Cloud Shell by clicking on Activate cloud shell. If prompted, click Continue.

In the Cloud Shell, download and unpack an archive that contains setup code:

*curl https://storage.googleapis.com/cloud-training/gcpsec/labs/stackdriver-lab.tgz | tar -zxf -

*cd stackdriver-lab



Click on the Open Editor icon in the top-right corner of your Cloud Shell session.

Click Open in a new window if prompted.

Open the stackdriver-lab folder and select the linux_startup.sh file.

Replace the # install logging agent and # install monitoring agent sections with the following:

*# install logging agent
curl -sSO https://dl.google.com/cloudagents/add-logging-agent-repo.sh
sudo bash add-logging-agent-repo.sh --also-install
# install monitoring agent
curl -sSO https://dl.google.com/cloudagents/add-monitoring-agent-repo.sh
sudo bash add-monitoring-agent-repo.sh --also-install



After pasting, make sure that your lines of code are properly indented.

Save your file.

Now open the setup.sh file.

Update the image version in # create vms section for windows-server (row 17) after --image with the following:

*windows-server-2016-dc-core-v20210511



After pasting, make sure that your lines of code are properly indented.

Save your file.

In the Cloud Console, click Open Terminal in the top-right corner.

Now run the following command:

*./setup.sh

The created resources will include:

    Service accounts (for use by VMs).
    Role assignments (granting service accounts permissions to write to Monitoring).
    A Linux VM with Apache and the Monitoring agents installed.
    A Windows VM with the Monitoring and Logging agents installed.
    A Google Kubernetes Engine cluster with an Nginx deployment.
    A Pub/Sub Topic and Subscription.

    If you get a similar message to the following:

    *ERROR: (gcloud.compute.instances.create) Could not fetch resource:
    ---
    code: ZONE_RESOURCE_POOL_EXHAUSTED
    errorDetails:
    
Run the following command to replace the zones in the setup script with a new one:

*sed -i 's/us-west1-b/us-east4-a/g' setup.sh

You can safely ignore errors about service accounts and firewalls already existing.

    If you receive the same error, select another Google Cloud zone and run the following command, replacing <YOUR_ZONE> with your newly selected zone:

*sed -i 's/us-east4-a/<YOUR_ZONE>/g' setup.sh

Ensure you receive a similar output that states that both the Linux and Windows VMs are created:

output:
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-03-7c1d05517425/zones/us-central1-a/instances/linux-server-qwiklabs-gcp-03-7c1d05517425].
NAME: linux-server-qwiklabs-gcp-03-7c1d05517425
ZONE: us-central1-a
MACHINE_TYPE: n1-standard-1
PREEMPTIBLE:
INTERNAL_IP: 10.128.0.2
EXTERNAL_IP: 162.222.176.37
STATUS: RUNNING
Created [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-03-7c1d05517425/zones/us-central1-a/instances/windows-server-qwiklabs-gcp-03-7c1d05517425].
WARNING: Some requests generated warnings:
 - The resource 'projects/windows-cloud/global/images/windows-server-2016-dc-core-v20210511' is deprecated. A suggested replacement is 'projects/windows-cloud/global/images/windows-server-2016-dc-core-v20210608'.
......
......   
NAME: windows-server-qwiklabs-gcp-03-7c1d05517425
ZONE: us-central1-a
MACHINE_TYPE: n1-standard-1
PREEMPTIBLE:
INTERNAL_IP: 10.128.0.3
EXTERNAL_IP: 34.67.55.114
STATUS: RUNNING
Updated [https://www.googleapis.com/compute/v1/projects/qwiklabs-gcp-03-7c1d05517425/zones/us-central1-a/instances/linux-server-qwiklabs-gcp-03-7c1d05517425].

View and filter logs in first project

In this task, you view VM instance logs with simple filtering.
See which services are writing logs

    Ensure that you are on the Google Cloud Console homepage.

    Verify you are still working in project 1; the project ID in the Console's info panel should match GCP Project ID 1 in your lab's connection details panel.

    View Cloud Logging by opening Navigation menu > Logging > Logs Explorer. If prompted, close the notification.

    On the left-hand panel, Log fields will be visible. Under Resource Type, you will see several Google Cloud services that are creating logs.

All of these services are writing log entries. Entries from all these logs appear on the right, in the Query results pane. You can also query for results from specific logs, or that match specific criteria.

View VM instance logs with simple filtering

    In the Log fields panel, under Resource Type, click VM Instance.

After you click this:

    The contents of the Log fields panel changes. You will see a new field named INSTANCE ID. It shows all the instance IDs of the VM instances that are writing log entries.
    The Query box near the top of the page is populated with resource.type="gce_instance". This means that only entries from VM instances will be logged and displayed.
    The Query results pane also updates automatically—entries from VM Instances are the only logs displayed.

    In the Instance Id field, select one of the instance IDs. Logs for the associated VM instance appear in the Query results pane.

    Click inside the Query box. This now becomes editable.

    In the Query box, remove everything after line 1. You should see only line 1, which contains resource.type="gce_instance".

    Click Run query (located in the top-right corner). In the Query results, you should see entries from all VM instance logs.

    Note that the logs panel reverts to its previous state.

    Turn on streaming logs by clicking Stream logs (top-right corner, next to the "Run query" button).

    You should see new log entries showing up every 1-2 seconds as the background activity is generating unauthorized requests against your Web servers.

You will now view overall web activity on any Linux Apache server.

    Stop log streaming by clicking on Stop stream in the top-right corner.

    Switch to viewing just the Apache access logs by selecting the apache-access log name (located in the log fields panel, can be selected under "Log name" in the top-right corner). You will see entries that show requests to the Linux Apache server.

You will now learn how to view general system activity on a given Linux server.

    Click Log Name dropdown, and then click on the Clear button next to apache access.

    Now click on the Log Name dropdown, and select syslog, and then click Apply.

Entries from syslog appear in the Query results pane.

Use log exports

In this task, you configure and test log exports to BigQuery.

Cloud Logging retains log entries for 30 days. In most circumstances, you'll want to retain some log entries for an extended time (and possibly perform sophisticated reporting on the archived logs).

Google Cloud provides a mechanism to have all log entries ingested into Cloud Monitoring also written to one or more archival sinks.

Configure the export to BigQuery

    Go to Cloud Logging Exports (Navigation menu > Logging > Log Router).

    Click Create Sink.

    For the Sink name, type vm_logs and then click Next.

    For Select sink service, select BigQuery dataset.

    For Select BigQuery dataset, select Create new BigQuery dataset.

    For the Dataset ID, type project_logs, and click Create Dataset.

    Click Next.

    In the Build inclusion filter list box, type resource.type="gce_instance".

    Click Create Sink. You will now return to a Log Router Create log sink next steps page (a message at the top may appear that says "Your log sink was successfully created. Data should be available soon.")

**logs_export1.JPG

You will now create an export for the Cloud HTTP Load Balancing logs to BigQuery.

    From the left-hand navigation menu, select Log Router to return to the service homepage.

    Click Create Sink.

    For the Sink name, type load_bal_logs and then click Next.

    For Select sink service, select BigQuery dataset.

    For Select BigQuery dataset, select project_logs. (You created this BigQuery dataset in the previous set of steps.)

    Click Next.

    In the Build inclusion filter list box, type resource.type="http_load_balancer".

    Click Create Sink.

    You will now be on the Create log sink next steps page for the log sink.

    From the left-hand navigation menu, select Log Router to return to the service homepage.

The Log Router page appears, displaying a list of sinks (including the one you just created—load_bal_logs).

Investigate the exported log entries

    Open BigQuery (Navigation menu > BigQuery).

    The "Welcome to BigQuery in the Cloud Console" message box opens. This message box provides a link to the quickstart guide and lists UI updates.

    Click Done.

    In the left pane in the Explorer section, click your project (this starts with qwiklabs-gcp-xxx) and you should see a project_logs dataset under it.

You will now verify that the BigQuery dataset has appropriate permissions to allow the export writer to store log entries.

    Click on the three dotted menu item ("View actions") next to the project_logs dataset and click Open.

    Then from the top-right hand corner of the Console, click the Sharing dropdown and select Permissions.

    On the Dataset permission page, you will see that your service accounts have the "BigQuery Data Editor" role.

    Close the dataset permissions panel.

    Expand the project_logs dataset to see the tables with your exported logs—you should see multiple tables (one for each type of log that's receiving entries).

    Click on the syslog_(1) table, then click Details to see the number of rows and other metadata. If the syslog_(1) table is not visible, try refreshing the browser.

    In Details tab, under the table info you will see the full table name in the Table ID, copy this table name.

You can run all sorts of queries to analyze your archived log entries. For example, to see a subset of your tables fields, paste the below query in the query Editor tab (replacing qwiklabs-gcp-xx-xxxxxxxxxxx.project_logs.syslog_xxxxxxxx with the table name you copied in the previous step).

*SELECT
  logName, resource.type, resource.labels.zone, resource.labels.project_id,
FROM
  `qwiklabs-gcp-xx-xxxxxxxxxxx.project_logs.syslog_xxxxxxxx`
  
  
    Then click Run.

Feel free to experiment with some other queries that might provide interesting insights.

**logs_export2.JPG

Create a logging metric

In this task, you create a metric that you can use to generate alerts if too many web requests generate access denied log entries.

Cloud Monitoring allows you to create custom metrics based on the arrival of specific log entries.

    Go back to the Logs Explorer page (Navigation menu > Logging > Logs Explorer).




    Select Create Metric (right-hand side of the Console) to create a logging metric based on this filter.

    In the Log-based metric Editor, set Metric Type as Counter.

    Under the Details section, set the Log metric name to 403s.

    Under the Filter selection for Build filter, enter the following and replace PROJECT_ID with GCP Project ID 1:

*resource.type="gce_instance"
log_name="projects/PROJECT_ID/logs/syslog"


    Leave all the other fields at their default.

    Click Create Metric.

    You will make use of this metric in the dashboarding portion of the lab.

Create a monitoring dashboard

In this task, you switch to the second project created by Qwiklabs and setup a Monitoring workspace.
Switch projects

    Switch to the second project created by Qwiklabs (use the GCP Project ID 2 from the Qwiklabs Connection Details). The current project ID is displayed at the top of the console.

**logs_export3.jpg



    Click the second project you want to switch to. Verify it is the GCP Project ID 2 from the Qwiklabs Connection Details.

    Click Open.


Create a Monitoring workspace

You will now setup a Monitoring workspace that's tied to your Google Cloud Project. The following steps create a new account that has a free trial of Monitoring.

    In the Cloud Console, click on Navigation menu > Monitoring.

    Wait for your workspace to be provisioned.

When the Monitoring dashboard opens, your workspace is ready.

Now add the first project to your Cloud Monitoring workspace.

    In the left menu, click Settings and then click + Add GCP Projects in the GCP Projects section.

    You'll see one of the projects for this lab as a monitored account. Check the box next to the other project you have, then for the scoping project select Use this project as the scoping project and click Add Projects.

    Click Confirm.

Create a monitoring dashboard

    In the left pane, click Dashboards.

    Click + Create Dashboard.

    Replace the generic dashboard name at the top with Example Dashboard.

    Click Line.

    For Chart Title, give your chart a name of CPU Usage.

    For Resource & Metric, select VM Instance > Instance > CPU usage. Make sure it's the one that follows the format: compute.googleapis.com/instance/cpu/usage_time. Click Apply.




    Click Add Chart.

    Click Line.

    Name the chart Memory Utilization and set the Resource & Metric to VM Instance > Memory > Memory Utilization. Make sure it's the one that follows the format: agent.googleapis.com/memory/percent_used.

    Click Apply.

    Click the Enable auto-refresh button in the top-right corner (next to "Edit Dashboard") to receive real-time graph results.

When it's done loading, you should see your two graphs—one for CPU usage and the other for memory utilization—populated.

You can now explore some other options by editing the charts such as Filter, Group By, and Aggregation.