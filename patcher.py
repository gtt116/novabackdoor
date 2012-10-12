import kombu
import functools

from nova import flags
from nova.rpc import impl_kombu

class TopicConsumer(impl_kombu.ConsumerBase):
    """Consumer class for 'topic'"""

    def __init__(self, channel, topic, callback, tag, conf, name=None,
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

def _declare_topic_consumer(self, topic, callback=None, queue_name=None):
    self.declare_consumer(functools.partial(TopicConsumer,
                                            name=queue_name, conf=flags.FLAGS),
                          topic, callback)

def patch_topic_consumer():
    impl_kombu.TopicConsumer = TopicConsumer
    impl_kombu.Connection.declare_topic_consumer = _declare_topic_consumer
