import json
import boto3
import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class VisitCounter:
    """Encapsulates DynamoDB table for the visit counter"""
    def __init__(self, dyn_resource, table):
        """
        Args: 
            dyn_resource: A Boto3 DynamoDB resource
        """
        self.dyn_resource = dyn_resource
        self.table = dyn_resource.Table(table)

    def get_count(self, count):
        """Gets counter item from table and reads its value.
        
            Args:
                count: value of Count partition key
        """
        try:
            response = self.table.get_item(Key={'Count': count})
            item = response['Item']
            d = item['Value']
            counter = {'Count': int(d)}
        except ClientError as err:
            logger.error(
                "Couldn't get count %s from table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return counter

    # def update_count(self, count):
    #     """Update"""


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = "Counter"
    # response = table.get_item(
    # Key={
    #     'Count': 'Counter'
    # }
    # )
    # item = response['Item']
    # d = item['Value']
    # count = {'Count': int(d)}
    counter = VisitCounter(dynamodb, table)
    count = counter.get_count("Counter")
    return {
        'statusCode': 200,
        'body': json.dumps(count)
    }

