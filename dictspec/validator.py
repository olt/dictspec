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

def validate(spec, data, context=None):
    if context is None:
        context = Context()
    
    if hasattr(spec, 'subspec'):
        spec = spec.subspec(data)
    
    # store spec for recursive specs in context
    if isinstance(spec, recursive):
        if not context.recurse_spec:
            context.recurse_spec = spec.spec
        spec = context.recurse_spec
    
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
            raise ValueError("'%s' in %s not of any type %r" % (data, context.current_pos, map(type, spec.specs)))
    elif hasattr(spec, 'compare_type'):
        if not spec.compare_type(data):
            raise ValueError("'%s' in %s not of type %s" % (data, context.current_pos, type(spec)))
    elif not isinstance(data, type(spec)):
        raise ValueError("'%s' in %s not of type %s" % (data, context.current_pos, type(spec)))
    
    # recurse in dicts and lists
    if isinstance(spec, dict):
        validate_dict(spec, data, context)
    elif isinstance(spec, list):
        validate_list(spec, data, context)

def validate_dict(spec, data, context):
    accept_any_key = False
    any_key_spec = None
    for k in spec.iterkeys():
        if isinstance(k, required):
            if k not in data:
                raise ValueError("missing '%s' not in %s" % (k, context.current_pos))
        if isinstance(k, anything):
            accept_any_key = True
            any_key_spec = spec[k]

    for k, v in data.iteritems():
        if accept_any_key:
            with context.pos('.' + k):
                validate(any_key_spec, v, context)

        else:
            if k not in spec:
                raise ValueError("unknown '%s' in %s" % (k, context.current_pos))
            with context.pos('.' + k):
                validate(spec[k], v, context)

def validate_list(spec, data, context):
    assert len(spec) == 1
    for i, v in enumerate(data):
        with context.pos('[%d]' % i):
            validate(spec[0], v, context)
        