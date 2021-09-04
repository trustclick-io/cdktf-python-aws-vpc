#!/usr/bin/env python
import random
import string
from decouple import config

class ramdomString:
    def __init__(self,len):
        length_of_string = len
        strings = string.ascii_lowercase
        random_string = ""
        for number in range(length_of_string):
            random_string += random.choice(strings)
        self.value = random_string
class generateCidrPrivateSubnetL2:
    def __init__(self,numOfsubnet,vpc_cidr):
        LIST_SUBNETS = []
        for x in range(100,numOfsubnet+100,1):
            SUB = vpc_cidr.split(".")
            SUB[2] = str(x)
            SUB[3] = '0/24'
            LIST_SUBNETS.append(str('.'.join(SUB)))
        self.value = LIST_SUBNETS
class generateCidrPrivateSubnetL3:
    def __init__(self,numOfsubnet,vpc_cidr):
        LIST_SUBNETS = []
        for x in range(200,numOfsubnet+200,1):
            SUB = vpc_cidr.split(".")
            SUB[2] = str(x)
            SUB[3] = '0/24'
            LIST_SUBNETS.append(str('.'.join(SUB)))
        self.value = LIST_SUBNETS
class generateCidrPublicSubnetL1:
    def __init__(self,numOfsubnet,vpc_cidr):
        LIST_SUBNETS = []
        for x in range(1,numOfsubnet+1,1):
            SUB = vpc_cidr.split(".")
            SUB[2] = str(x)
            SUB[3] = '0/24'
            LIST_SUBNETS.append(str('.'.join(SUB)))
        self.value = LIST_SUBNETS
class variables:
    def __init__(self):
        self.AWS_ACCESS_KEY = config('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_KEY = config('AWS_SECRET_ACCESS_KEY')
        self.NAME_PREFIX = config('NAME_PREFIX')
        self.REGION = config('REGION').lower()
        if config('VPC_CIDR_BLOCK').split(".")[3] != '0/16':
            print ('Please set prefix only /16')
        else:
            self.VPC_CIDR_BLOCK=config('VPC_CIDR_BLOCK')
        if config('LAYER_SUBNET_COUNT') == "":
            self.LAYER_SUBNET_COUNT = 1
        elif int(config('LAYER_SUBNET_COUNT')) > 3 :
            print ("Exceed the number of layers allowed to create, please set from 1 to 3")
        else:
            self.LAYER_SUBNET_COUNT = int(config('LAYER_SUBNET_COUNT'))

        if config('AVAILABILITY_ZONE_COUNT') == "":
            self.AVAILABILITY_ZONE_COUNT = 1
        else:
            self.AVAILABILITY_ZONE_COUNT = int(config('AVAILABILITY_ZONE_COUNT'))
        
        if config('NAT_GATEWAY_SET').lower() == "":
            self.NAT_GATEWAY_SET = "false"
        elif config('NAT_GATEWAY_SET').lower() == "true" or config('NAT_GATEWAY_SET').lower() == "false":
            self.NAT_GATEWAY_SET = config('NAT_GATEWAY_SET').lower()    
        else:
            print ("Please enter True or False")

        if config('VPC_FLOW_LOG_SET').lower() == "":
            self.VPC_FLOW_LOG_SET = "false"
        elif config('VPC_FLOW_LOG_SET').lower() == "true" or config('VPC_FLOW_LOG_SET').lower() == "false":
            self.VPC_FLOW_LOG_SET = config('VPC_FLOW_LOG_SET').lower()    
        else:
            print ("Please enter True or False")
