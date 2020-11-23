def not_supported() -> None:
    from inspect import stack

    print('Function "%s" is not supported for this client.' % stack()[1][3])
