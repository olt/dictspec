class required(str):
    pass

class anything(object):
    def compare_type(self, data):
        return True

class recursive(object):
    def __init__(self, spec=None):
        self.spec = spec
    def compare_type(self, data):
        return isinstance(data, type(self.spec))

class one_off(object):
    def __init__(self, *specs):
        self.specs = specs

class number(object):
    def compare_type(self, data):
        return isinstance(data, (float, int, long))

class type_spec(object):
    def __init__(self, type_key, specs):
        self.type_key = type_key
        self.specs = specs
        
        for v in specs.itervalues():
            if not isinstance(v, dict):
                raise ValueError('%s requires dict subspecs', self.__class__)
            if self.type_key not in v:
                v[self.type_key] = str()
    
    def subspec(self, data):
        key = data[self.type_key]
        return self.specs[key]