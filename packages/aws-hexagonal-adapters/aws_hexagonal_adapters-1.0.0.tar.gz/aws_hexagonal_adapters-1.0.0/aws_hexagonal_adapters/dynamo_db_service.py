# -*- coding: utf-8 -*-
"""Abstraction layer on top of AWS Event Bridge."""
import os
import boto3

# noinspection PyPackageRequirements
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

LOGGER = Logger(sampling_rate=float(os.environ["LOG_SAMPLING_RATE"]), level=os.environ["LOG_LEVEL"])


class DynamoDBService:
    """Interact with DynamoDB using the AWS boto3 library."""

    def __init__(self, region_name="eu-west-1"):
        """Initialize region in which operations will be performed.

        :param region_name: default eu-west-1
        """
        self.__client = boto3.resource(
            "dynamodb",
            region_name=region_name,
            endpoint_url=f"https://dynamodb.{region_name}.amazonaws.com/",
        )

    def put_item(self, table_name, item):
        """Save dict item to DynamoDB.

        :param table_name: name of the table
        :param item: dict with key/value pairs
        :return: item saved to DynamoDB
        """
        table = self.__client.Table(table_name)
        try:
            item = table.put_item(Item=item)
            LOGGER.info(f"Put item into {table_name} table")
            return item
        except ClientError as error:
            LOGGER.error(f"Failed to put item into {table_name} table due to {error}")
            raise

    def batch_put_items(self, table_name, items):
        """Save multiple items into DynamoDB table.

        :param table_name: name of the table
        :param items: list of dictionaries with key/value pairs
        :return:
        """
        table = self.__client.Table(table_name)
        try:
            with table.batch_writer() as batch:
                for item in items:
                    batch.put_item(Item=item)
            LOGGER.info(f"Put {len(items)} items into {table_name} table")
        except ClientError as error:
            LOGGER.error(f"Failed to batch put for {table_name} table due to {error}")
            raise

    def delete_item(self, table_name, item):
        """Delete an item from a table.

        :param table_name: name of the table
        :param item: dict with key/value pairs
        :return: item deleted from the table
        """
        table = self.__client.Table(table_name)
        try:
            item = table.delete_item(Key=item)
            LOGGER.info(f"Delete item in {table_name} table")
            return item
        except ClientError as error:
            LOGGER.error(f"Failed to delete item from {table_name} table due to {error}")
            raise

    def get_item(self, table_name, key):
        """Get item from the DynamoDB table.

        :param table_name: name of the table
        :param key: hash key
        :return: item obtained from the table
        """
        table = self.__client.Table(table_name)
        try:
            response = table.get_item(Key=key)
            LOGGER.info(f"Got item from {table_name} table")
            return response.get("Item")
        except ClientError as error:
            LOGGER.error(f"Failed to get item from {table_name} table due to {error}")
            raise

    def update_item(self, table_name, key, expression, values):
        """Update existing item or add new one if entry don't exist.

        :param table_name: name of the table
        :param key: hash key which will be updated or added if not exists
        :param expression: dynamodb expression used to update item in the table
        :param values: expression attribute values
        :return: NotImplemented
        """
        table = self.__client.Table(table_name)
        try:
            table.update_item(Key=key, UpdateExpression=expression, ExpressionAttributeValues=values)
            LOGGER.info(f"Updated item in {table_name} table")
        except ClientError as error:
            LOGGER.error(f"Failed to update item in {table_name} table due to {error}")
            raise

    def get_items(self, table_name, filter_expression=None):
        """Get multiple items from table.

        :param table_name: name of the table
        :param filter_expression: dynamodb expression used to narrow returned results
        :return: dict with items
        """
        table = self.__client.Table(table_name)

        try:
            if filter_expression:
                response = table.scan(FilterExpression=filter_expression)
            else:
                response = table.scan()
            data = response["Items"]
            while "LastEvaluatedKey" in response:
                response = table.scan(
                    ExclusiveStartKey=response["LastEvaluatedKey"],
                    FilterExpression=filter_expression,
                )
                data.extend(response["Items"])
            LOGGER.info(f"Got {len(data)} items from {table_name} table")
            return data
        except ClientError as error:
            LOGGER.error(f"Failed to scan items from {table_name} table due to {error}")
            raise

    def get_items_page(self, table_name, filter_expression, last_evaluated_key=None, limit=500):
        """Get all elements from table limited to default 500 items per page.

        :param table_name: name of the table
        :param filter_expression: dynamodb expression used to get items in the table
        :param last_evaluated_key: the last key to start pagination from
        :param limit: default 500 items will be returned in one pagination page
        :return: list of dictionaries
        """
        table = self.__client.Table(table_name)
        try:
            if last_evaluated_key is None:
                response = table.scan(FilterExpression=filter_expression, Limit=limit)
            else:
                response = table.scan(
                    ExclusiveStartKey=last_evaluated_key,
                    FilterExpression=filter_expression,
                    Limit=limit,
                )
            LOGGER.info(f"Got { response['Count']} items from {table_name} table")
            return response
        except ClientError as error:
            LOGGER.error(f"Failed to scan items from {table_name} table due to {error}")
            raise

    def query(self, table_name, **kwargs):
        """Query DynamoDB table using key/value pairs.

        :param table_name: name of the table
        :param kwargs: dict of key/value pairs
        :return: list of dictionaries
        """
        table = self.__client.Table(table_name)

        try:
            response = table.query(**kwargs)
            data = response["Items"]
            while "LastEvaluatedKey" in response:
                kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                response = table.query(**kwargs)
                data.extend(response["Items"])
            LOGGER.info(f"Got {len(data)} items from {table_name} table")
            return data
        except ClientError as error:
            LOGGER.error(f"Failed to query items from {table_name} table due to {error}")
            raise
