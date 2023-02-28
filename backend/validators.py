def make_error(code, text):
    return {
        "code": code,
        "text": text
    }


def get_errors(data, fields):
    errors = []

    for field in fields:
        code = field['code']
        title = field['title']

        # required
        if field['is_required'] and code not in data:
            errors.append(make_error(code, f"Заполните поле {title}"))
            continue

        if not field['is_required'] and code not in data:
            continue

        # datatype
        if field["type"] == "int":
            try:
                data[code] = int(data[code])
            except:
                errors.append(make_error(code, f"Значение {title} должно быть целым числом"))
                continue

        elif field["type"] == "float":
            try:
                data[code] = float(data[code])
            except:
                errors.append(make_error(code, f"Значение {title} должно быть числом"))
                continue

        elif field["type"] == "radio" or field["type"] == "select":
            print(field)
            options = list(map(lambda variant: variant['value'], field['options']))

            if data[code] not in options:
                errors.append(make_error(code, f"Недопустимое значение {title}"))
                continue

        value = data[code]

        # limits
        if "limits" in field:
            for rule in field["limits"]:
                if rule["type"] == "max":
                    if value > rule['value']:
                        errors.append(make_error(code, f"Значение {title} должно быть меньше {rule['value']}"))
                        continue
                if rule["type"] == "min":
                    if value < rule['value']:
                        errors.append(make_error(code, f"Значение {title} должно быть больше {rule['value']}"))
                        continue

    return errors
