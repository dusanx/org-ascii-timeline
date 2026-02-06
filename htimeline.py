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
                    tag = next_line.strip()
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
                    tag = next_line.strip()
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

def create_box(event, left_title, right_title):
    """Create a box for an event with type, title, body lines, and tag."""
    # Box contents: type + title (from >= or <=), event lines, tag
    box_lines = []

    # First line: type symbol + space + title (based on side)
    title = left_title if event['side'] == 'left' else right_title
    first_line = event['type'] + ' ' + title
    box_lines.append(first_line)

    # Add all event text lines
    for line in event['lines']:
        box_lines.append(line)

    # Add tag if present
    if event['tag']:
        box_lines.append(event['tag'])

    # Calculate box width (longest line + 2 for padding)
    max_width = max(len(line) for line in box_lines)
    box_width = max_width + 2  # +2 for left and right padding

    # Build the box
    result = []

    # Top border
    result.append('+' + '-' * box_width + '+')

    # Content lines
    for line in box_lines:
        result.append('| ' + line.ljust(max_width) + ' |')

    # Bottom border
    result.append('+' + '-' * box_width + '+')

    return result

def render_horizontal_timeline(left_title, right_title, events):
    """Render horizontal timeline with boxes connected by arrows."""
    if not events:
        return ""

    # Create boxes for all events
    boxes = [create_box(event, left_title, right_title) for event in events]

    # Find maximum box height to determine vertical centering
    max_height = max(len(box) for box in boxes)

    # Vertically center all boxes
    centered_boxes = []
    for box in boxes:
        height = len(box)
        padding_top = (max_height - height) // 2
        padding_bottom = max_height - height - padding_top

        # Get box width from first line
        box_width = len(box[0])

        # Create centered box
        centered = []
        for _ in range(padding_top):
            centered.append(' ' * box_width)
        centered.extend(box)
        for _ in range(padding_bottom):
            centered.append(' ' * box_width)

        centered_boxes.append(centered)

    # Combine boxes horizontally with arrows
    output_lines = ['' for _ in range(max_height)]

    for i, box in enumerate(centered_boxes):
        # Add the box to output lines
        for line_idx, line in enumerate(box):
            output_lines[line_idx] += line

        # Add arrow connector if not the last box
        if i < len(centered_boxes) - 1:
            # Find middle line for arrow
            middle = max_height // 2
            for line_idx in range(max_height):
                if line_idx == middle:
                    output_lines[line_idx] += '-->'
                else:
                    output_lines[line_idx] += '   '

    return '\n'.join(output_lines)

def main():
    body = sys.stdin.read()
    left_title, right_title, events = parse_input(body)
    result = render_horizontal_timeline(left_title, right_title, events)
    print(result)

if __name__ == '__main__':
    main()
