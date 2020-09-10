# Zoom Auto Uploader
It's so annoying to always check your email to upload the latest lecture to Piazza for students right? This simple script will automate this for you! 

# How to Run
Go to [this](https://developers.google.com/gmail/api/quickstart/python?authuser=1) link to get your `credentials.json` file and place it in this folder. 

You need to run the script once locally to generate the `token.pickle` information needed.

Now you need to edit the Dockerfile to add your Piazza information. Change the `ENV` lines to your Piazza info. The `PIAZZA_CLASS_NETWORK_ID` can be found by checking the URL in Piazza. It will look something like this `https://piazza.com/class/PIAZZA_CLASS_NETWORK_ID` when you are viewing your class on the browser. 

Once you've created the token.pickle, you can run the following command:

    ```
    > docker build  -t zoomautouploader:latest .
    ```

(TODO: We could automate this in a script for non-tech savy people). 