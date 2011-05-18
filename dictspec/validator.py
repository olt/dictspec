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

class ValidationError(TypeError):
    def __init__(self, msg, errors=None):
        TypeError.__init__(self, msg)
        self.errors = errors or []

class Validator(object):
    def __init__(self, spec, fail_fast=False):
        """
        :params fail_fast: True if it should raise on the first error
        """
        self.context = Context()
        self.complete_spec = spec
        self.raise_first_error = fail_fast
        self.errors = []
        
    def validate(self, data):
        self._validate_part(self.complete_spec, data)
        
        if self.errors:
            if len(self.errors) == 1:
                raise ValidationError(self.errors[0])
            else:
                raise ValidationError('found %d validation errors.' % len(self.errors), self.errors)
            

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
                return self._handle_error("'%s' in %s not of any type %r" %
                    (data, self.context.current_pos, map(type, spec.specs)))
        elif hasattr(spec, 'compare_type'):
            if not spec.compare_type(data):
                return self._handle_error("'%s' in %s not of type %s" %
                    (data, self.context.current_pos, type(spec)))
        elif not isinstance(data, type(spec)):
            return self._handle_error("'%s' in %s not of type %s" %
                (data, self.context.current_pos, type(spec)))
    
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
                    self._handle_error("missing '%s' not in %s" %
                        (k, self.context.current_pos))
            if isinstance(k, anything):
                accept_any_key = True
                any_key_spec = spec[k]

        for k, v in data.iteritems():
            if accept_any_key:
                with self.context.pos('.' + k):
                    self._validate_part(any_key_spec, v)

            else:
                if k not in spec:
                    self._handle_error("unknown '%s' in %s" %
                        (k, self.context.current_pos))
                    continue
                with self.context.pos('.' + k):
                    self._validate_part(spec[k], v)

    def _validate_list(self, spec, data):
        assert len(spec) == 1
        for i, v in enumerate(data):
            with self.context.pos('[%d]' % i):
                self._validate_part(spec[0], v)
    
    def _handle_error(self, msg):
        if self.raise_first_error:
            raise ValidationError(msg)
        self.errors.append(msg)
        