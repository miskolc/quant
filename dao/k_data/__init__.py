
def fill_market(code):

    if code.startswith("6"):
        return 'SH.'+ code

    elif code.startswith("0") or code.startswith("3"):
        return 'SZ.' + code

    else:
        return code