import json
import boto3
import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class VisitCounter:
    """Encapsulates DynamoDB table for the visit counter"""
    def __init__(self, dyn_resource):
        """
        Args: 
            dyn_resource: A Boto3 DynamoDB resource
        """
        self.dyn_resource = dyn_resource
        self.table = "Counter"

    def get_count(self, count):
        """Gets counter item from table and reads its value.
        
            Args:
                count: value of Count partition key
        """
        try:
            response = self.table.get_item(Key={'Count': count})
        except ClientError as err:
            logger.error(
                "Couldn't get count %s from table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return response['Item']

    # def update_count(self, count):
    #     """Update"""


def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Counter')
    response = table.get_item(
    Key={
        'Count': 'Counter'
    }
    )
    item = response['Item']
    d = item['Value']
    count = {'Count': int(d)}
    return {
        'statusCode': 200,
        'body': json.dumps(count)
    }

