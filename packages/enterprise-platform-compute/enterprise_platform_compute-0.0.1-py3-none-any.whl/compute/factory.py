import base64

import cloudpickle


class Factory:
    def __init__(self, method):
        self.method = method

    def serialize(self):
        """
        Use cloudpickle to serialize the function so that it can be
        transferred to the compute platform via the public api.
        """
        if self.method is None:
            return None

        return base64.b64encode(cloudpickle.dumps(self.method)).decode("utf-8")
