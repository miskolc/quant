
def fill_market(code):

    if code.startswith('SH'):
        return code

    if code.startswith('SZ'):
        return code

    elif code.startswith("6"):
        return 'SH.'+ code

    elif code.startswith("0") or code.startswith("3"):
        return 'SZ.' + code

    else:
        return code