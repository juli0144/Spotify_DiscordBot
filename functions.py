

def int_or_5(arg):
    try:
        return int(arg)
    except ValueError:
        return 5


def custom_input_numeric(prompt):
    custom_inp = ''
    while custom_inp == '':
        a_input = input(prompt)
        custom_inp = a_input if a_input.isnumeric() else ''
    return custom_inp