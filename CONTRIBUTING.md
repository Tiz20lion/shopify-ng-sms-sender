# Contributing to Shopify Nigeria SMS Sender

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)

### Suggesting Features

Feature suggestions are welcome! Open an issue describing:
- The feature you'd like to see
- Why it would be useful
- How it might work

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit with clear messages (`git commit -m 'Add amazing feature'`)
5. Push to your branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Code Style

- Follow the existing code style
- Use type hints for all function parameters and return values
- Keep functions focused and small
- Add comments only when logic is non-obvious
- Ensure all tests pass (if applicable)

### Setup for Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `.\venv\Scripts\Activate.ps1` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `example.env` to `.env` and configure
6. Copy `app/templates.json.example` to `app/templates.json`

### Testing

Before submitting:
- Test your changes locally
- Ensure webhook verification still works
- Test SMS sending with a test phone number
- Check that templates save/load correctly

## Questions?

Feel free to open an issue for any questions!

