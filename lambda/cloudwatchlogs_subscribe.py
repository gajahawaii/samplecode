import boto3
import logging
import json
import gzip
import urllib
import time
from StringIO import StringIO

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    bucketS3 = 'cloudwatchlogs-sample'
    folderS3 = 'apigateway'
    prefixS3 = 'apigateway_'
    
    #capture the CloudWatch log data
    outEvent = str(event['awslogs']['data'])
    
    #decode and unzip the log data
    outEvent = gzip.GzipFile(fileobj=StringIO(outEvent.decode('base64','strict'))).read()
    
    #convert the log data from JSON into a dictionary
    cleanEvent = json.loads(outEvent)
    
    #create a temp file
    tempFile = open('/tmp/file', 'w+')
    
    #loop through the events line by line
    for t in cleanEvent['logEvents']: 
        tempFile.write(str(t['id']) + "|" +str(t['timestamp']) + "|" + str(t['message'])+"\n")
    tempFile.close()    
      
    #write the files to s3
	key = folderS3 + '/' + prefixS3 + str(int(time.time())) + ".log"
    s3Results = s3.upload_file('/tmp/file', bucketS3, key)
    print s3Results