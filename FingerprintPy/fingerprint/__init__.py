
class Keystroke:
    def __init__(self):
        pass

def identify(keystroke_stream):
    features = extract_features(keystroke_stream)
    return features

def extract_features(keystroke_stream):
    down_up_average = get_down_up_average(keystroke_stream)
    up_down_average = get_up_down_average(keystroke_stream)
    down_down_average = get_down_down_average(keystroke_stream)
    return {
        "down_up_average" : down_up_average,
        "up_down_average" : up_down_average,
        "down_down_average" : down_down_average,
    }

def get_down_up_average(keystroke_stream):
    stack = []
    total_time = 0
    number_of_down_up_pairs = 0
    for keystroke in keystroke_stream:
        if keystroke['direction'] == 'DOWN':
            stack.append(keystroke)
        elif keystroke['direction'] == 'UP':
            if stack:
                top_keystroke = stack.pop()
                total_time += keystroke['timestamp'] - top_keystroke['timestamp']
                number_of_down_up_pairs += 1
    return total_time/number_of_down_up_pairs if number_of_down_up_pairs != 0 else None

def get_up_down_average(keystroke_stream):
    stack = []
    total_time = 0
    number_of_up_down_pairs= 0
    for keystroke in keystroke_stream:
        if keystroke['direction'] == 'UP':
            stack.append(keystroke)
        elif keystroke['direction'] == 'DOWN':
            if stack:
                top_keystroke = stack.pop()
                total_time += keystroke['timestamp'] - top_keystroke['timestamp']
                number_of_up_down_pairs += 1
    return total_time/number_of_up_down_pairs if number_of_up_down_pairs != 0 else None

def get_down_down_average(keystroke_stream):
    last_timestamp = None
    total_time = 0
    number_of_down_down_pairs = 0
    for keystroke in keystroke_stream:
        if keystroke['direction'] == 'DOWN':
            if last_timestamp is None:
                last_timestamp = keystroke['timestamp']
            else:
                total_time += keystroke['timestamp'] - last_timestamp
                number_of_down_down_pairs += 1
                last_timestamp = keystroke['timestamp']
    return total_time/number_of_down_down_pairs if number_of_down_down_pairs != 0 else None

