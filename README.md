
# Welcome to API Rest Demo!

In this demo we are going to demostrate how to create a CDK project from scratch.

Below you are going to find the steps to create the project.

## 1. Create a folder for your project.
```
mkdir api_rest
cd api_rest
```
## 2. Initializing CDK Project.
First of all initialize the CDK project with:
```
cdk init sample-app --language python
```
Project folder needs to be empty. It's a must!
Now, activate the virtual environment:
```
source .venv/bin/activate
```
Finally, install the required python modules.
```
pip install -r requirements.txt
```
## 3. Bootstraping an environment
Use the command 
```
cdk bootstrap
```
You need to know that previuosly you need to configure AWS CLI credentials with correspondant permissions. 

## 4. Deploy your app:

```
cdk deploy
```


