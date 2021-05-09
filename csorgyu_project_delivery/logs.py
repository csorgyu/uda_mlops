from azureml.core import Workspace
from azureml.core.webservice import Webservice

# Requires the config to be downloaded first to the current working directory
ws = Workspace(
	subscription_id="9b72f9e6-56c5-4c16-991b-19c652994860",
	resource_group="aml-quickstarts-144279",
	workspace_name="quick-starts-ws-144279"
)

# Set with the deployment name
name = "bankmarketing-model-dply3"

# load existing web service
service = Webservice(name=name, workspace=ws)

# enable application insight
# we have done this from notebook
#service.update(enable_app_insights=True)

logs = service.get_logs()

for line in logs.split('\n'):
    print(line)