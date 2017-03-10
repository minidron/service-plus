def format_price(value):
    if not value:
        value = 0
    elif isinstance(value, str):
        value = int(float(value))
    return '%s р.' % '{0:,}'.format(value).replace(',', ' ')
