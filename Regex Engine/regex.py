def main():
    regex, string = input().strip().split("|")
    return eval_regex(regex, string)


def eval_regex(regex, string):
    if len(regex) == 0:
        return True

    if regex[0] == '^':
        if not is_equal(regex[1], string[0]):
            return False
        regex = regex[1:]

    for i in range(len(string)):
        is_match = match_regex(regex, string[i:])
        if is_match or regex[0] == '^':
            return is_match
    return False


def match_regex(regex, string, regex_i=0, string_i=0):
    # escape character
    escape = False
    if regex_i in range(len(regex)) and regex[regex_i] == '\\':
        escape = True
        regex_i += 1

    if regex_i+1 < len(regex) and not escape:
        if regex[regex_i+1] == '?':
            # ? = match 0 or once
            if is_equal(regex[regex_i], string[string_i]):
                string_i += 1
            regex_i += 2

        elif regex[regex_i+1] in '*+':
            # * = match 0 or inf
            # + = match once or inf
            char_after_mc = None
            for char in regex[regex_i + 1:]:
                if char not in '*$+?':
                    char_after_mc = char
                    break

            if regex[regex_i+1] == '+' and not is_equal(regex[regex_i], string[string_i]):
                return False

            while string_i < len(string) and is_equal(regex[regex_i], string[string_i]):
                break_loop = True
                if char_after_mc and is_equal(string[string_i], char_after_mc):
                    if string_i+1 < len(string) and is_equal(string[string_i+1], char_after_mc):
                        break_loop = False
                    if break_loop:
                        break
                string_i += 1
            regex_i += 2

    # Regex is consumed
    if regex_i == len(regex):
        return True

    if regex[regex_i] == '$' and not escape:
        if string_i == len(string):
            return True
        else:
            return False

    if not is_equal(regex[regex_i], string[string_i], escape):
        return False

    return match_regex(regex, string, regex_i+1, string_i+1)


def is_equal(regex_char, string_char, escape=False):
    if escape:
        if regex_char == string_char:
            return True
    else:
        if regex_char == '.' or regex_char == string_char:
            return True
    return False


if __name__ == '__main__':
    print(main())
