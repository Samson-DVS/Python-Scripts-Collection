#Author: Visahl Samson David Selvam
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def get_user_input(prompt):
    return input(prompt)

def list_dynamodb_tables(session):
    try:
        dynamodb = session.client('dynamodb')
        response = dynamodb.list_tables()
        return response.get('TableNames', [])
    except Exception as e:
        print(f"Error listing DynamoDB tables: {e}")
        return []

def check_dynamodb_access(session, table_name):
    try:
        dynamodb = session.resource('dynamodb')
        table = dynamodb.Table(table_name)
        response = table.scan(Limit=1)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Error: Table '{table_name}' not found.")
        else:
            print(f"Error: Unable to access table '{table_name}'. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def check_s3_bucket_access(session, bucket_name):
    try:
        s3 = session.client('s3')
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            print(f"Error: Bucket '{bucket_name}' not found.")
        else:
            print(f"Error: Unable to access bucket '{bucket_name}'. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False

def check_sqs_access(session, queue_url):
    try:
        sqs = session.client('sqs')
        response = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['All'])
        return True
    except ClientError as e:
        print(f"Error: Unable to access SQS queue '{queue_url}'. Details: {e}")
    return False

def check_sns_access(session, topic_arn):
    try:
        sns = session.client('sns')
        response = sns.get_topic_attributes(TopicArn=topic_arn)
        return True
    except ClientError as e:
        print(f"Error: Unable to access SNS topic '{topic_arn}'. Details: {e}")
    return False

def check_rds_access(session, db_instance_identifier):
    try:
        rds = session.client('rds')
        response = rds.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
        return True
    except ClientError as e:
        print(f"Error: Unable to access RDS instance '{db_instance_identifier}'. Details: {e}")
    return False

def check_ec2_access(session, instance_id):
    try:
        ec2 = session.client('ec2')
        response = ec2.describe_instances(InstanceIds=[instance_id])
        return True
    except ClientError as e:
        print(f"Error: Unable to access EC2 instance '{instance_id}'. Details: {e}")
    return False

def check_lambda_access(session, function_name):
    try:
        lambda_client = session.client('lambda')
        response = lambda_client.get_function(FunctionName=function_name)
        return True
    except ClientError as e:
        print(f"Error: Unable to access Lambda function '{function_name}'. Details: {e}")
    return False

def main():
    print("Select the resource you want to check access for:")
    print("1. DynamoDB")
    print("2. S3")
    print("3. SQS")
    print("4. SNS")
    print("5. RDS")
    print("6. EC2")
    print("7. Lambda")
    resource_choice = get_user_input("Enter the number corresponding to your choice: ")

    if resource_choice not in ['1', '2', '3', '4', '5', '6', '7']:
        print("Invalid choice. Exiting.")
        return

    aws_access_key_id = get_user_input("Enter your AWS Access Key ID: ")
    aws_secret_access_key = get_user_input("Enter your AWS Secret Access Key: ")
    aws_region = get_user_input("Enter your AWS Region (e.g., ap-southeast-2): ")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    if resource_choice == '1':
        dynamodb_staging_table = get_user_input("Enter the name of the DynamoDB staging table: ")
        tables = list_dynamodb_tables(session)
        print(f"Tables in region '{aws_region}': {tables}")
        if dynamodb_staging_table in tables and check_dynamodb_access(session, dynamodb_staging_table):
            print(f"Access to '{dynamodb_staging_table}' is successful.")
        else:
            print(f"Access to '{dynamodb_staging_table}' failed.")
    elif resource_choice == '2':
        s3_bucket_name = get_user_input("Enter the name of the S3 bucket: ")
        if check_s3_bucket_access(session, s3_bucket_name):
            print(f"Access to S3 bucket '{s3_bucket_name}' is successful.")
        else:
            print(f"Access to S3 bucket '{s3_bucket_name}' failed.")
    elif resource_choice == '3':
        sqs_queue_url = get_user_input("Enter the SQS Queue URL: ")
        if check_sqs_access(session, sqs_queue_url):
            print(f"Access to SQS queue '{sqs_queue_url}' is successful.")
        else:
            print(f"Access to SQS queue '{sqs_queue_url}' failed.")
    elif resource_choice == '4':
        sns_topic_arn = get_user_input("Enter the SNS Topic ARN: ")
        if check_sns_access(session, sns_topic_arn):
            print(f"Access to SNS topic '{sns_topic_arn}' is successful.")
        else:
            print(f"Access to SNS topic '{sns_topic_arn}' failed.")
    elif resource_choice == '5':
        rds_instance_identifier = get_user_input("Enter the RDS DB Instance Identifier: ")
        if check_rds_access(session, rds_instance_identifier):
            print(f"Access to RDS instance '{rds_instance_identifier}' is successful.")
        else:
            print(f"Access to RDS instance '{rds_instance_identifier}' failed.")
    elif resource_choice == '6':
        ec2_instance_id = get_user_input("Enter the EC2 Instance ID: ")
        if check_ec2_access(session, ec2_instance_id):
            print(f"Access to EC2 instance '{ec2_instance_id}' is successful.")
        else:
            print(f"Access to EC2 instance '{ec2_instance_id}' failed.")
    elif resource_choice == '7':
        lambda_function_name = get_user_input("Enter the Lambda Function Name: ")
        if check_lambda_access(session, lambda_function_name):
            print(f"Access to Lambda function '{lambda_function_name}' is successful.")
        else:
            print(f"Access to Lambda function '{lambda_function_name}' failed.")

if __name__ == "__main__":
    main()
