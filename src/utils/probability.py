import random

def chance(p):
    """
    Возвращает True с вероятностью p.
    """
    return random.random() < p

def weighted_choice(items):
    """
    items = [(obj, weight), ...]
    """
    total = sum(w for _, w in items)
    r = random.uniform(0, total)
    upto = 0
    for obj, weight in items:
        if upto + weight >= r:
            return obj
        upto += weight