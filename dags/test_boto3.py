import boto3
import json

s3 = boto3.client('s3')

data = {
    'name': 'Fluminense',
    'age': 24,
    'year': 1912
}

s3.put_object(
    Bucket='simple-pipeline-lucastassi',
    Body=json.dumps(data),
    Key='teams/' + data['name'].lower() + '.json'
)
