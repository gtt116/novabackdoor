novabackdoor
============

A AMQP backdoor for openstack nova. 
It listen on rabbitmq to receive msg from compute, network, scheduler.
Also It can receive notification from other compoment.


NOTE
========

This script is written under folsom nova.
Since Folsom nova mova rpc to openstack.common, and some construnction of some
class has changed. I monkey patch the rpc impletation to be compatible with
Essex nova. The code of monkey patch is locate in consumer.py

