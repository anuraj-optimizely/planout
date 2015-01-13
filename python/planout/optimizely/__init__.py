import urllib2
from urllib2 import URLError
import json
import logging
import Queue
import threading
import time
from handler import QueueListener
from handler import LogEventHttpHandler

project = {
    'id': None,
    'data': {},
    'sync_project_data_thread': None,
    'log_event_queue': None,
    'init': False,
    'log_event_queue_listener': None
}
SYNC_PROJECT_FREQUENCY = 1  # seconds


def init(project_id):
    global project
    if project['init']:
        return
    project['init'] = 'in_progress'
    project['id'] = project_id
    update_project_data()
    t = threading.Thread(target=sync_project_data)
    t.setDaemon(True)
    t.start()
    project['sync_project_data_thread'] = t
    q = Queue.Queue()
    project['log_event_queue'] = q
    project['log_event_queue_listener'] = QueueListener(q,
                                                        LogEventHttpHandler(host=
                                                                            str(project_id)+'.log.optimizely.com',
                                                                            url='/event')).start()
    project['init'] = True


def sync_project_data():
    while True:
        update_project_data()
        time.sleep(SYNC_PROJECT_FREQUENCY)

def update_project_data():
    global project
    req = urllib2.Request('http://cdn.optimizely.com/json/server/%s.json' % str(project.get('id')))
    resp = None
    try:
        resp = urllib2.urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            logging.error('Failed to reach a server, reason: %s' % e.reason, e)
        elif hasattr(e, 'code'):
            logging.error('Server couldn\'t fulfill the request, error code: %s' % str(e.code), e)
        else:
            logging.error('Error making request', e)

    if resp is not None:
        try:
            project['data'] = json.loads(resp.read())
            logging.debug('Updated project_data for project_id: ' + str(project.get('id')))
        except ValueError as e:
            logging.error('Invalid json payload in response', e)
