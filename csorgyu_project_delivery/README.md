

# Automating Bank Marketing Campaign Inference Environment
The task is creating an automated environment for a bank marketing campaign, which includes 
* AutoML based model creation
* Model deployment as a service
* Enabling inference service monitoring with logging 
* Testing endpoint functionality
* Creating an ML pipleine for the whole workflow
* Documenting service endpoint


# Architectural Diagram
During the project I was using the udacity lab environment, which is a virtualized wondows desktop in Azure.
The Azure ML Studio is available from here through the browser, authentication is set up for me.
The first thing to do is create a compute instance to run the ipython code on.
From here I can create Compute clusters for training by code.
I created one with 4 running nodes
The results of automated ML runs (metrics, run details, logs and pickle files in the first place) are generated on the blob storage associated to the Workspace.
The Workspace is a PaaS service and encapsulates model registry, endpoint management, studio and other features for developer and admins.
Most of the steps have been created by ipython, the real time deployment was more convenient from the UI.
The real time deployment is hosted by ACI with Authentication enabled feature.
The monitoring is done by Application Insights

The endpoint test scripts are run from the virtualized desktop.
The swagger local instance and the HTTP Client is running here, swagger running on port 8000, the HTTP client on 9001, more details below.
The architectural diagram below shows the high level setup

