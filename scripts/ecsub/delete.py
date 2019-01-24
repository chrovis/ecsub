# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 13:06:19 2018

@author: Okada
"""

import ecsub.aws
import ecsub.tools
import glob

def main(params):
    
    params["wdir"] =  params["wdir"].rstrip("/")
    summary_list = glob.glob("%s/%s/log/summary.*.log" % (params["wdir"], params["task_name"]))
    if len(summary_list) == 0:
        print (ecsub.tools.error_message (params["task_name"], None, "task-name %s is not find in directory %s." % (params["wdir"], params["task_name"])))
        return 1
    
    params["wdir"] =  "%s/%s" % (params["wdir"].rstrip("/"), params["task_name"])
    
    import json
    summary = json.load(open(summary_list[0]))
    params["aws_key_name"] = summary["KeyName"]
    params["aws_security_group_id"] = summary["SecurityGroupId"]
    params["cluster_name"] = summary["ClusterName"]
    params["shell"]  = summary["Shell"]
    params["aws_ecs_task_vcpu"]  = summary["EcsTaskVcpu"]
    params["aws_ecs_task_memory"] = summary["EcsTaskMemory"]
    params["aws_ec2_instance_disk_size"] = summary["Ec2InstanceDiskSize"]
    params["image"] = summary["Image"]
    params["use_amazon_ecr"] = summary["UseAmazonEcr"]
    params["spot"] = summary["Spot"]
    
    params["aws_ec2_instance_type_list"] = ['']
    params["aws_ec2_instance_type"] = ""
    params["aws_subnet_id"] = ""
    params["retry_od"] = False
        
    aws_instance = ecsub.aws.Aws_ecsub_control(params, 1)
    aws_instance.aws_key_auto = summary["AutoKey"]
    aws_instance.cluster_arn = summary["ClusterArn"]
    aws_instance.task_definition_arn = summary["TaskDefinitionAn"]
    
    aws_instance.clean_up()
    
    return 0
    
def entry_point(args, unknown_args):
    
    params = {
        "wdir": args.wdir,
        "task_name": args.task_name,
        "set_cmd": "set -x",
    }
    return main(params)
    
if __name__ == "__main__":
    pass