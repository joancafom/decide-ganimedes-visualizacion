
def check_str_is_int(string):

    try:
        int(string)

        return True

    except ValueError:
        return False

