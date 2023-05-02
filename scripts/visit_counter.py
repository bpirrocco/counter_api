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

    def get_count(self, name):
        """Gets counter item from table and reads its value.
        
            Args:
                name: value of Count partition key
        """
        try:
            response = self.table.get_item(Key={'Count': name})
            item = response['Item']
            d = item['Val']
            counter = int(d)
        except ClientError as err:
            logger.error(
                "Couldn't get count %s from table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return counter

    def update_count(self, name, count):
        """Update counter item and return it to the table
        
            Args:
                name: value of Count partition key

                count: current value of counter item
        """
        try:
            count += 1
            response = self.table.update_item(Key={'Count': name},
                                              UpdateExpression='SET Val = :val1',
                                              ExpressionAttributeValues={
                                                ':val1': count
                                              })
        except ClientError as err:
            logger.error(
                "Couldn't update count %s from table %s. Here's why: %s: %s",
                count, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return {'Count': count}

def lambda_handler(event, context):
    # TODO implement
    dynamodb = boto3.resource('dynamodb')
    table = "Counter"
    counter = VisitCounter(dynamodb, table)
    pre_count = counter.get_count(table)
    post_count = counter.update_count(table, pre_count)
    return {
        'statusCode': 200,
        'body': json.dumps(post_count)
    }

