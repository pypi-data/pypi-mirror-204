def populate(num, pos):
    if pos == 1:
        return [num]
    if pos == 0:
        return [num]
    zero = [(num<<pos)|i for i in populate(0, pos-2)]
    one = [(num<<pos)|i for i in populate(1, pos-2)]
    two = [(num<<pos)|i for i in populate(2, pos-2)]
    three = [(num<<pos)|i for i in populate(3, pos-2)]
    
    return zero + one + two + three