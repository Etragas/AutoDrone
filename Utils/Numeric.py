def is_num(candidate):
    try:
        val = float(candidate)
        return True
    except:
        return False