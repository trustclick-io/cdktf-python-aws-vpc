# cdftf-python-aws-vpc
## Prerequisites
### You need the following installed locally:
*     Terraform v0.15+
*     CDK for Terraform
*     Node.js v12.16+
*     Python v3.7+ and pipenv
*     an AWS account and AWS Access Credentials
### Initialize a new CDK for Terraform application

Start by creating a directory named cdktf-python for the project.

```
$ mkdir cdktf-python
$ cd learn-cdktf-python
```
Inside the directory, run cdktf init with the python template. Use --local to store Terraform's state file on your machine instead of remotely in Terraform Cloud.

```
$ cdktf init --template="python" --local
```
### Add AWS provider
Open cdktf.json in your text editor, and add aws as one of the Terraform providers that you will use in the application.
```
{
   "language": "python",
   "app": "pipenv run python main.py",
-  "terraformProviders": [],
+  "terraformProviders": [
+    "hashicorp/aws@~> 3.42"
+  ],
   "terraformModules": [],
   "codeMakerOutput": "imports",
   "context": {
       "excludeStackIdFromLogicalIds": "true",
       "allowSepCharsInLogicalIds": "true"
  } 
}
```
Run cdktf get to install the AWS provider you added to cdktf.json.
```
$ cdktf get
Generated python constructs in the output directory: imports
```
## Install python-decouple 
Open Pipfile in your text editor, and add package python-decouple
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[requires]
python_version = "3"

[packages]
cdktf = "~=0.5.0"
+ python-decouple = "~=3.4"
```
Run pipenv install to install the AWS provider you added to cdktf.json.
```
$ pipenv install
```
## Copy main.py and folder "modules" into your project.
The stack output directory is as follows.
```
tree .
.
├── imports
├── modules
└── main.py
```
## Rename .env.sample file to .env
Rename and change your setting 
AWS_ACCESS_KEY
AWS_SECRET_KEY
...
REGION

## Provision infrastructure
Now that you have initialized the project with the AWS provider and written code to provision an instance, it's time to deploy it by running cdktf deploy. Remember to confirm the deploy with a yes
```
$ cdktf deploy
Deploying Stack: awsVPC
```