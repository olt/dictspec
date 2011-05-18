from dictspec.spec import required, one_off, anything, recursive
from contextlib import contextmanager

class Context(object):
    def __init__(self):
        self.recurse_spec = None
        self.obj_pos = []
    
    def push(self, spec):
        self.obj_pos.append(spec)
    
    def pop(self):
        return self.obj_pos.pop()
    
    @contextmanager
    def pos(self, spec):
        self.push(spec)
        yield
        self.pop()
    
    @property
    def current_pos(self):
        return ''.join(self.obj_pos).lstrip('.')


def validate(spec, data):
    return Validator(spec).validate(data)

class Validator(object):
    def __init__(self, spec):
        self.context = Context()
        self.complete_spec = spec
    
    def validate(self, data):
        return self._validate_part(self.complete_spec, data)

    def _validate_part(self, spec, data):
        if hasattr(spec, 'subspec'):
            spec = spec.subspec(data)
    
        # store spec for recursive specs in context
        if isinstance(spec, recursive):
            if not self.context.recurse_spec:
                self.context.recurse_spec = spec.spec
            spec = self.context.recurse_spec
    
        if isinstance(spec, anything):
            return
    
        if isinstance(spec, one_off):
            # check if at least one spec type matches
            for subspec in spec.specs:
                if (hasattr(subspec, 'compare_type') and subspec.compare_type(data)
                    or isinstance(data, type(subspec))):
                    spec = subspec
                    break
            else:
                raise ValueError("'%s' in %s not of any type %r" % (data, self.context.current_pos, map(type, spec.specs)))
        elif hasattr(spec, 'compare_type'):
            if not spec.compare_type(data):
                raise ValueError("'%s' in %s not of type %s" % (data, self.context.current_pos, type(spec)))
        elif not isinstance(data, type(spec)):
            raise ValueError("'%s' in %s not of type %s" % (data, self.context.current_pos, type(spec)))
    
        # recurse in dicts and lists
        if isinstance(spec, dict):
            self._validate_dict(spec, data)
        elif isinstance(spec, list):
            self._validate_list(spec, data)

    def _validate_dict(self, spec, data):
        accept_any_key = False
        any_key_spec = None
        for k in spec.iterkeys():
            if isinstance(k, required):
                if k not in data:
                    raise ValueError("missing '%s' not in %s" % (k, self.context.current_pos))
            if isinstance(k, anything):
                accept_any_key = True
                any_key_spec = spec[k]

        for k, v in data.iteritems():
            if accept_any_key:
                with self.context.pos('.' + k):
                    self._validate_part(any_key_spec, v)

            else:
                if k not in spec:
                    raise ValueError("unknown '%s' in %s" % (k, self.context.current_pos))
                with self.context.pos('.' + k):
                    self._validate_part(spec[k], v)

    def _validate_list(self, spec, data):
        assert len(spec) == 1
        for i, v in enumerate(data):
            with self.context.pos('[%d]' % i):
                self._validate_part(spec[0], v)
        