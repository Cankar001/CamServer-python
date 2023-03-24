import datetime

def generate(basename):
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    return '_'.join([basename, suffix])

