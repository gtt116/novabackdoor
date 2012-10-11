#!/usr/bin/python
# IMPORTANT: The script is only used for folsom openstack
import pprint
import eventlet

try:
    from nova.openstack.common import rpc
except Exception:
    print 'The script is only for folsom openstack'
    exit()

logfile = 'log.txt'

def print_msg(message):
#    pprint.pprint(message)
    pprint.pprint(message.keys())
    pprint.pprint(message['method'])
    print '-'*50


class MsgHandler(object):
    '''
    The Message keys

        [u'_context_roles',
        u'_context_request_id',
        u'_context_quota_class',
        u'_context_instance_lock_checked',
        u'_context_project_name',
        u'_context_service_catalog',
        u'args',
        u'method',
        u'_context_auth_token',
        u'_context_is_admin',
        u'version',
        u'_context_project_id',
        u'_context_timestamp',
        u'_context_read_deleted',
        u'_context_user_id',
        u'_context_user_name',
        u'_context_remote_address']

    The notifications Message Example:

        {'message_id': str(uuid.uuid4()),
        'publisher_id': 'compute.host1',
        'timestamp': timeutils.utcnow(),
        'priority': 'WARN',
        'event_type': 'compute.create_instance',
        'payload': {'instance_id': 12, ... }}
    '''

    def __init__(self, name, notify=False):
        self.name = name
        self.notify = notify

    def __call__(self, message):
        def _print(key):
            value = message.get(key, None)
            print '%s: %s' % (key, value)

        print self.name.center(50)
        if self.notify:
            try:
                _print('message_id')
                _print('publisher_id')
                _print('event_type')
                _print('payload')
                _print('_context_request_id')
                _print('_context_remote_address')
                _print('timestamp')
            except Exception:
                pass
            finally:
                print '-'*50
        else:
            try:
                _print('method')
                _print('args')
                _print('_context_request_id')
                _print('_context_remote_address')
                _print('_context_timestamp')
            except Exception:
                pass
            finally:
                print '-'*50


def loopwait():
    while True:
        eventlet.sleep(1)

def main():
    conn = rpc.create_connection(new=True)

    topics = ['compute', 'compute.*',
              'network', 'network.*',
              'scheduler']
    for topic in topics:
        conn.declare_topic_consumer(topic=topic, callback=MsgHandler(topic),
                                    queue_name='%s_backdoor' % topic)

    topic = 'notifications.*'
    conn.declare_topic_consumer(topic=topic, callback=MsgHandler(topic, True),
                                queue_name='%s_backdoor' % topic)
    conn.consume_in_thread()
    eventlet.spawn(loopwait).wait()


if __name__ == '__main__':
    main()
