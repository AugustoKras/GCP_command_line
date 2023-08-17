Redacting Sensitive Data with the DLP API 

Enable the DLP API
Go to Navigation menu > APIs & Services.

Click the Enable APIs and Services button.

In the Search for APIs & Services field, enter DLP and then click on the Cloud Data Loss Prevention (DLP) API title.

Click the Enable button to enable the DLP API. If the API is already enabled, you will see a Manage button instead, along with an API enabled message. In that case you do not need to do anything.

Install the DLP API and Node JS samples

On the Google Cloud Console tile bar, click Activate Cloud Shell (Activate Cloud Shell icon) to open Cloud Shell. When prompted, click Continue. After a moment, in the lower part of the browser window, the Terminal appears.

Run the following command to create the GCLOUD_PROJECT environment variable and set it to the project ID:
*export GCLOUD_PROJECT=$DEVSHELL_PROJECT_ID

Run the following command in Cloud Shell to download the Node JS DLP API and samples

*git clone https://github.com/GoogleCloudPlatform/nodejs-docs-samples

Once the download is complete, change into the nodejs-docs-samples/dlp directory
*cd nodejs-docs-samples/dlp

There are several Node JS DLP sample programs in this folder. Before you run them, you need to install the dependencies.

    Run the following command to install the required dependencies:
*npm install @google-cloud/dlp
*npm install yargs
*npm install mime

Inspect and redact sensitive data
In this task, you inspect and mask sensitive information from the string also use the DLP API to redact sensitive data from an image.

*node inspectString.js $GCLOUD_PROJECT "My email address is joe@example.com."

output
Findings:
        Info type: EMAIL_ADDRESS
        Likelihood: LIKELY
        
The result shows what sensitive data was found, what type of information it is, and how certain the API is about that info type.

    In Cloud Shell, run the following command:
*node inspectString.js $GCLOUD_PROJECT "My phone number is 555-555-5555."

You should receive the following output.

Output:
Findings:
        Info type: PHONE_NUMBER
        Likelihood: VERY_LIKELY
        
Feel free to experiment with different input to the inspectString.js program. For example, try passing in values like 1234-5678-9876-5432 or 123-45-6789.

You should receive the following output.
output
My phone number is ************.

Redact sensitive data from images

You will now use the DLP API to redact sensitive data from an image.

    Right-click on the image below and select Save image as. Save it locally on your computer as dlp-input.png.

**DLP_image1.png 

In the bar above the terminal, click the button at the top right with three vertical dots and select Upload.

If Upload is not clickable ("grayed out"), then click Restart. After the Cloud Shell environment is restarted, the Upload Link should be active.

Execute these commands commands before starting the next step in the lab.

*export GCLOUD_PROJECT=$DEVSHELL_PROJECT_ID



Click Choose Files, select the downloaded dlp-input.png image file, and Upload it to Cloud Shell.

From Cloud Shell, click Open Editor . This will launch the Cloud Shell code editor, which includes a file browser.

In the Cloud Shell code editor, on the left, you should see the dlp-input.png file.

Click the dlp-input.png file to display the image and verify it was uploaded.

From Cloud Shell, click Open Terminal to return to the terminal window.

In the terminal, run the following command to redact the email address values from the image:

*node redactImage.js $GCLOUD_PROJECT ~/dlp-input.png "" EMAIL_ADDRESS ~/dlp-redacted.png



Open Editor.

In the Cloud Shell code editor, on the left, click the dlp-redacted.png file.

You will see the image with the domain name redacted.

**DLP_image2.png

When calling the redact API, you specified EMAIL_ADDRESS as the infotype to redact. In the image, you should notice that the email address is no longer visible.
