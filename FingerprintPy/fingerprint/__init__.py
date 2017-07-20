
def identify(keystroke_stream):
    features = extract_features(keystroke_stream)
    return features

def extract_features(keystroke_stream):
    down_up_average = get_down_up_average(keystroke_stream)
    return {
        "down_up_average" : down_up_average
    }

def get_down_up_average(keystroke_stream):
    stack = []
    total_time = 0
    number_of_down_up_pairs = 0
    for keystroke in keystroke_stream:
        if keystroke[1] == 'DOWN':
            stack.append(keystroke)
        elif keystroke[1] == 'UP':
            if stack:
                top_keystroke = stack.pop()
                total_time += keystroke[2] - top_keystroke[2]
                number_of_down_up_pairs += 1
    return total_time/number_of_down_up_pairs
