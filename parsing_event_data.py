#!/usr/bin/env python3

import re
import json

def read_events(line):
    # group match, first part is key, second part is value
    splitting_pattern = r'([^:]*): "(.*?)"( |$)'
    # translate escaped quotes (\\" -> ")
    parsing_line = line.replace('\\"', '"')

    for match in re.findall(splitting_pattern, parsing_line):
        yield {match[0]: match[1]}

def parse_events(filename):
    with open(filename) as f:
        whole_data = {}
        for line in f:
            for event in read_events(line):
                # whole_data | event works, but requires python 3.9 or greater
                whole_data = {**whole_data, **event}
        return json.dumps(whole_data)

if __name__ == "__main__":
    events = parse_events("event_data.txt")
    print(f'parsed json of events: {events}')
