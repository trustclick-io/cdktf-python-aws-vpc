# cdftf-python-aws-vpc
## Prerequisites
### You need the following installed locally:
*     Terraform v0.15+
*     CDK for Terraform
*     Node.js v12.16+
*     Python v3.7+ and pipenv
*     an AWS account and AWS Access Credentials
### Install cdktf
Link guide: [https://learn.hashicorp.com/tutorials/terraform/cdktf-installs](https://learn.hashicorp.com/tutorials/terraform/cdktf-install).

## Initialize the project
### Clone python code

Run git clone to download source code.
```
$ git clone https://github.com/trustclick-io/cdktf-python-aws-vpc.git
```

Run cdktf get to install the AWS provider you added to cdktf.json.
```
$ cd cdktf-python-aws-vpc
$ cdktf get
Generated python constructs in the output directory: imports
```
Run pipenv install to install the AWS provider you added to cdktf.json.
```
$ pipenv install
```
## Config ENV
Go to folder *modules*. Rename file .env.sample file to .env and change your setting 
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