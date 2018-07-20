

class Profit:
    def __init__(self, date_time, value):
        self.date_time = date_time
        self.value = value


    def __repr__(self):
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])
