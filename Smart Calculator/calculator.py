from collections import deque
import operator

operator_priority = {
        '+': 0,
        '-': 0,
        '*': 1,
        '/': 2,
        '^': 3,
    }

operator_map = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv,
    '^': operator.pow
}


def main():
    var_dict = {}
    while True:
        user_in = input()

        if len(user_in) == 0:
            continue
        elif user_in == '/help':
            print("The program calculates expression passed as string")
        elif user_in == '/exit':
            print("Bye!")
            exit()
        elif user_in[0] == '/':
            print("Unknown command")
        elif '=' in user_in:
            try:
                key, val = eval_assignment(user_in, var_dict)
                var_dict[key] = val
            except InvalidUserInputError as e:
                print(e)
        else:
            try:
                postfix_list = to_postfix(user_in)
            except InvalidUserInputError as e:
                print(e)
                continue

            try:
                print(calculate_from_postfix(postfix_list, var_dict))
            except InvalidUserInputError as e:
                print(e)


def to_postfix(user_in: str):
    user_in = user_in.replace(" ", "")
    operator_stack = deque()
    postfix_list = []
    was_num = False
    was_op = False

    if user_in[0] == '-':
        was_num = True
        postfix_list.append(user_in[0])
        user_in = user_in[1:]
    for index, char in enumerate(user_in):
        if char.isalnum():
            if was_num:
                postfix_list[-1] += char
            else:
                postfix_list.append(char)
            was_num = True
            was_op = False
        else:
            if char == "(":
                operator_stack.append(char)
            elif char == ")":
                try:
                    top = operator_stack.pop()
                    while top != "(":
                        postfix_list.append(top)
                        top = operator_stack.pop()
                except IndexError:
                    raise InvalidUserInputError("Invalid expression")
            else:
                top = peek(operator_stack)
                if was_op:
                    operator_stack.pop()
                    if top == '-':
                        top = '+' if char == '-' else '-'
                        operator_stack.append(top)
                    elif top == '+':
                        operator_stack.append(char)
                    else:
                        raise InvalidUserInputError("Invalid expression")

                elif top is None or top == "(":
                    operator_stack.append(char)
                else:
                    while len(operator_stack) > 0 and top != "(" and operator_priority[char] <= operator_priority[top]:
                        top = operator_stack.pop()
                        postfix_list.append(top)
                    operator_stack.append(char)
            was_op = True
            was_num = False

    while len(operator_stack) > 0:
        top = operator_stack.pop()
        if top in "()":
            raise InvalidUserInputError("Invalid expression")
        postfix_list.append(top)
    return postfix_list


def peek(stack: deque):
    try:
        top = stack.pop()
        stack.append(top)
    except IndexError:
        top = None
    return top


def calculate_from_postfix(postfix_list: list, variable_dict: dict):
    result_stack = deque()
    for elem in postfix_list:
        if elem.isnumeric():
            result_stack.append(int(elem))
        elif elem.isalpha():
            try:
                result_stack.append(int(variable_dict[elem]))
            except KeyError:
                raise InvalidUserInputError("Unknown variable")
        elif elem in operator_map:
            num2 = result_stack.pop()
            num1 = result_stack.pop()
            result_stack.append(operator_map[elem](num1, num2))
        else:
            try:
                result_stack.append(int(elem))
            except TypeError:
                pass
            raise InvalidUserInputError("Invalid identifier")
    return result_stack.pop()


def eval_assignment(user_assignment, variable_dict):
    user_assignment = user_assignment.replace(" ", "")
    key, value, *extra = user_assignment.split("=")

    if not key.isalpha():
        raise InvalidUserInputError("Invalid identifier")

    try:
        value = int(value)
    except ValueError:
        if not value.isalpha():
            raise InvalidUserInputError("Invalid assignment")
        try:
            value = variable_dict[value]
        except KeyError:
            raise InvalidUserInputError("Unknown variable")

    if len(extra) > 0:
        raise InvalidUserInputError("Invalid assignment")

    return key, value


class InvalidUserInputError(Exception):
    pass


if __name__ == '__main__':
    main()
