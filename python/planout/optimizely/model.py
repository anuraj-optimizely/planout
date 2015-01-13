from planout import optimizely


class Experiment(object):
    def __init__(self, experiment_id):
        self.id = experiment_id
        self.project_id = optimizely.project['id']
        self._project_data = optimizely.project['data'].copy()
        self._experiment_data = self._project_data.get('experiments', {}).get(str(experiment_id), {})

    @property
    def project_data(self):
        return self._project_data

    def get(self, key, default_val):
        return self._experiment_data.get(key, default_val)

    def get_variation_data(self, variation_id):
        return self._project_data['variations'].get(str(variation_id), {})

    def get_enabled_variation_ids_and_weights(self):
        enabled_variation_ids = self.get('enabled_variation_ids', [])
        enabled_variation_weights = [self.get('variation_weights', {}).get(enabled_variation_id)
                                     for enabled_variation_id in enabled_variation_ids]

        return enabled_variation_ids, enabled_variation_weights