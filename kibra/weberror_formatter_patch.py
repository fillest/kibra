"""
    this ugly hack fixes https://bitbucket.org/bbangert/weberror/issue/7/error-while-logging-to-wsgierrors-under
"""


import weberror.formatter


# see https://bitbucket.org/bbangert/weberror/src/35ecbdd750ad/weberror/formatter.py#cl-253
def _hacked_format_combine(self, data_by_importance, lines, exc_info):
    lines[:0] = [value for n, value in data_by_importance['important']]
    lines.append(exc_info)
    for name in 'normal', 'supplemental', 'extra':
        lines.extend([value for n, value in data_by_importance[name]])
    return self.format_combine_lines(lines)

def patch_lib ():
    weberror.formatter.TextFormatter.format_combine = _hacked_format_combine