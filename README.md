# org-ascii-timeline

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

ASCII timeline visualization tools for Emacs Org-mode. Create beautiful vertical and horizontal timelines using a simple, intuitive syntax.

```
                    Developer     |     Reviewer
                    ---------     |     --------
                                  |
Request code review ------------->+ (feature/auth)
                                  |
                                  |         Reviewing changes
                         (review) +<------- Found minor issues
                                  |
Fixed issues as requested ------->+ (updated)
                                  |
                                  +!------- Approved, please merge
                                  |
Merged to main ------------------>+
                                  |
```

## License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

## Overview

org-ascii-timeline provides two visualization styles for timeline data:
- **vtimeline.py**: Vertical timeline with events flowing top-to-bottom
- **htimeline.py**: Horizontal timeline with boxed events flowing left-to-right

Both scripts use the same simple input format and are designed to work seamlessly with Emacs Org-mode's babel execution system.

## Language Syntax

The timeline language is designed to capture interactions between two actors (left and right).

### Basic Structure

```
>= Left Actor Name
<= Right Actor Name

>> Event from left actor
<< Event from right actor
```

### Event Types

Events are defined by a two-character prefix:

**First character** - Defines the actor:
- `>` - Left actor
- `<` - Right actor

**Second character** - Defines the event type:
- `>` or `<` - Communication/message
- `?` - Question/decision point
- `!` - Imperative/annotation/command

### Multi-line Events

Events can span multiple lines. Simply continue writing on the next line:

```
>> This is a multi-line event
   that continues here
   and even here
```

### Tags

Add optional tags to events using `:tag:` syntax. Tags appear on different positions depending on the visualization:
- **Vertical timeline**: Tags appear next to the timeline axis
- **Horizontal timeline**: Tags appear inside the box, at the bottom

```
>> Event with a tag
   :2025:
```

Tags can be dates, categories, or any label (`:feature:`, `:bug:`, `:cats:`).

### Comments and Empty Lines

```
-- This is a comment and will be ignored

Lines with only whitespace are also ignored
```

### Complete Example

```
-- Project discussion
>= Developer
<= Code Reviewer

>> Implemented new authentication system
   with OAuth2 support
   :feature:

<? Does this meet security requirements?
   :security-review:

>! Updated documentation
   :docs:

<< Approved and merged to main
   :approved:
```

## Installation

1. Clone or download this repository
2. Make the scripts executable:
```bash
chmod +x vtimeline.py htimeline.py
```

## Usage

### Command Line

Both scripts read from stdin:

```bash
cat examples/example1.txt | ./vtimeline.py
cat examples/example1.txt | ./htimeline.py
```

### Emacs Org-mode Integration

#### Configuration for Doom Emacs

Add to your `config.el`:

```elisp
;; Optional: Control indentation behavior
(setq org-adapt-indentation t)  ;; nil=0 indent; t=align with heading
(setq org-babel-min-lines-for-block-output 9999) ;; optional force ":" prepend

;; Configure babel execution for timeline languages
(after! org
  ;; Vertical timeline outputs raw text (no wrapping)
  (setq org-babel-default-header-args:vtimeline
        '((:results . "scalar replace")))

  ;; Horizontal timeline wrapped in example block
  (setq org-babel-default-header-args:htimeline
        '((:results . "replace")
          (:wrap . "example")))

  ;; Define execution functions
  (defun org-babel-execute:vtimeline (body params)
    (org-babel-eval "~/path/to/vtimeline.py" body))

  (defun org-babel-execute:htimeline (body params)
    (org-babel-eval "~/path/to/htimeline.py" body)))
```

**Note**: Update `~/path/to/` with the actual path to your scripts.

#### Configuration for Regular Emacs

Add to your `init.el` or `.emacs`:

```elisp
(require 'org)

;; Configure babel execution for timeline languages
(setq org-babel-default-header-args:vtimeline
      '((:results . "raw replace")))

(setq org-babel-default-header-args:htimeline
      '((:results . "replace")
        (:wrap . "example")))

(defun org-babel-execute:vtimeline (body params)
  (org-babel-eval "~/path/to/vtimeline.py" body))

(defun org-babel-execute:htimeline (body params)
  (org-babel-eval "~/path/to/htimeline.py" body))
```

**Note**: Update `~/path/to/` with the actual path to your scripts.

#### Using in Org Files

1. Create a source block with `<s TAB` then type `vtimeline` or `htimeline`
2. Or manually create:

```org
#+begin_src vtimeline
>= Customer
<= Support Team

>> Initial inquiry
<< Response provided
#+end_src
```

3. Execute with `C-c C-c` while cursor is in the block

## Vertical Timeline (vtimeline.py)

Renders events on a central vertical axis with left and right events.

### Features

- Fixed timeline position for clean alignment
- Multi-line events connect on their last line
- Arrows automatically padded to reach timeline
- Tags displayed next to the timeline axis
- Balanced layout with proper spacing

### Example Output

```
                               Customer     |     Support Team
                               --------     |     ------------
                                            |
Initial inquiry about product ------------->+ (2020)
                                            |
                                            |         Response with product details
                                     (2021) +<------- More information provided
                                            |
Should I purchase the premium plan? -------?+ (2022)
                                            |
                                     (2023) +!------- Please complete the purchase form
                                            |
Form submitted successfully --------------->+
                                            |
```

## Horizontal Timeline (htimeline.py)

Renders events as ASCII boxes connected by arrows.

### Features

- Events displayed in bordered boxes
- First line shows event type + actor name
- Boxes vertically centered for balanced appearance
- Connected with `-->` arrows
- Tags appear at bottom of box

### Example Output

```
+-------------------------------+   +-------------------------------+
| > Customer                    |   | < Support Team                |
| Initial inquiry about product |   | Response with product details |
| 2020                          |-->| More information provided     |
+-------------------------------+   | 2021                          |
                                    +-------------------------------+
```

## Examples

See the `examples/` directory for sample timeline files demonstrating various features.

## Requirements

- Python 3.6+
- For Org-mode integration: Emacs with Org-mode

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Author

Created for use with Emacs Org-mode to create beautiful, simple timeline visualizations.
