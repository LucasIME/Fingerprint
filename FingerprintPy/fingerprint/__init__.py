
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
    
    pairs_to_analyze = [('v', 'e'), ('d', 'o'), ('l', ' '), ('l', 'p'), ('s', 'o'), ('w', 'n'), ('c', 'a'), ('j', 'u'), ('r', 'n'), ('p', 'h'), (' ', 'T'), ('x', ' '), ('n', ' '), ('t', 'h'), ('e', 't'), ('q', 'u'), ('u', 'i'), ('o', ' '), ('p', 's'), ('P', 'P'), (' ', 'q'), ('a', 'n'), ('r', ' '), ('i', 'n'), ('e', 'r'), ('R', 'C'), ('h', 'a'), ('u', 'r'), ('l', 'l'), ('r', 's'), ('g', ' '), ('I', 't'), ('s', 'e'), ('w', 'e'), ('e', ':'), ('a', 'z'), (' ', 'j'), ('T', 'h'), ('p', 'a'), ('l', 's'), ('r', 'a'), ('a', 'c'), ('o', 'v'), ('n', 'd'), ('t', 'y'), ('f', 'o'), ('b', 'r'), ('t', 'e'), ('c', 't'), ('t', 'r'), ('t', ' '), ('l', 'a'), ('E', 'R'), ('k', ' '), ('t', 't'), ('p', 'i'), ('y', 'o'), ('a', 'g'), ('u', 'm'), (' ', 'o'), (' ', 'U'), ('A', 'S'), (' ', 'h'), ('h', '.'), ('a', 'b'), ('h', 'e'), ('l', 'o'), ('c', 'h'), ('n', 't'), (' ', 'p'), ('i', 'k'), ('e', 'n'), ('a', 'i'), ('r', 'o'), ('e', ' '), ('d', ' '), ('a', 's'), ('n', 'c'), ('i', 's'), ('t', 'o'), ('o', 'w'), (' ', 't'), ('r', 'c'), ('c', 'k'), ('a', 'l'), ('g', 'r'), (' ', 'd'), ('a', 'r'), ('o', 'u'), ('m', 'p'), ('n', 'g'), ('c', 'e'), (' ', 'b'), ('.', ' '), ('y', 'p'), ('l', 'i'), (' ', 'i'), ('h', 'i'), (' ', 'a'), ('a', 't'), ('C', 'A'), ('e', 'a'), ('l', 'e'), ('n', 'i'), ('P', 'E'), (' ', 'f'), ('a', 'p'), ('i', 'c'), ('n', '.'), ('k', 'e'), ('o', 'g'), ('y', ' '), ('E', ' '), (' ', 's'), (':', ' '), (' ', 'I'), ('z', 'y'), ('b', 'e'), ('s', ' '), (' ', 'y'), (' ', 'l'), ('U', 'P'), ('o', 'x'), ('S', 'E'), (' ', 'c')] 
    for c, c2 in pairs_to_analyze:
        key = 'DD_{0}_{1}'.format(convert_to_mongo_acceptable_string(c), convert_to_mongo_acceptable_string(c2))
        value = get_down_down_avg_for_digraph(keystroke_stream, c, c2)
        resp[key] = value

    return resp

def convert_to_mongo_acceptable_string(char):
    if char.isalnum():
        return char
    if char == '.':
        return 'period'
    if char == ' ':
        return 'space'
    if char == ':':
        return 'colon'
    if char == ';':
        return 'semicolon'

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
            if next_down_i == -1:
                break
            if keystroke_stream[next_down_i]['key'] == key2:
                total_time += keystroke_stream[next_down_i]['timestamp'] - cur_keystroke['timestamp']
                number_of_matches += 1
            i = next_down_i
        else:
            i+=1
    return total_time/number_of_matches if number_of_matches != 0 else None

def get_next_down(keystroke_stream, i):
    for i2 in range(i+1, len(keystroke_stream)):
        cur_keystroke = keystroke_stream[i2]
        if cur_keystroke['direction'] == 'DOWN':
            return i2
    return -1
