#!/usr/bin/env python
# coding=utf-8

import boto.ec2
import time
from notify import Elasticsearch

Elasticsearch = Elasticsearch()

conn = boto.ec2.connect_to_region("sa-east-1", aws_access_key_id='AKIAIWT7JWYSCQP2CXPQ',
                                  aws_secret_access_key='x')


class AwsInstance(object, Elasticsearch):
    def __init__(self, instanceId):
        self.instanceId = instanceId

    def createNewInstance(self):
        self.createInstanceTime = int(time.time())
        print 'Start instance'
        reservations = conn.run_instances(image_id='ami-4485d628', key_name='douglas-evo', instance_type='t2.micro',
                                          subnet_id='subnet-3e84ce59')
        self.instance = reservations.instances[0]
        self.objectId = self.instance
        self.instance.add_tag('Name', 'aws-handler')
        self.metrics()
        print 'Instance ID: '+ self.id
        self.waitState(stateWait='running')
        return self.instanceId

    def metrics(self):
        self.id = self.objectId.id.encode("utf-8")
        self.state = self.objectId.state.encode("utf-8")
        self.ip = self.objectId.private_ip_address.encode("utf-8")
        self.instanceId = self.instance.id.encode("utf-8")

    def stopInstance(self):
        self.stopInstanceTime = int(time.time())
        self.waitState(stateWait='running')
        self.objectId.stop()

    def startInstace(self):
        self.startInstanceTime = int(time.time())
        self.waitState(stateWait='stopped')
        self.objectId.start()

    def terminateInstance(self):
        self.terminateInstanceTime = int(time.time())
        self.waitState(stateWait='running')
        self.objectId.terminate()
        self.waitState(stateWait='terminated')

    def waitState(self, stateWait):
        while self.objectId.state not in (stateWait):
            time.sleep(11)
            self.objectId.update()

    def InfoInstace(self):
        print 'Instance IP: '+ self.ip
        print 'Instance ID: ' + self.id
        print 'Instance State: ' + self.state
        print 'Creation Date: ', self.createInstanceTime
        print 'Stop Date:', self.stopInstanceTime
        print 'Start Time:', self.startInstanceTime
        print 'Terminate Time:', self.terminateInstanceTime

    def notify(self):
        return Elasticsearch.msgBody(
            InstanceID=self.id,
            InstanceIP=self.ip,
            CreationTime=self.createInstanceTime,
            StartTime=self.startInstanceTime,
            StopTime=self.stopInstanceTime,
            TerminateTime=self.terminateInstanceTime)


if __name__ == '__main__':
    a = AwsInstance(instanceId='Null')
    a.createNewInstance()
    a.stopInstance()
    a.startInstace()
    a.terminateInstance()
    a.notify()


