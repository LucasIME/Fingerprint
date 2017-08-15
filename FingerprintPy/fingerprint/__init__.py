
class Keystroke:
    def __init__(self):
        pass

def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

def identify(keystroke_stream):
    features = extract_features(keystroke_stream)
    return features

def extract_features(keystroke_stream):
    resp = {}

    for c in char_range('a', 'z'):
        key = c + '_hold_avg'
        value = get_hold_avg_for_key(keystroke_stream, c)
        resp[key] = value
    
    return resp

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

def get_up_up_average(keystroke_stream):
    last_timestamp = None
    total_time = 0
    number_of_up_up_pairs = 0
    for keystroke in keystroke_stream:
        if keystroke['direction'] == 'UP':
            if last_timestamp is None:
                last_timestamp = keystroke['timestamp']
            else:
                total_time += keystroke['timestamp'] - last_timestamp
                number_of_up_up_pairs += 1
                last_timestamp = keystroke['timestamp']
    return total_time/number_of_up_up_pairs if number_of_up_up_pairs != 0 else None

def get_hold_avg_for_key(keystroke_stream, key):
    last_timestamp = None
    total_time = 0
    number_of_matches = 0
    for keystroke in keystroke_stream:
        if keystroke['key'] == key:    
            if keystroke['direction'] == 'DOWN':
                last_timestamp = keystroke['timestamp']
            elif keystroke['direction'] == 'UP':
                if last_timestamp is not None:
                    total_time += keystroke['timestamp'] - last_timestamp
                    number_of_matches += 1
                    last_timestamp = keystroke['timestamp']
    return total_time/number_of_matches if number_of_matches != 0 else None

def get_down_down_avg_for_digraph(keystroke_stream, key1, key2):
    last_timestamp = None
    total_time = 0
    number_of_matches = 0
    i = 0
    while i < len(keystroke_stream):
        cur_keystroke = keystroke_stream[i]
        if cur_keystroke['key'] == key1 and cur_keystroke['direction'] == 'DOWN':
            next_down_i = get_next_down(keystroke_stream, i)
            if keystroke_stream[next_down_i]['key'] == key2:
                total_time += keystroke_stream[next_down_i]['timestamp'] - cur_keystroke['timestamp']
                number_of_matches += 1
            i = next_down_i
        else:
            i+=1
    return total_time/number_of_matches if number_of_matches != 0 else None
