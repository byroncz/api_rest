
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
You need to know that previuosly you need to configure AWS CLI credentials with correspondant permissions. For more info: 

## 4. Bootstraping an environment





You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`api_rest_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under th e .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
