#!/usr/bin/env python
from os import name
import json
from decouple import config
from constructs import Construct
from cdktf import TerraformStack, TerraformOutput,S3Backend
from imports.aws import Vpc, InternetGateway,IamRole,IamRolePolicy
from imports.aws import AwsProvider,Eip,NatGateway,FlowLog,CloudwatchLogGroup
from imports.aws import Subnet,RouteTable,RouteTableAssociation,DataAwsAvailabilityZones,RouteTableRoute
from .libraries import generateCidrPrivateSubnetL2,generateCidrPrivateSubnetL3,generateCidrPublicSubnetL1
from .libraries import variables,ramdomString


class awsVPC(TerraformStack):
  def __init__(self, scope: Construct, ns: str):
    super().__init__(scope, ns)
    AwsProvider(self, 'Aws', 
      region=variables().REGION,
      access_key = variables().AWS_ACCESS_KEY,
      secret_key = variables().AWS_SECRET_KEY
    )
    # S3_BACKEND = S3Backend(self,
    #   bucket = "cdktf-terraform-backend",
    #   key = "cdktf-terraform-backend/terraform.tfstate",
    #   region = variables().REGION,
    #   access_key = variables().AWS_ACCESS_KEY,
    #   secret_key = variables().AWS_SECRET_KEY
    # )
    #Create VPC
    VPC = Vpc(self, 'VPC',
      cidr_block = variables().VPC_CIDR_BLOCK,
      enable_dns_support   = True,
      enable_dns_hostnames = True,
      tags       = {
          "Name":"%s-vpc-%s" % (variables().NAME_PREFIX , ramdomString(5).value),
      }
    )
    IGW = InternetGateway(self, 'InternetGateWay',
      vpc_id  = VPC.id,
      tags    = {
        "Name":"%s-igw-%s" % (variables().NAME_PREFIX , ramdomString(5).value),
      }
    )
    ROUTE_TABLE_ROOT = RouteTableRoute(
        cidr_block= "0.0.0.0/0",
        gateway_id = IGW.id,        
    )
    ROUTE_PUBLIC_SUBNET = RouteTable(self, 'publicSubRouteTable',
      vpc_id = VPC.id,
      route = [ROUTE_TABLE_ROOT],
      tags    = {
         "Name":"%s-publicSubRouteTable-%s" % (variables().NAME_PREFIX , ramdomString(5).value),
      }
    )
    #Get DataAwsAvailabilityZone
    DATA_AVAILABILITYZONES = DataAwsAvailabilityZones(self,'dataAvailabilityZones',   
      state= "available"
    )
    #Create public subnet layer 1
    PUBLIC_SUBNET_L1 = []
    NUM_OF_PUBLIC_SUBNET = variables().AVAILABILITY_ZONE_COUNT
    for index in range(NUM_OF_PUBLIC_SUBNET):
      subnetName = "publicSubnetLayer1-%s-%s" % (str(index) , ramdomString(5).value)
      PUBLIC_SUBNET = Subnet(self, subnetName, 
        availability_zone       = "${data.aws_availability_zones.dataAvailabilityZones.names[%s]}" % index,
        vpc_id                  = VPC.id,
        cidr_block              = generateCidrPublicSubnetL1(NUM_OF_PUBLIC_SUBNET,variables().VPC_CIDR_BLOCK).value[index],
        map_public_ip_on_launch = True,
        tags    = {
            "Name":"%s-%s" % (variables().NAME_PREFIX, subnetName),
        }
      )
      RouteTableAssociationName = "public-%s-%s" % (str(index) , ramdomString(5).value)
      ROUTE_ASSOCIATION = RouteTableAssociation(self,RouteTableAssociationName,
        subnet_id      = PUBLIC_SUBNET.id,
        route_table_id = ROUTE_PUBLIC_SUBNET.id
      )
      PUBLIC_SUBNET_L1.append(PUBLIC_SUBNET)
    #Create private subnet layer 2
    if variables().LAYER_SUBNET_COUNT == 2 or variables().LAYER_SUBNET_COUNT == 3:
      PRIVATE_SUBNET_L2 = []
      NUM_OF_PRIVATE_SUBNET = variables().AVAILABILITY_ZONE_COUNT
      for index in range(NUM_OF_PRIVATE_SUBNET):
        subnetName = "privateSubnetLayer2-%s-%s" % (str(index) , ramdomString(5).value)
        PRIVATE_SUBNET = Subnet(self, subnetName, 
          availability_zone       = "${data.aws_availability_zones.dataAvailabilityZones.names[%s]}" % index,
          vpc_id                  = VPC.id,
          cidr_block              = generateCidrPrivateSubnetL2(NUM_OF_PRIVATE_SUBNET,variables().VPC_CIDR_BLOCK).value[index],
          map_public_ip_on_launch = False,
          tags    = {
              "Name":"%s-%s" % (variables().NAME_PREFIX, subnetName),
          }
        )
        PRIVATE_SUBNET_L2.append(PRIVATE_SUBNET)
    #Create private subnet layer 3
    if variables().LAYER_SUBNET_COUNT == 3:
      PRIVATE_SUBNET_L3 = []
      NUM_OF_PRIVATE_SUBNET = variables().AVAILABILITY_ZONE_COUNT
      for index in range(NUM_OF_PRIVATE_SUBNET):
        subnetName = "privateSubnetLayer3-%s-%s" % (str(index) , ramdomString(5).value)
        PRIVATE_SUBNET = Subnet(self, subnetName, 
          availability_zone       = "${data.aws_availability_zones.dataAvailabilityZones.names[%s]}" % index,
          vpc_id                  = VPC.id,
          cidr_block              = generateCidrPrivateSubnetL2(NUM_OF_PRIVATE_SUBNET,variables().VPC_CIDR_BLOCK).value[index],
          map_public_ip_on_launch = False,
          tags    = {
              "Name":"%s-%s" % (variables().NAME_PREFIX, subnetName),
          }
        )
        PRIVATE_SUBNET_L3.append(PRIVATE_SUBNET)
    if variables().NAT_GATEWAY_SET == 'true':
      AWS_EIP_LIST = []
      NATGATEWAY_LIST = []
      for index in range(variables().AVAILABILITY_ZONE_COUNT):
        eipName = "eip-%s" % (index)        
        AWS_EIP = Eip(self, eipName,
          vpc = True,
          tags    = {
          "Name":"%s-eip-%s" % (variables().NAME_PREFIX , ramdomString(5).value),
          }
        )
        AWS_EIP_LIST.append(AWS_EIP)
        natGatewayName = "natGatewayName-%s" % (index)        
        NAT_GATEWAY = NatGateway(self, natGatewayName,
          allocation_id = AWS_EIP.id,
          subnet_id  = PUBLIC_SUBNET_L1[index-1].id,
          tags    = {
            "Name":"%s-natgateway-%s" % (variables().NAME_PREFIX , ramdomString(5).value),
          }
        )
        NATGATEWAY_LIST.append(NAT_GATEWAY)
        ROUTE_TABLE_ROOT_PRIVATE_SUB = RouteTableRoute(
          cidr_block= "0.0.0.0/0",
          gateway_id = NAT_GATEWAY.id,        
        )
        RouteTableName = "privateSubRouteTableName-%s" % (index)
        ROUTE_PRIVATE_SUBNET = RouteTable(self, RouteTableName,
          vpc_id = VPC.id,
          route = [ROUTE_TABLE_ROOT_PRIVATE_SUB],
          tags    = {
            "Name":"%s-privateSubRouteTable-%s" % (variables().NAME_PREFIX , ramdomString(5).value),
          }
        )
        RouteTableAssociationName = "routeTableAssociationName-%s" % (index)
        ROUTE_ASSOCIATION_PRIVATE_SUB = RouteTableAssociation(self,RouteTableAssociationName,
          subnet_id      = PRIVATE_SUBNET_L2[index-1].id,
          route_table_id = ROUTE_PRIVATE_SUBNET.id
        )
    if variables().VPC_FLOW_LOG_SET == 'true':
      VPC_FLOW_LOG_IAM_ROLE = IamRole(self,'VpcFlowLogIamRole',
        name = "%s-VpcFlowLogIamRole-%s" % (variables().NAME_PREFIX, ramdomString(5).value),
        assume_role_policy = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
              {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                  "Service": "vpc-flow-logs.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
              }
            ]
        })
      )
      VPC_FLOW_LOG_IAM_ROLEPOLICY = IamRolePolicy(self,'VpcFlowLogIamRolePolicy',
        name = "%s-VpcFlowLogIamRolePolicy-%s" % (variables().NAME_PREFIX, ramdomString(5).value),
        role = VPC_FLOW_LOG_IAM_ROLE.id,
        policy = json.dumps({
            "Version": "2012-10-17",
            "Statement": [
              {
                "Action": [
                  "logs:CreateLogGroup",
                  "logs:CreateLogStream",
                  "logs:PutLogEvents",
                  "logs:DescribeLogGroups",
                  "logs:DescribeLogStreams"
                ],
                "Effect": "Allow",
                "Resource": "*"
              }
            ]
          })      
      )
      VPC_FLOW_LOG_GROUP = CloudwatchLogGroup(self,'VpcFlowCloudwatchLogGroup',
        name = "%s-VpcFlowCloudwatchLogGroup-%s" % (variables().NAME_PREFIX, ramdomString(5).value),
        retention_in_days = 7
      )
      VPC_FLOW_LOG = FlowLog(self,'Vpc-flow-logs',
        iam_role_arn = VPC_FLOW_LOG_IAM_ROLE.arn,
        log_destination = VPC_FLOW_LOG_GROUP.arn,
        traffic_type = "ALL",
        vpc_id = VPC.id
      )