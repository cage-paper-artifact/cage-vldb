The azurefuncs folder contains all the code for building the azure functions for our experiments.
These azure functions are all in python.
The entire azure function code is in the `LocalFuncProj` directory. Run the following (example) command to build the docker image:
`docker build --tag <DOCKER_ID>/azurefunctionsimage:v1.0.0 .`

The folder also contains a few python scripts for testing the docker function locally. To test a docker function locally, go to the `LocalFuncProj` directory and run `func start`.

Useful Azure Functions tutorials:
Intro
https://github.com/Azure-Samples/functions-python-pytorch-tutorial/tree/master/

HTTP Trigger
https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger?tabs=python

Project Structure
https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=application-level#folder-structure

With docker and push to azure functions
https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-csharp

Push container to Azure Container Registry (ACR)
https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-docker-cli?tabs=azure-cli
^for checking image version of docker container (for CD/CI), use submenu of azure function app called deployment center

More on ACR
https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-portal

Get URL for azure function
https://stackoverflow.com/questions/51825573/how-get-azure-function-url-directly-by-code-in-azure-function-apps

Azure function tiers and scaling
https://docs.microsoft.com/en-us/azure/azure-functions/functions-scale#scale
