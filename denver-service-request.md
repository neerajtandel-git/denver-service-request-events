Denver Service Request Events

**The Project**

**Preface**

For test delivery, the data set here is relatively small (data from
Denver\'s open data catalog (https://www.denvergov.org/opendata)). You
should approach this test as though the data were 1000x the actual size
and frequently updated by real-time events.

**Approach**

There might be multiple ways to approach this challenge but the approach
which is being used here is AWS Cloud by building out the core of system
with components like EC2, Kinesis Data Firehose, S3, Glue, Athena,
Redshift, Quicksight, Kinesis Data Streams, Lambda, DynamoDB.

**Data Pipeline**

![Diagram Description automatically
generated](media/image1.png){width="6.56718394575678in"
height="4.329114173228346in"}

**The Data Flow:**

-   Kinesis Data Firehose -- To capture data from events being generated
    on Amazon EC2 instance which will be monitored by Kinesis Agent.

-   S3 -- Publish the events coming from Kinesis Data Firehouse into a
    data lake house in S3 which can be used in many different ways

-   AWS Glue -- To infer a schema from the data lake in S3 which houses
    all the data. Glue Crawler will scan the data seating there in S3
    and will populate the Glue Data Catalog.

-   Amazon Athena -- Issue queries against that data from Athena as if
    it were a SQL Database.

-   Amazon Redshift -- For building out Data Warehousing, have used
    Redshift Spectrum here to access the data in S3. The advantage is if
    we had other tables that were loaded in Redshift, we can join that
    data with S3 data as well.

-   Amazon Quicksight -- Building out Data Visualization, spin up the
    Amazon Quicksight to visualize the data coming from Redshift which
    in turn is looking at the data in S3.

-   Kinesis Data Streams -- Capture the events which gets generated on
    Amazon EC2 instance.

-   AWS Lambda -- Publish the data coming from Kinesis Data Streams to
    AWS Lambda Function.

-   DynamoDB -- The Lambda function which gets invoked will turn around
    and populate the data into DynamoDB if needed in future client app
    can read from.

**Kinesis Data Firehose**

![Graphical user interface, text, application, email Description
automatically generated](media/image2.png){width="4.987341426071741in"
height="3.725054680664917in"}

**EC2 Instance**

![Graphical user interface, application Description automatically
generated](media/image3.png){width="6.5in"
height="0.8861111111111111in"}

**Kinesis Agent**

![Text Description automatically
generated](media/image4.png){width="6.5in"
height="1.5284722222222222in"}

**EventGenerator.py** -- Generate the events (from the csv file) into
the /var/log/ directory of the instance

Generate the events into /var/log/ directory which will be monitored by
Kinesis Agent.

![Text Description automatically
generated](media/image5.png){width="5.607595144356956in"
height="3.5862248468941385in"}

**agent.json** -- Configuration file for the Kinesis Agent

![Text Description automatically
generated](media/image6.png){width="6.113923884514436in"
height="2.879945319335083in"}

Start the Kinesis Agent

![Text Description automatically
generated](media/image7.png){width="6.5in"
height="1.1493055555555556in"}

Generate the number of events

![Text Description automatically
generated](media/image8.png){width="6.5in"
height="1.1493055555555556in"}

Events generated in /var/log/ directory which Kinesis Agent monitors and
send it to Kinesis Data Firehose and Kinesis Data Streams.

![Text Description automatically generated with low
confidence](media/image9.png){width="6.964075896762905in"
height="1.6075951443569554in"}

**S3 Data Lake**

![Graphical user interface, application Description automatically
generated](media/image10.png){width="6.5in" height="1.4875in"}

![Graphical user interface, application, table Description automatically
generated](media/image11.png){width="6.5in"
height="2.3027777777777776in"}

**Kinesis Data Streams**

![Graphical user interface, application, Teams Description automatically
generated](media/image12.png){width="6.5in"
height="2.1277777777777778in"}

agent.json -- Add the new flow here which will push the data to Kinesis
Data Stream and tell the client to convert the CSV data into JSON format

![Text Description automatically
generated](media/image13.png){width="3.9873414260717412in"
height="6.631923665791776in"}

Generate the events, Kinesis Agent will monitor the events and send the
data to both the flows (Kinesis Data Firehose and Kinesis Data Streams)

![Text Description automatically
generated](media/image14.png){width="6.5in"
height="0.8638888888888889in"}

**AWS Lambda** function (lambda_function.py) running in a serverless
environment that can scale itself up indefinitely and as needed will
consume data from Kinesis Data Stream and write it out to DynamoDB.

![Graphical user interface, application Description automatically
generated](media/image15.png){width="6.5in"
height="2.191666666666667in"}

**DynamoDB**

![Graphical user interface, text, application, email Description
automatically generated](media/image16.png){width="6.5in"
height="2.9618055555555554in"}

**Data Warehousing and Visualization Purpose**

**AWS Glue** -- Set up AWS Glue to infer a schema from the data lake in
S3 which houses all of the 311 Service Request Events and Traffic
Accident data. We need to give AWS Glue few hints about that data is
actually named.

![Graphical user interface, application Description automatically
generated](media/image17.png){width="6.5in" height="3.50625in"}

![Graphical user interface, text, application, email Description
automatically generated](media/image18.png){width="6.5in"
height="0.9097222222222222in"}

![Table Description automatically
generated](media/image19.png){width="6.499560367454068in"
height="2.8846620734908135in"}

**Amazon Athena** -- Athena running through AWS Glue on an S3 data lake.
The advantage of using Athena is we don't to set up any servers, don't
have to import the database or the table it talks to Glue automatically.
it provides a quick and easy way to explore your data and extract
information.

![Graphical user interface, application, table Description automatically
generated](media/image20.png){width="6.76237532808399in"
height="3.189009186351706in"}

**Amazon Redshift** -- Redshift Spectrum is being used here, while we
could have copy that data into Redshift directly and let it just sit
within the Redshift, why have a copy of the data if not needed since we
have AWS Glue in place that can expose data to Redshift Spectrum and we
can query the data directly.

Advantage of using Redshift Spectrum is if we had other tables loaded
into Redshift, we join that S3 data with the other data as well.

![Graphical user interface, application Description automatically
generated](media/image21.png){width="6.5in" height="1.5375in"}

![Graphical user interface, application Description automatically
generated](media/image22.png){width="6.5in"
height="2.4791666666666665in"}

![Graphical user interface, application Description automatically
generated](media/image23.png){width="6.5in"
height="3.064583333333333in"}

> ![Graphical user interface, text, application, email Description
> automatically
> generated](media/image24.png){width="3.075219816272966in"
> height="2.492373140857393in"}

**Amazon QuickSight** -- Spin up QuickSight to visualize the data coming
out of Redshift which in turn is looking at the data in Amazon S3.

**What is the monthly trends in the total number of cases in Denver
City?**

**Monthly Trend, Total Number of Cases**![Chart, line chart Description
automatically generated](media/image25.png){width="6.311692913385826in"
height="3.3621905074365706in"}

**How are the cases distributed by geographic area?**

**Number of Cases, By Area**![Map Description automatically
generated](media/image26.png){width="6.383720472440945in"
height="3.452392825896763in"}

![Map Description automatically
generated](media/image27.png){width="6.5in"
height="3.515277777777778in"}

**Through which source most requests are generated?**

**Cases Generated by Source**![Map Description automatically
generated](media/image28.png){width="6.5in"
height="3.6277777777777778in"}

**Is the Resolution done on the First Call?**

**First Call Resolution Distribution**![Map Description automatically
generated](media/image29.png){width="6.5in"
height="3.372916666666667in"}

**Top 5 events common in an area?**

**Top 5 Events in an Area**![Map Description automatically
generated](media/image30.png){width="6.5in"
height="3.6618055555555555in"}

**Which are the Top Ten busiest departments?**

**Ten Most Busy Departments**![Chart Description automatically
generated](media/image31.png){width="6.5in"
height="3.334722222222222in"}

**Percentage of case status between Resolved and Unresolved?**

**Case Status Ratio**![Chart, pie chart Description automatically
generated](media/image32.png){width="6.5in"
height="3.991898512685914in"}

**Type of Case Area wise?**

![Map Description automatically
generated](media/image33.png){width="6.5in" height="4.425in"}

**Top Ten Most Common Cases?**

![Chart, pie chart Description automatically
generated](media/image34.png){width="3.492101924759405in"
height="3.279070428696413in"}

**Monthly Volume?**

**Monthly Volume of Service Requests**![Chart, line chart Description
automatically generated](media/image35.png){width="5.369832677165355in"
height="3.8994389763779527in"}

**At what time most request is made at (hourly)?**

**Service Request Calls by Hourly**![Chart, line chart Description
automatically generated](media/image36.png){width="4.689624890638671in"
height="3.3233202099737533in"}

**Type of Accidents in an Area?**

![Map Description automatically
generated](media/image37.png){width="6.5in"
height="3.816666666666667in"}

**Number of traffic accidents happening around neighborhood?**

**Total Number of Traffic Accidents Near Neighborhood**![Chart
Description automatically generated](media/image38.png){width="6.5in"
height="3.5597222222222222in"}

**Future Scope**

![Diagram Description automatically
generated](media/image39.png){width="6.027777777777778in"
height="4.902777777777778in"}

**Amazon EMR** -- We can publish service request events through Kinesis
Firehose into a data lake hosted in Amazon S3 and spin up Amazon Elastic
Map Reduce Cluster to process huge volume of data using Apache Spark.

**Kinesis Data Analytics** -- We can create an operational system that
alerts us if unexpected rate of request events comes in all of a sudden
which will need someone to work in real time. We can use Kinesis Data
Streams and Kinesis Data Analytics to monitor the events and use lambda
function to send a notification using Amazon SNS.

**Amazon Elasticsearch Service** -- To Analyze event data in near real
time for operational purposes. For this we can use Kinesis Data Firehose
that will pump the data directly into Elasticsearch service where we can
easily query that data and build dashboards for it using Kibana.
