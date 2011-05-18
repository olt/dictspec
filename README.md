dictspec – Validator for JSON/YAML/dicts
========================================

dictspec is a simple Python library that validates dictionary and list based data structures.
You can use it to validate JSON/YAML documents against your own specification.

Examples
--------

Validate against plain Python data types:

    >>> spec = {
    ...   'foo': 1,
    ...   'bar': [str()],
    ... }
    >>> data = {
    ...   'foo': 4,
    ...   'bar': ['hello', 'world']}
    ... }
    >>> from dictspec.validator import validate
    >>> validate(spec, data)


Use more complex specs and get detailed errors:

    >>> from dictspec.spec import number, required
    >>> spec = {
    ...   required('foo'): number(),
    ...   'bar': bool(),
    ... }
    >>> data = {
    ...                 # missing 'foo' key
    ...   'bar': 4,     # wrong type
    ...   'baz': True,  # unknown key
    ... }
  
    >>> from dictspec.validator import ValidationError
    >>> try:
    ...   validate(spec, data)
    ... except ValidationError, ex:
    ...   print ex.errors
    ["missing 'foo' not in .", "unknown 'baz' in .", "4 in bar not of type <type 'bool'>"]


Also with recursion and arbitrary keys:

    >>> from dictspec.spec import anything, recursive
    >>> spec = {
    ...   'hello': recursive({
    ...     anything(): recursive(),
    ...   })
    ... }
    >>> data = {
    ...   'hello': {'any': {'thing': {'recursive':{}}}}
    ... }
    >>> validate(spec, data)
  