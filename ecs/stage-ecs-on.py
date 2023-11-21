import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
client = boto3.client('ecs')

def lambda_handler(event, context):
    
    clusterName = "DevCluster"              #ECS 클러스터 명
    serviceName = "stage-service"           #ECS service 명
    
    logger.info("Starting service on : " + format(serviceName))
    response = client.update_service(cluster=clusterName, service=serviceName, desiredCount=1)
    logger.info("response : " + format(response))  
    
    return {
        'statusCode': 200,
        'body': 'ecs service on'
    }
