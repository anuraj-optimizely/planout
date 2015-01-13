from planout import optimizely
from planout.optimizely.experiment import OptimizelyExperiment

optimizely.init(44036)

ope = OptimizelyExperiment(5550970352173056, user_id='anuraj')
print ope.get('a')
print ope.get_params()

#print optimizely.project['log_event_queue'].qsize()

#while optimizely.project['log_event_queue'].qsize() > 0:
#    print 'wait', optimizely.project['log_event_queue'].qsize()

#from planout.optimizely.handler import LogEventHttpHandler

#import json


#LogEventHttpHandler(host='1906270004.log.optimizely.com', url='/event').handle(
#  json.dumps(ope.log_event(event_type='engagement', extras={'revenue': 5*100})))



