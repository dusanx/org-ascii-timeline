#!/usr/bin/env python3
# org-ascii-timeline - ASCII timeline visualization for Emacs Org-mode
# Copyright (C) 2026 Dusan Popovic
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
import re

def parse_input(text):
    """Parse the input format and return structured data."""
    lines = text.split('\n')
    left_title = ""
    right_title = ""
    events = []

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Skip comments and empty lines
        if line.startswith('--') or not line.strip():
            i += 1
            continue

        # Parse titles
        if line.startswith('>='):
            left_title = line[2:].strip()
            i += 1
            continue
        elif line.startswith('<='):
            right_title = line[2:].strip()
            i += 1
            continue

        # Parse events
        if line.startswith('>>') or line.startswith('>?') or line.startswith('>!'):
            side = 'left'
            event_type = line[1]  # '>', '?', or '!'
            event_lines = [line[2:].strip()]
            i += 1

            # Collect continuation lines and tag
            tag = ""
            while i < len(lines):
                next_line = lines[i].rstrip()
                if not next_line.strip():
                    break
                if next_line.startswith(('--', '>>', '>?', '>!', '<<', '<?', '<!')):
                    break
                if re.match(r'^\s*:[^:]+:\s*$', next_line):
                    tag = next_line.strip()[1:-1]
                    i += 1
                    break
                else:
                    event_lines.append(next_line.strip())
                    i += 1

            events.append({
                'side': side,
                'type': event_type,
                'lines': event_lines,
                'tag': tag
            })
            continue

        elif line.startswith('<<') or line.startswith('<?') or line.startswith('<!'):
            side = 'right'
            event_type = line[1]  # '<', '?', or '!'
            event_lines = [line[2:].strip()]
            i += 1

            # Collect continuation lines and tag
            tag = ""
            while i < len(lines):
                next_line = lines[i].rstrip()
                if not next_line.strip():
                    break
                if next_line.startswith(('--', '>>', '>?', '>!', '<<', '<?', '<!')):
                    break
                if re.match(r'^\s*:[^:]+:\s*$', next_line):
                    tag = next_line.strip()[1:-1]
                    i += 1
                    break
                else:
                    event_lines.append(next_line.strip())
                    i += 1

            events.append({
                'side': side,
                'type': event_type,
                'lines': event_lines,
                'tag': tag
            })
            continue

        i += 1

    return left_title, right_title, events

def calculate_connector_line(num_lines):
    """Determine which line to use for connector based on number of event lines."""
    # Always use the last line for connector
    return num_lines - 1

def render_timeline(left_title, right_title, events, total_width=76):
    """Render the vertical timeline with balanced layout."""
    output = []

    # Find the timeline position (determined by longest left event text)
    timeline_pos = 0

    for event in events:
        if event['side'] == 'left':
            # For left events, find the longest line
            max_line_len = max(len(line) for line in event['lines'])
            # Timeline must be at least: text + space + min_connector
            min_connector = 8  # At least 7 dashes + symbol
            needed_pos = max_line_len + 1 + min_connector
            timeline_pos = max(timeline_pos, needed_pos)

    # Render each event
    prefix = ""
    # Title
    #output.append(left_title + ''.ljust(timeline_pos - len(left_title)) + '|' + " " * 9 + right_title)
    title_padding = 5
    output.append(prefix + " " * (timeline_pos - len(left_title) - title_padding) + left_title + " " * title_padding + "|" + " " * title_padding + right_title)
    output.append(prefix + " " * (timeline_pos - len(left_title) - title_padding) + "-" * len(left_title) + " " * title_padding + "|" + " " * title_padding + "-" * len(right_title))
    # Start with one empty line
    output.append(prefix + ''.ljust(timeline_pos) + '|')
    for event in events:
        num_lines = len(event['lines'])
        connector_line_idx = calculate_connector_line(num_lines)

        for i, text in enumerate(event['lines']):
            if i == connector_line_idx:
                # This is the line with the connector
                if event['side'] == 'left':
                    # Left side: text + dashes (fill to timeline) + symbol + timeline + tag
                    text_end = len(text)
                    dashes_needed = timeline_pos - text_end - 1 - 1  # -1 for space, -1 for symbol
                    connector = ' ' + '-' * dashes_needed + event['type']
                    tag_str = ' ' + event['tag'] if event['tag'] else ''
                    line = text + connector + '+' + tag_str
                else:
                    # Right side: tag + timeline + symbol + dashes + space + text
                    connector = event['type'] + '-' * 7
                    tag_str = event['tag'] + ' ' if event['tag'] else ''
                    right_part = connector + ' ' + text
                    line = tag_str.rjust(timeline_pos) + '+' + right_part
            else:
                # Regular line without connector
                if event['side'] == 'left':
                    line = text.ljust(timeline_pos) + '|'
                else:
                    # Right side non-connector lines: timeline + spacing + text
                    # All right text starts 9 chars after timeline (symbol + 7 dashes + space)
                    line = ''.ljust(timeline_pos) + '|' + ' ' * 9 + text

            output.append(prefix + line)

        # Add a vertical line separator after each event
        output.append(prefix + ''.ljust(timeline_pos) + '|')

    return '\n'.join(output)

def main():
    body = sys.stdin.read()
    left_title, right_title, events = parse_input(body)
    result = render_timeline(left_title, right_title, events)
    print(result)

if __name__ == '__main__':
    main()
