#!/usr/bin/env python3

import re
import json
import base64

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

def populate_fifth_event(parsed_json):
    #check hint
    print('Outputing values to solve what fifth value could be')
    print(f'\tprovided hint is "{base64.b64decode(parsed_json.get("hint"))}"')
    # base64 decode the hint told to do xor with 0x17f
    bitwise_xor_from_hint = int("0x17F", 16)
    for value in ["one", "two", "three", "four"]:
        # parse hex-string to int and do xor with hinted value
        output = int(parsed_json.get(value), 16) ^ bitwise_xor_from_hint
        #print output values for manual pattern calculating
        print(f'\t{value} = {parsed_json.get(value)} xorred with 0x17F = {output} and in hex {hex(output)}')
    # pattern seems to be nb nf n5 so fifth value would be 0x35 ^ 0x17F
    # populate fifth value to dict
    parsed_json['five'] = hex(int("0x35", 16) ^ bitwise_xor_from_hint)
    return parsed_json

if __name__ == "__main__":
    events = parse_events("event_data.txt")
    print(f'parsed json of events: {events}')
    parsed_json = json.loads(events)
    parsed_json = populate_fifth_event(parsed_json)
    print(f'json with fifth event added: {parsed_json}')
