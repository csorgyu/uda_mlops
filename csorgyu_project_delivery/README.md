*NOTE:* This file is a template that you can use to create the README for your project. The *TODO* comments below will highlight the information you should be sure to include.


# Automating Bank Marketing Campaign Inference Environment
The task is creating an automated environment for a bank marketing campaign, which includes 
* AutoML based model creation
* Model deployment as a service
* Enabling inference service monitoring with logging 
* Testing endpoint functionality
* Creating an ML pipleine for the whole workflow
* Documenting service endpoint


## Architectural Diagram
*TODO*: Provide an architectual diagram of the project and give an introduction of each step. An architectural diagram is an image that helps visualize the flow of operations from start to finish. In this case, it has to be related to the completed project, with its various stages that are critical to the overall flow. For example, one stage for managing models could be "using Automated ML to determine the best model".

![image](https://user-images.githubusercontent.com/81808810/117540007-69bd2900-b00d-11eb-9294-8bef8b683b95.png)


## Key Steps
*TODO*: Write a short discription of the key steps. Remeber to include all the screenshots required to demonstrate key steps. 
### Auto ML Experiment
#### Registered dataset is available
The registered dataset is available, there was no need to import it from the code, from web location, however the name needed to be adjusted.
##### Code call
![image](https://user-images.githubusercontent.com/81808810/117368887-6bc7a080-aec4-11eb-9d21-89c9e41ea18d.png)
##### Availability proof: In workspace
![image](https://user-images.githubusercontent.com/81808810/117365514-abd85480-aebf-11eb-99c9-fc53af1378ab.png)
##### Availability proof: In code, with head check
![image](https://user-images.githubusercontent.com/81808810/117365418-8b0fff00-aebf-11eb-970a-20d6938a5a6e.png)
#### Experiment is shown as completed
##### Auto ML Config
The explain best model's paramater's default value is True, however I am setting that up explicitly as a proof.
![image](https://user-images.githubusercontent.com/81808810/117369031-a3364d00-aec4-11eb-98cd-c07a0b628392.png)
##### Auto ML Run shows completed in the code
![image](https://user-images.githubusercontent.com/81808810/117369748-a847cc00-aec5-11eb-84d3-1b0b17c0c197.png)
##### In notebook programmatically: Auto ML Runs generator has the copleted item as a most recent element
![image](https://user-images.githubusercontent.com/81808810/117369826-c7465e00-aec5-11eb-9b52-35d2f30e8951.png)
##### In workspace
The result shows the best model is a voting ensamble
![image](https://user-images.githubusercontent.com/81808810/117369908-e349ff80-aec5-11eb-8597-d91757da1c71.png)
#### Best model
The best model is a voting ensemble, wit 0.947 AUC, which is surprisingly high.
![image](https://user-images.githubusercontent.com/81808810/117370369-94e93080-aec6-11eb-84a8-45af03b72fad.png)
#### Model explanation
![image](https://user-images.githubusercontent.com/81808810/117375729-e813b100-aecf-11eb-9d3c-aefc3d387261.png)


### Deploying the model
#### Selecting best model from code
![image](https://user-images.githubusercontent.com/81808810/117371173-ba2a6e80-aec7-11eb-9bac-2b25ad959501.png)
#### Registering model
![image](https://user-images.githubusercontent.com/81808810/117371540-581e3900-aec8-11eb-929d-38b0ecf47db4.png)
#### Deploying model directly from best run
Azure generates an entry script automatically, so directly deploying the model from the run info will not require entry script.
![image](https://user-images.githubusercontent.com/81808810/117372526-f5c63800-aec9-11eb-87e1-d771f7a4781c.png)
#### Enabling authentication and using ACI 
![image](https://user-images.githubusercontent.com/81808810/117372735-4f2e6700-aeca-11eb-9ffc-3e0f294404c0.png)
#### Deployment successful
![image](https://user-images.githubusercontent.com/81808810/117372895-94eb2f80-aeca-11eb-8ebf-edab0eb3fb7e.png)

### Enabling Application Insights
#### Ensure az installed
![image](https://user-images.githubusercontent.com/81808810/117373357-5b66f400-aecb-11eb-9704-cc18269a1348.png)
#### Ensure python SDK for azure is installed with ipython
![image](https://user-images.githubusercontent.com/81808810/117373617-e1833a80-aecb-11eb-8895-94504ffe149d.png)
#### Create virtual environment
![image](https://user-images.githubusercontent.com/81808810/117373931-79812400-aecc-11eb-8cae-89fe8a451621.png)
#### Enabling application insights from code
![image](https://user-images.githubusercontent.com/81808810/117376714-02e72500-aed2-11eb-839f-58d029b1169d.png)

#### Proof for application insights being enabled
Healthy endpoint
![image](https://user-images.githubusercontent.com/81808810/117377062-b05a3880-aed2-11eb-8b25-d35e6fe3c12c.png)

And enabled application insights
![image](https://user-images.githubusercontent.com/81808810/117377114-c7008f80-aed2-11eb-8f6e-e1b5eacc90c1.png)

#### Proof in the logs.py output
![image](https://user-images.githubusercontent.com/81808810/117377284-35dde880-aed3-11eb-8382-15b54cef0f83.png)

#### Checking Apache Benchmark
![image](https://user-images.githubusercontent.com/81808810/117378196-324b6100-aed5-11eb-9fd7-6db81494cd9d.png)

### Documentation
#### Swagger runs locally and shows the API details
![image](https://user-images.githubusercontent.com/81808810/117543197-13a3b200-b01c-11eb-8981-b545e5ce4213.png)

#### Response codes
![image](https://user-images.githubusercontent.com/81808810/117543221-27e7af00-b01c-11eb-94fa-c9d00505e590.png)

#### HTTP Client
![image](https://user-images.githubusercontent.com/81808810/117543253-42218d00-b01c-11eb-82b2-8bbe077aa8c8.png)


### Enpoint consumption
#### Proof of running against the endpoint
![image](https://user-images.githubusercontent.com/81808810/117378064-f7e1c400-aed4-11eb-8246-63be2e056329.png)

### ML pipeline
#### Pipeline has been created
![image](https://user-images.githubusercontent.com/81808810/117543114-bad41980-b01b-11eb-8bfa-3627ec86d732.png)


#### Pipeline endpoint has been created
##### From UI
![image](https://user-images.githubusercontent.com/81808810/117543341-afcdb900-b01c-11eb-9ebb-9c82df14bb6c.png)
##### From code
![image](https://user-images.githubusercontent.com/81808810/117543446-32ef0f00-b01d-11eb-999e-886cafb6debf.png)


#### Dataset and Aut ML module
![image](https://user-images.githubusercontent.com/81808810/117543297-7eed8400-b01c-11eb-83cb-9ebb6d3b211c.png)


#### REST API Active status
![image](https://user-images.githubusercontent.com/81808810/117543353-c07e2f00-b01c-11eb-901b-b91fd9ba97b5.png)


#### Jupyter steps
![image](https://user-images.githubusercontent.com/81808810/117543635-f2dc5c00-b01d-11eb-9b12-961b0466d170.png)

![image](https://user-images.githubusercontent.com/81808810/117543650-025ba500-b01e-11eb-93bc-2d1b6261937e.png)




#### Scheduled run
##### Code triggered run finished
![image](https://user-images.githubusercontent.com/81808810/117543533-88c3b700-b01d-11eb-813b-3ebafabc7131.png)

![image](https://user-images.githubusercontent.com/81808810/117543558-a3962b80-b01d-11eb-844f-7c616367c8a1.png)

![image](https://user-images.githubusercontent.com/81808810/117543592-cc1e2580-b01d-11eb-9044-2f7370ad444a.png)


## Screen Recording
*TODO* Provide a link to a screen recording of the project in action. Remember that the screencast should demonstrate:

## Standout Suggestions
*TODO (Optional):* This is where you can provide information about any standout suggestions that you have attempted.
