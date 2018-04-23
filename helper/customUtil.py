"""
trans mysql data to string
"""
def date2Json(data):
    import datetime
    if isinstance(data, list):
        for i, row in enumerate(data):
            for key,val in row.items():
                if isinstance(val, datetime.datetime):
                    data[i][key] = val.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(val, datetime.date):
                    data[i][key] = val.strftime('%Y-%m-%d')
    else:
        for key,val in data.items():
            if isinstance(val, datetime) or isinstance(val, datetime.date):
                data[key] = str(val)
    return data