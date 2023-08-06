def to_title_case(string):
    title_case_string = ""
    capitalize_next_char = True
    for char in string:
        if capitalize_next_char and char.isalpha():
            title_case_string += char.upper()
            capitalize_next_char = False
        else:
            title_case_string += char.lower()
            if char in [' ', '-', '_', '.']:
                capitalize_next_char = True
    return title_case_string

def to_lower_case(string):
    lower_case_string = ""
    for char in string:
        if char.isalpha():
            lower_case_string += chr(ord(char) | 32)
        else:
            lower_case_string += char
    return lower_case_string

def to_upper_case(string):
    upper_case_string = ""
    for char in string:
        if char.isalpha():
            upper_case_string += chr(ord(char) & ~32)
        else:
            upper_case_string += char
    return upper_case_string
