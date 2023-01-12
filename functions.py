


class Log:
    def __init__(self, *args, **kwargs):
        if len(args) == 5:
            self.id = args[0]
            self.user_id = args[1]
            self.user = args[2]
            self.date_time = args[3]
            self.msg_text = args[4]

        elif len(args) == 1:
            self.__init__(args[0][0], args[0][1], args[0][2], args[0][3],  args[0][4])
        else:
            raise TypeError("wrong number of args")


    def __repr__(self):
        return str(self.id) + ' ' + self.date_time + ' ' + str(self.user_id) + ' ' + self.user + ' ' + self.msg_text


    def __str__(self):
        return str(self.id) + ';' + str(self.user_id) + ';' + self.user + ';' + str(self.date_time) + ';' + \
               str(self.msg_text)


def check_if_number(text):
    if text.isdigit():
        result = [True,'int_typ', text]
    elif text.count('.') == 1 and text.replace('.', '').isdigit():
        result = [True, 'float_typ', text]
    elif text[-1] == 'j' and text[:-1].replace('+', '').replace('.', '').isdigit():
        string = text[:-1].split('+')
        if len(string) == 1:
            if string[0].count('.') <= 1:
                r = 0
                i = string[0]
                result = [True,'complex_typ', r, i]
            else:
                result = [False]
        else:
            if string[0].count('.') <= 1 and string[1].count('.') <= 1:
                r = string[0]
                i = string[1]
                result = [True,'complex_typ', r, i]
    elif text[-1] == 'j' and text[:-1].replace('-', '').isdigit():
        string = text[:-1].split('-')
        if len(string) == 1:
            if string[0].count('.') <= 1:
                r = 0
                i = string[0]
                result = [True,'complex_typ', r, i]
            else:
                result = [False]
        else:
            if string[0].count('.') <= 1 and string[1].count('.'):
                r = string[0]
                i = string[1]
                result = [True,'complex_typ', r, i]
    else:
        result = [False]
    return result

def number_res(result):
    if result[1] == 'int_typ':
        number = int(result[2])
    elif result[1] == 'float_typ':
        number = float(result[2])
    elif result[1] == 'complex_typ':
        number = complex(float(result[2]), float(result[3]))
    return number

def check_action(text):
    result = [False]
    if text in '+ - * : **'.split():
        if text == '+':
            oper = sum
        elif text == '-':
            oper = minus
        elif text == '*':
            oper = mult
        elif text == ':':
            oper = div
        elif text == '**':
            oper = pwr
        result = [True, oper]
    return result


def sum(x, y):
    xn, yn = change_type(x, y)
    return xn + yn


def minus(x, y):
    xn, yn = change_type(x, y)
    return xn - yn


def mult(x, y):
    return x[1] * y[1]


def div(x, y):
    if x[0] == 'int_typ' and x[0] == 'int_typ':
        if x[1] % y[1] != 0:
            x[1] = float(x[1])
            y[1] = float(y[1])
    return x[1] / y[1]


def pwr(x, y):
    return x[1] ** y[1]


def log_save(arr):
    with open(f'log.csv', 'w', encoding='utf-8') as file:
        for text in arr:
            res_text = str(text)
            file.writelines(f'{res_text}; \n')


def calc_result(id_, dc, result):
    x, y = dc[id_][0], dc[id_][1]
    return result(x, y)


def change_type(x, y):
    if (x[0] != 'int_typ'and y[0] != 'int_typ') or (x[0] == 'int_typ'and y[0] == 'int_typ'):
        xn, yn = x[1], y[1]
    elif x[0] != 'int_typ'and y[0] == 'int_typ':
        xn, yn = x[1], float(y[1])
    elif x[0] == 'int_typ'and y[0] != 'int_typ':
        xn, yn = float(x[1]), y[1]
    return xn, yn