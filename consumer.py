import kombu

from nova import rpc

class TopicConsumer(rpc.ConsumerBase):
    """Consumer class for 'topic'"""

    def __init__(self, conf, channel, topic, callback, tag, name=None,
                 **kwargs):
        """Init a 'topic' queue.

        :param channel: the amqp channel to use
        :param topic: the topic to listen on
        :paramtype topic: str
        :param callback: the callback to call when messages are received
        :param tag: a unique ID for the consumer on the channel
        :param name: optional queue name, defaults to topic
        :paramtype name: str

        Other kombu options may be passed as keyword arguments
        """
        # Default options
        options = {'durable': conf.rabbit_durable_queues,
                   'auto_delete': False,
                   'exclusive': False}
        options.update(kwargs)
        exchange = kombu.entity.Exchange(name=conf.control_exchange,
                                         type='topic',
                                         durable=options['durable'],
                                         auto_delete=options['auto_delete'])
        super(TopicConsumer, self).__init__(channel,
                                            callback,
                                            tag,
                                            name=name or topic,
                                            exchange=exchange,
                                            routing_key=topic,
                                            **options)

def patch_topic_consumer():
    nova.rpc.impl_kombu.TopicConsumer = TopicConsumer
