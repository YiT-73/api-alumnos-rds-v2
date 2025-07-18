import boto3
import pymysql
import os
import json

def lambda_handler(event, context):
    secret_name = os.environ['DB_SECRET']  # Ej: 'dev/dbCredentials'
    region_name = os.environ['AWS_REGION']  # Asegúrate de configurarlo

    # Cliente de Secrets Manager
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(get_secret_value_response['SecretString'])

        connection = pymysql.connect(
            host=secret['host'],
            user=secret['username'],
            password=secret['password'],
            db=secret['dbname'],
            connect_timeout=5
        )

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM alumnos;")
            results = cursor.fetchall()

        return {
            "statusCode": 200,
            "body": results
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "error": str(e)
        }

    finally:
        if 'connection' in locals():
            connection.close()