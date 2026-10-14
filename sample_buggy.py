def process_data(data):
    result = []
    for item in data:
        if item.active:
            result.append(transform(item))
    return result

def calculate_total(prices):
    total = 0
    for p in prices:
        total = total + p
    return total

def get_user(id):
    if id == None:
        return None
    return database.fetch(id)
