#!/usr/bin/env python
# coding=utf-8
from elasticsearch import Elasticsearch
from aws import AwsInstance
import time

es = Elasticsearch([dict(host='localhost', port=9200, http_auth=('elastic', 'changeme'))])
AwsInstance = AwsInstance()

class Elasticsearch(object, AwsInstance):
    def msgBody(self, InstanceID, InstanceIP, CreationTime, StopTime, StartTime, TerminateTime):
        self.analyzed = {'Timestamp': int(time.time()),
                         'InstanceID': InstanceID,
                         'InstanceIP': InstanceIP,
                         'CreationTime': CreationTime,
                         'StopTime': StopTime,
                         'StartTime': StartTime,
                         'TerminateTime': TerminateTime}
        self.sendToES()

    def sendToES(self):
        es.index(index='aws', doc_type='instances', body=self.analyzed)



if __name__ == '__main__':
    elastic = Elasticsearch()
    elastic.msgBody()
