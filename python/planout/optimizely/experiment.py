import time
import random
import json
import logging
from planout.experiment import DefaultExperiment
from planout.experiment import SimpleInterpretedExperiment
from ops.random import OptimizelyWeightedChoice
from planout import optimizely
from handler import QueueHandler
from planout.optimizely.model import Experiment
import threading


class OptimizelyExperiment(DefaultExperiment):
    BUCKETING_SEED = 1
    logger = {}

    def __init__(self, experiment_id, **inputs):
        self.experiment_id = experiment_id
        self.has_ppid = 'user_id' in inputs
        if 'user_id' not in inputs or inputs['user_id'] is None:
            self.user_id = 'oeu%sr%s' % (str(int(time.time() * 1000)), str(random.random()))
        else:
            self.user_id = inputs['user_id']
        self.experiment = Experiment(experiment_id)
        self.choices, self.weights = self.experiment.get_enabled_variation_ids_and_weights()
        self.logger_name = str(self.experiment.project_id)
        inputs.update({'experiment_id': experiment_id, 'user_id': self.user_id})
        super(OptimizelyExperiment, self).__init__(**inputs)

    def setup(self):
        self._in_experiment = False
        self.salt = str(self.experiment_id)
        self.name = self.experiment.get('name', self.__class__.__name__)

    def __asBlob(self, extras={}):
        d = {
            'name': self.name,
            'time': int(time.time()),
            'salt': self.salt,
            'inputs': self.inputs,
            'params': dict(self._assignment),
        }
        for k in extras:
            d[k] = extras[k]
        if self._checksum:
            d['checksum'] = self._checksum
        if 'event' in d:
            optimizely_log_event = {
                'a': str(self.experiment.project_id),
                'n': extras.get('event'),
                'u': self.user_id,
                'x'+str(self.experiment_id): str(self._assignment.get('_variation_id')),
            }
            if self.has_ppid:
                optimizely_log_event.update({
                    'p': self.user_id
                })
            if 'extra_data' in extras and 'revenue' in extras['extra_data']:
                optimizely_log_event.update({
                    'v': str(extras['extra_data']['revenue'])
                })
            if 'extra_data' in extras and 'goal_id' in extras['extra_data']:
                optimizely_log_event.update({
                    'g': str(extras['extra_data']['goal_id'])
                })
            d.update({
                'optimizely_log_event': optimizely_log_event,
            })
        return d

    def configure_logger(self):

        my_logger = self.__class__.logger
        # only want to set logging handler once for each project (id)
        if self.logger_name not in self.__class__.logger:
            my_logger[self.logger_name] = logging.getLogger(self.name)
            my_logger[self.logger_name].setLevel(logging.INFO)
            my_logger[self.logger_name].propogate = False
            q = optimizely.project.get('log_event_queue')
            if q is not None:
                my_logger[self.logger_name].addHandler(QueueHandler(q))
            my_logger[self.logger_name].propagate = True

    def log_event(self, event_type, extras=None):
        """Log an arbitrary event"""
        if not self._in_experiment:
            return
        if extras:
            extra_payload = {'event': event_type, 'extra_data': extras.copy()}
        else:
            extra_payload = {'event': event_type}
        self.log(self.__asBlob(extra_payload))

    def log(self, data):
        """Logs data to a file"""
        self.__class__.logger[self.logger_name].info(json.dumps(data))

    def assign(self, params, **kwargs):
        if not self.experiment.get('enabled', False) and not self.weights:
            return

        params._variation_id = OptimizelyWeightedChoice(choices=self.choices, weights=self.weights,
                                                        experiment_id=self.experiment_id, unit=self.user_id,
                                                        salt=OptimizelyExperiment.BUCKETING_SEED)
        if not params._variation_id:
            return
        params._variation_data = self.experiment.get_variation_data(params._variation_id)
        if params._variation_data and 'planout_script' in params._variation_data:
            params.update(OptimizelyVariationExperiment(params._variation_data.get('planout_script'),
                                                        **self.inputs).get_params())
            self._in_experiment = True


class OptimizelyVariationExperiment(SimpleInterpretedExperiment):
    def __init__(self, planout_script, **inputs):
        super(OptimizelyVariationExperiment, self).__init__(**inputs)
        self.script = json.loads(planout_script)

    def setup(self):
        self._in_experiment = False
        self.set_auto_exposure_logging(False)