![image](https://user-images.githubusercontent.com/81808810/117540007-69bd2900-b00d-11eb-9294-8bef8b683b95.png)


# OVERVIEW
The project consists of 2 major steps:
* Creating a real-time service endpoint with Auto ML, including
 * The ML model creation itself
 * Best model deployment
 * Enabling monitoring on the service endpoint
 * Documenting the API with swagger
 * Testing the endpoint 
* Creating a scheduled Auto ML pipeline
 * Including Pipeline build
 * Pipeline endpoint setup
 * Scheduled retraining

# PROJECT STEPS

## REAL TIME ENDPOINT 
When setting up an AutoML experiment we need to 
* Ensure the dataset we want to use is registered in the ML Workspace
* We have a compute instance where we can run the AutoML steps on
* Define Auto ML config
  * The key metric needs to be set, to compare runs, here it is AUC Weighted, as this is a classification problem
  * The timeout to save resources
  * Training dataset
  * Target variable column name mapping
  * Early stopping
  * Format of the model (onnx compatible as an example)
  * Featurization setup
* Maximum number of nodes need to be adjusted to the compute cluster size
* The best model can be selected multiple ways, I did it on the UI, and deployed the real time endpoint from the AML UI
* After deployment, when status is not finally transitioning, the Application Insights can be enabled
* The service can be consumed through the endpoint defined and the UI helps with the access token
* The test was done by the modified endpoint.py
* With swagger the details of the service endpoint can be checked
  * Input format with example payload
  * Request structure
* Based on this load test can be done

### DATASET
* This part of the project is about data acquisition
* We check the data availability and use that for later training for both tasks

#### Registered dataset is available
The registered dataset is available, there was no need to import it from the code, from web location, however the name needed to be adjusted.

#### Code call
![image](https://user-images.githubusercontent.com/81808810/117368887-6bc7a080-aec4-11eb-9d21-89c9e41ea18d.png)
Key elements:
* The dataset is either already available in the workspace, with the name string as a key or need to be downloaded and added to the workspace
* Datasets are stored in a blob storage for the workspace and Azure Blob Storage uses key-value pair based lookup  to access the blobs
* The Code creates a tabular dataset from delimited file in case it is not available 

#### Availability proof: In workspace
![image](https://user-images.githubusercontent.com/81808810/117365514-abd85480-aebf-11eb-99c9-fc53af1378ab.png)
* The dataset has actually been added to the workspace, so we just need to reference on that with a matching name

#### Availability proof: In code, with head check
![image](https://user-images.githubusercontent.com/81808810/117365418-8b0fff00-aebf-11eb-970a-20d6938a5a6e.png)
* With the take() function we can check the structure of the data, and if necessary can start data cleaning and manual fature engineering step

### AUTO ML TRAINING
* In this case we use Auto ML for model selection
* This can be the case if we have well known and relatively clean datastes, from the other side we do not have very strong business requirements/we have freedom to choose the model type
* In this example I do not focus on model selection very strongly, I let Auto ML do that for me: this approach is affordable in rapid prototyping and low value/operational cases only
* The key focus is selecting a metric, based on which we can compare the different runs of Auto ML and is a basis of comparison
* The early stopping setting of the Auto ML are also bound to this, if the model metric does not change significantly run after run, the early stopping is triggered
* This is a balancing act between best model selection and cost savings related to the compute utilized for the multiple runs of model selection

#### Auto ML Config
![image](https://user-images.githubusercontent.com/81808810/117369031-a3364d00-aec4-11eb-98cd-c07a0b628392.png)

* The focus metrics are related to the evaluation target metrics, concurrent iterations and experiment timeouts.
* The evaluation metric is AUC weighted
 * The AUC is a very typical metric for classification model evaluation
 * Classic ROC curves are agostic to the imbalance of the class skew
 * Weighted AUC can focus on certain area of the curve (like high recall, see source : https://stats.stackexchange.com/questions/158915/what-is-the-difference-between-area-under-roc-and-weighted-area-under-roc) 
* We cannot build more than 4 node clusters, so the max_concurrent_iterations appropriate value is 4
* The featurization is set to auto

#### Auto ML Run completed proof - notebook execution
![image](https://user-images.githubusercontent.com/81808810/117369748-a847cc00-aec5-11eb-84d3-1b0b17c0c197.png)

* The notebook indicates the execution has successfully finished

#### Auto ML Run completed proof - code
![image](https://user-images.githubusercontent.com/81808810/117369826-c7465e00-aec5-11eb-9b52-35d2f30e8951.png)

* The output of the  *get_runs()* call is a generator object
* We can get the items with the *next()* function
* The output shows the experiment level details: the parent run id and the experiment name
* If we want to get more details, we need to go to the clild level 

#### Auto ML Run completed proof - workspace UI
![image](https://user-images.githubusercontent.com/81808810/117369908-e349ff80-aec5-11eb-8597-d91757da1c71.png)

* The AutoML run parent level shows a summary of the runs, including properties best model summary and run summary
* The status in the upper left shows the Auto ML Experiment has completed
* We could check the child runs, but the best model is highlighted in the upper right
* This shows a Voting Ensemble model, which is a combination of several models, providing a result as a vote
* The AUC score is 0.94644 so this assumes a very strong model


#### Best model scores - summary
![image](https://user-images.githubusercontent.com/81808810/117370369-94e93080-aec6-11eb-84a8-45af03b72fad.png)

* If we click on the paren run page to the *View all other metrics* link we will see the other metrics associated to the model
* In certain use cases we need to use other metrics (too) for explaining the model value to the business, especially if the price tag to certain error types is under focus
* Even though the Auto ML uses one mertic for comparing the multiple child runs, we want to make sure, that other metrics are aligned with business expectations

#### Best model scores - further visual evaluation
![image](https://user-images.githubusercontent.com/81808810/117573741-efa6a600-b0d9-11eb-8da5-c78003f4b92c.png)

* If we click on the actual model, we can see the different scores visually too
* This helps understanding the characteristics of the model

#### Model explanation

![image](https://user-images.githubusercontent.com/81808810/117573805-3b594f80-b0da-11eb-8bb8-0a61f9089526.png)

![image](https://user-images.githubusercontent.com/81808810/117573896-d2260c00-b0da-11eb-8013-6c4f179e3d66.png)


* In the model explanation section one finds cohort analysis for the different data elements both on raw and engineered level
* As Auto ML was run with featurization, this has a key importance to see the impact of the feature engineering and what are the top N features in the raw and the eangineered features
* These all improve the model "selling points" to business, as stakeholdersa want to see the importance themselves many times, to get an intuition, however model performance in many cases can be improved with features, which have gone through many transformations

#### Model details
![image](https://user-images.githubusercontent.com/81808810/117573981-482a7300-b0db-11eb-8d8f-e8114a35cab0.png)

* The image above shows the composition of the ensamble model
* It shows that the ensemble was built on gradient boosting algorythms and tree based algorythms

### MODEL DEPLOYMENT

#### Selecting best model from code
![image](https://user-images.githubusercontent.com/81808810/117574049-82941000-b0db-11eb-8568-232b357d1f10.png)

* The best run can be retreived from the code, so we actually get the child ID which we need to focus on
* As results and the model pkl file itself is stored on the storage using the child ID, this is useful to check
* It is possible to deploy the model from code, but it is also possible to use the portal and get the best run immediately deployed

#### Deploying model directly from best run
![image](https://user-images.githubusercontent.com/81808810/117574192-36959b00-b0dc-11eb-8e2d-c2235ed24f5d.png)

* Azure generates an entry script automatically, so directly deploying the model from the run info will not require entry script.
* We enable authentication, so we can grant the service endpoint token based authentication protection
* We deploy to Azure Container Instances, but deployment can happen on Azure Kubernetes too

#### Checking successful deployment - UI
![image](https://user-images.githubusercontent.com/81808810/117574291-bcb1e180-b0dc-11eb-986a-310f3ab0908a.png)

* After the deployment we can check the service endpoints for the new deployment we created
* When clicking on the name we see, that deployment state is healthy, it is using a model ID Auto ML generated
* The same model can be seen in the models section

### ENABLING APPLICATION INSIGHTS

#### Enabling application insights from code
![image](https://user-images.githubusercontent.com/81808810/117376714-02e72500-aed2-11eb-839f-58d029b1169d.png)

* The code snippet updates the actual service endpoints
* In the background the PaaS is making changes on service endpoint an it takes ~10 minutes before the service endpoint becomes functional after successful service call
* In this period the rest endpoint is not enabled, showing null, and service state is Transitioning
* The *name* parameter need to match the one we used for manual deployment

#### Application Insights enabled - UI 
![image](https://user-images.githubusercontent.com/81808810/117574632-5fb72b00-b0de-11eb-83b6-c092a8ade4f4.png)


* After enabling Application Insights we see the service state healthy again and the rest endpoint is not null anymore


![image](https://user-images.githubusercontent.com/81808810/117574651-7493be80-b0de-11eb-80ba-ef216785638c.png)

* Lower on the UI we can see the Application Insights enabled 
* We can see the application Insigts link, which will provide us by default details about
  *  failed requests 
  *  server response time
  *  server requests
  *  availability
*  So basically all details a service needs to be checked about
*  We can set up further checks in Application Insights

### VALIDATING ML SERVICE ENDPOINT
* Here we are going to run calls from the developer environment to ensure, that the service is in good shape
* We are checking on the local development resources, after that we will run check scripts locally

#### Environment setup
##### Ensure az installed
![image](https://user-images.githubusercontent.com/81808810/117373357-5b66f400-aecb-11eb-9704-cc18269a1348.png)

* This is needed, because az based authentication will be run in the background, when running the scripts
* The active version can be checked from powershell


##### Ensure python SDK for azure is installed with ipython
![image](https://user-images.githubusercontent.com/81808810/117373617-e1833a80-aecb-11eb-8895-94504ffe149d.png)

* The development environment already has the SDK installed
* This enable local python calls being interpreted


##### Create virtual environment
![image](https://user-images.githubusercontent.com/81808810/117373931-79812400-aecc-11eb-8cae-89fe8a451621.png)

* This is useful if we want to maintain compatibility between packages and make sure, that our code can always run in the given environment
* Also we can opt for different environment versions which is useful if we want to do version upgrades systematically

#### *VALIDATION01 - service logs for real-time endpoint*
![image](https://user-images.githubusercontent.com/81808810/117574825-3fd43700-b0df-11eb-84d2-ec24fb1f75b4.png)

* The first check is that the logs for the service are available
* We make a service call to the endpoint and get the latest logs from the service

### DOCUMENTATION
#### Swagger showing API details
![image](https://user-images.githubusercontent.com/81808810/117543197-13a3b200-b01c-11eb-8981-b545e5ce4213.png)

* With swagger one can analyze the endpoint consumption ways: http get and post details
* To achieve this there are a couple of things need to be made
  * The swagger.json file needs to be downloaded from the service endpoint locally
  * A docker image, that runs swagger need to be downloade, the image need to be started on the appropriate port
  * This is implemented in the swagger.sh, once the json file is downloaded
  * The port configuration needs to be set up
  * In my specific example swagger is taking requests in the 8000 port, 8080 is internal setting
  * I have also started a python based HTTP client which serves files from locally, specifically the swagger.json
  * Once the serve.py retreived the file from the file system, swagger can showit on the user frendly UI
  * Swagger UI needs to access HTTP client on HTTP and not on HTTPS
*  GET shows the default answer if service is healthy and the format of the HTTP responsee json payload
*  POST/score shows the input payload with example values and the response code/response json structure

#### Response codes
![image](https://user-images.githubusercontent.com/81808810/117543221-27e7af00-b01c-11eb-94fa-c9d00505e590.png)

#### Swagger logs
![image](https://user-images.githubusercontent.com/81808810/117545272-50c07200-b025-11eb-8bbe-a0e3628d9df1.png)

* swagger logs can be checked on the docker desktop for the given active image
* The docker desktop gives help to understand, which port the swagger service is listening on


#### HTTP Client
![image](https://user-images.githubusercontent.com/81808810/117575682-32b94700-b0e3-11eb-85e9-c412d90ffaaa.png)

* HTTP client shows there was a request to serve the */swagger.json*/ file from local folder and the status was success (200)
* This was trhe result of me accessing the URI from the swagger browser
* The HTTP client is running on port 9001 not to conflict with the swagger endpoint

#### *VALIDATION02 - service endpoint consumption*
![image](https://user-images.githubusercontent.com/81808810/117378064-f7e1c400-aed4-11eb-8246-63be2e056329.png)

![image](https://user-images.githubusercontent.com/81808810/117575046-6c3c8300-b0e0-11eb-84e8-272483b9d6ee.png)


* The consumption is implemented by the endpoint.py file
* This needs to be amended by the endpoint URI and the token
* These 2 can be obtained from the Consume tab of rhe endpoint
* Tokens can be regenerated, this is a typical maintenance task for MLOPS


## ML PIPELINE AUTOMATION

* In this project section we focus on automated ML workflows, which may be recurring maintenance tasks for the model service and model objects
* This AutoML pipeline is used for a reproducible trainings, this is very useful, if we want to control model decay
* Batch inference pipelines can be set up and retraining ones as well
* The current implementation is a retraining pipeline, that runs every 24 hours
* The pipeline is created from code, can be verified from the UI
* The video shows the details of the pipeline being deployed.
* The screenshots below show, that the retraining is scheduled


### CREATING PIPELINE

* In this task we produce a pipeline with one single step: an AutoML based training on a dataste
* We expect the training to be done many times, and the scenario is making sure, that our model is up to date with the latest data and is less exposed to model decay
* Dependent how rapsodically the base data changes and also how often  and with wath usage patterns the model is consumed, this can be done with different schedules
* Pipelines steps are daisy chained together with outputs, so one step can consume and process further the next step

#### Creating pipeline from code
![image](https://user-images.githubusercontent.com/81808810/117576167-0ef70080-b0e5-11eb-951a-c57fa583b507.png)

![image](https://user-images.githubusercontent.com/81808810/117576064-b162b400-b0e4-11eb-8a54-6f618018e453.png)

* The pipeline takes the Auto ML config as an input, in this specific case this is the same input we used for the real-time endpoint
* The step name is *automl_module*
* Output definitions contain where the models and the metrics can be added - these are stored on the blob storage backend
* The step is set to be able to reused 
* A pipeline is created andthe single step is added


#### Pipeline endpoint has been created
##### From UI
![image](https://user-images.githubusercontent.com/81808810/117576713-2afba180-b0e7-11eb-98e8-f63467b44507.png)

* The Workspace supports UI help to check on active pipeline runs (with status) and pipeline endpoints too
* Similarly to experiments not using pipelines the main run details and the child run details can be observed
* The UI shows, that I used a different experiment for pipeline based run as for real time endpoint

##### From code
![image](https://user-images.githubusercontent.com/81808810/117576750-5aaaa980-b0e7-11eb-948e-6f92f7e24f98.png)

* The execution summary shows, that the run has ended
* It also references on the
  * Start and end time
  * The log locations on the blob storage
  * And the pipeline run ID itself 
* The code based check is important, as the typical use case for ML pipelines in scheduled autoated execution with no human manual check in the loop

### CHECKING PIPELINE RESULTS

#### Checking details from code
![image](https://user-images.githubusercontent.com/81808810/117576854-ac533400-b0e7-11eb-9cdf-f93240cf7733.png)

* The run details of child runs can be accessed programmatically
* The API call deserializes the results and can be consumed in a regular dataframe
* In this specific example pipeline child runs are in columns and scores are in rows
* Further post processing is possible based on dataset like
  * Selecting a model based on a specific metric (not necessarily the one we optimized the run for)
  * Setting up alerts if specific metrics are not up to par 

#### Selecting best model
![image](https://user-images.githubusercontent.com/81808810/117577143-e113bb00-b0e8-11eb-91e8-1f5d98346e43.png)

* Best model can be selected based on the metric we used for the autoML config
* This is retrieving the model from the backend storage in the format of the pickle file
* The best model structure can be visualized 

#### Checking steps from code
![image](https://user-images.githubusercontent.com/81808810/117577204-1d471b80-b0e9-11eb-80e3-0841d4ba7c74.png)

* As automated ML runs on many model types, and with additional featurization, it is important to understand the actually execued steps
* These can be observed by code
* From the other side if needed these can be later further optimized by hyperdrive, once the method is understood and explained

#### Testing the best model
![image](https://user-images.githubusercontent.com/81808810/117577259-613a2080-b0e9-11eb-8c2b-ded57214ec7f.png)

* Code based test is important for the model
* Before we start using the actual run and maybe retrain the model the same way, we need to be sure, that the errors are in an appropriate distribution in the confusion matrix, as the example shows
* These outputs are stored on the blob but can be exposed to other storages where BI can be added for operatiosn team or business

### CHECKING DETAILS ON UI
![image](https://user-images.githubusercontent.com/81808810/117577638-e6720500-b0ea-11eb-83b9-09cdf906ba7e.png)

* The screensho shows the 1 single step of the pipeline, that is executed, this is the automl step, on the top of the dataset
* We can get the pipeline ID from here
* We can see the last run time and last run status


### CHECKING REST ENDPOINT FOR PIPELINE

#### REST API Endpoint status - UI
![image](https://user-images.githubusercontent.com/81808810/117543353-c07e2f00-b01c-11eb-901b-b91fd9ba97b5.png)

* The REST API status can be checked on the UI
* This shows that the pipeline being in active status
* The pipleine ID can be obtained either from here or from code


#### REST API Endpoint status - code
![image](https://user-images.githubusercontent.com/81808810/117577394-e291b300-b0e9-11eb-9717-9db8b4e7b3f6.png)

* The endpoint status can be checked in an automated manner
* Here the call also shows status as *Active* , should that be different automated alerts could be triggered

#### Checking last run status
![image](https://user-images.githubusercontent.com/81808810/117577488-3c927880-b0ea-11eb-81c3-8c3083315c0c.png)

* This can be important, if we want to monitor stuck or failed pipelines
* Those would leave our service in an undesirabled state
* So alerts need to be established on those too


### SCHEDULED RUN
#### Scheduling a run from code
![image](https://user-images.githubusercontent.com/81808810/117578022-a9a70d80-b0ec-11eb-8ed6-bafddc2fe5fc.png)

* We can set up scheduled runs
* Currently we have a training pipeline, recurring training is useful if we want to control for model decay
* If we want to do scoring in that case batch inference pipelines need to be used
* Here we want to sue the experiment name we created in the previous section

#### Schedule is ready
![image](https://user-images.githubusercontent.com/81808810/117578197-816bde80-b0ed-11eb-9bc2-2bbd701a044c.png)

* The latest pipeline scheduled by the trigger has finished
* We have a recurring training now every 24 hours



## Screen Recording
https://youtu.be/0mA8XTVLO6E

Second attempt,coverinng model section too

## Standout Suggestions
Future improvement steps:
* Creating batch inference pipeline for the new data
* Detailed service endpoint monitoring based on Application Insights for real-time endpoint
* Systematic monitoring of the pipeline retraining
* Model performance check based on daily retraining and making sure all metrics stay within a range
* Load testing of the models
