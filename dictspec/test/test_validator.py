from dictspec.validator import validate
from dictspec.spec import required, one_off, number, recursive, type_spec

from nose.tools import raises

class TestSimpleDict(object):
    def test_validate_simple_dict(self):
        spec = {'hello': 1, 'world': True}
        validate(spec, {'hello': 34, 'world': False})

    @raises(ValueError)
    def test_invalid_key(self):
        spec = {'world': True}
        validate(spec, {'world_foo': False})

    def test_empty_data(self):
        spec = {'world': 1}
        validate(spec, {})

    @raises(ValueError)
    def test_invalid_value(self):
        spec = {'world': 1}
        validate(spec, {'world_foo': False})

    @raises(ValueError)
    def test_missing_required_key(self):
        spec = {required('world'): 1}
        validate(spec, {})
    
    def test_valid_one_off(self):
        spec = {'hello': one_off(1, bool())}
        validate(spec, {'hello': 129})
        validate(spec, {'hello': True})
    
    @raises(ValueError)
    def test_invalid_one_off(self):
        spec = {'hello': one_off(1, False)}
        validate(spec, {'hello': []})

class TestLists(object):
    def test_list(self):
        spec = [1]
        validate(spec, [1, 2, 3, 4, -9])

    def test_empty_list(self):
        spec = [1]
        validate(spec, [])
    
    @raises(ValueError)
    def test_invalid_item(self):
        spec = [1]
        validate(spec, [1, 'hello'])

class TestNumber(object):
    def check_valid(self, spec, data):
        validate(spec, data)
    
    def test_numbers(self):
        spec = number()
        for i in (0, 1, 23e999, int(10e20), 23.1, -0.0000000001):
            yield self.check_valid, spec, i

class TestNested(object):
    def check_valid(self, spec, data):
        validate(spec, data)
    
    @raises(ValueError)
    def check_invalid(self, spec, data):
        validate(spec, data)
        
    def test_dict(self):
        spec = {
            'globals': {
                'image': {
                    'format': {
                        'png': {
                            'mode': 'RGB',
                        }
                    },
                },
                'cache': {
                    'base_dir': '/path/to/foo'
                }
            }
        }
        
        yield self.check_valid, spec, {'globals': {'image': {'format': {'png': {'mode': 'P'}}}}}
        yield self.check_valid, spec, {'globals': {'image': {'format': {'png': {'mode': 'P'}}},
                                                   'cache': {'base_dir': '/somewhere'}}}
        yield self.check_invalid, spec, {'globals': {'image': {'foo': {'png': {'mode': 'P'}}}}}
        yield self.check_invalid, spec, {'globals': {'image': {'png': {'png': {'mode': 1}}}}}

class TestRecursive(object):
    def test(self):
        spec = recursive({'hello': str(), 'more': recursive()})
        validate(spec, {'hello': 'world', 'more': {'hello': 'foo', 'more': {'more': {}}}})

class TestTypeSpec(object):
    def test(self):
        spec = type_spec('type', {'foo': {'alpha': str()}, 'bar': {'one': 1, 'two': str()}})
        validate(spec, {'type': 'foo', 'alpha': 'yes'})
        validate(spec, {'type': 'bar', 'one': 2})

class TestErrors(object):
    def test_invalid_key(self):
        spec = {'world': {'europe': {}}}
        try:
            validate(spec, {'world': {'europe': {'germany': 1}}})
        except ValueError, ex:
            assert 'world.europe' in str(ex)
        else:
            assert False
    
    def test_invalid_list_item(self):
        spec = {'numbers': [number()]}
        try:
            validate(spec, {'numbers': [1, 2, 3, 'foo']})
        except ValueError, ex:
            assert 'numbers[3]' in str(ex), str(ex)
        else:
            assert False
