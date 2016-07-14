# Copyright (c) 2011, Oliver Tonnhofer <olt@omniscale.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
PY2 = sys.version_info[0] == 2
PY3 = not PY2

if PY2:
    numeric_types = (float, int, long)
    string_type = basestring
    text_type = unicode
    # unichr = chr
else:
    numeric_types = (float, int)
    string_type = str
    text_type = str
    # unichr = unichr

if PY2:
    def iteritems(d):
        return d.iteritems()

    def iterkeys(d):
        return d.iterkeys()

    def itervalues(d):
        return d.itervalues()
else:
    def iteritems(d):
        return d.items()

    def iterkeys(d):
        return iter(d.keys())

    def itervalues(d):
        return d.values()
