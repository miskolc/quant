import numpy as np
import json
from datetime import date, datetime

class JSONEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        return obj.__dict__
