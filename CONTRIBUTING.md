# Contributing to org-ascii-timeline

Thank you for your interest in contributing to org-ascii-timeline!

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:
1. Check if the issue already exists in the issue tracker
2. Create a new issue with a clear description
3. Include example input that demonstrates the problem
4. Include the expected vs actual output

### Submitting Changes

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Test your changes with the example files
5. Ensure the scripts still work with Emacs Org-mode
6. Submit a pull request with a clear description of your changes

### Code Style

- Keep the code simple and readable
- Follow existing code patterns
- Add comments for non-obvious logic
- Maintain compatibility with Python 3.6+

### Testing

Before submitting:
```bash
# Test both scripts with all examples
./vtimeline.py < examples/simple.txt
./htimeline.py < examples/simple.txt

# Test with each example file
for f in examples/*.txt; do
    echo "Testing $f..."
    ./vtimeline.py < "$f"
    ./htimeline.py < "$f"
done
```

### Adding Examples

New example files are welcome! Place them in the `examples/` directory with a descriptive name and ensure they demonstrate a specific feature or use case.

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0 or later.

## Questions?

Feel free to open an issue for questions or discussion.
