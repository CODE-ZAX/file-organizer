# Contributing to File Organizer

Thank you for your interest in contributing to File Organizer! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or bugfix
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip

### Setup Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/file-organizer.git
   cd file-organizer
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

4. **Install development dependencies:**

   ```bash
   pip install pytest pytest-cov flake8 black isort
   ```

5. **Run tests to verify setup:**
   ```bash
   pytest
   ```

## Contributing Guidelines

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues in the codebase
- **New features**: Add new functionality
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **UI/UX**: Improve the user interface

### Before Contributing

1. **Check existing issues**: Look for existing issues or discussions
2. **Create an issue**: For significant changes, create an issue first
3. **Discuss changes**: For major features, discuss your approach
4. **Follow the style guide**: Adhere to coding standards

## Pull Request Process

### Before Submitting

1. **Update tests**: Add tests for new functionality
2. **Update documentation**: Update relevant documentation
3. **Run tests**: Ensure all tests pass
4. **Check code style**: Run linting and formatting tools
5. **Update changelog**: Add entry to CHANGELOG.md

### Pull Request Template

When creating a pull request, please include:

- **Description**: Clear description of changes
- **Type**: Bug fix, feature, documentation, etc.
- **Testing**: How you tested the changes
- **Breaking changes**: Any breaking changes
- **Related issues**: Link to related issues

### Review Process

1. **Automated checks**: CI/CD pipeline runs automatically
2. **Code review**: Maintainers review the code
3. **Testing**: Changes are tested on multiple platforms
4. **Approval**: At least one maintainer must approve
5. **Merge**: Changes are merged after approval

## Issue Reporting

### Before Creating an Issue

1. **Search existing issues**: Check if the issue already exists
2. **Check documentation**: Verify it's not a documentation issue
3. **Try latest version**: Ensure you're using the latest version

### Issue Template

When creating an issue, please include:

- **Title**: Clear, descriptive title
- **Description**: Detailed description of the issue
- **Steps to reproduce**: How to reproduce the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, etc.
- **Logs**: Relevant log output

### Bug Reports

For bug reports, please include:

- **Version**: File Organizer version
- **OS**: Operating system and version
- **Python version**: Python version used
- **Error message**: Complete error message
- **Log files**: Relevant log files
- **Minimal example**: Minimal code to reproduce

### Feature Requests

For feature requests, please include:

- **Use case**: Why this feature is needed
- **Proposed solution**: How you envision it working
- **Alternatives**: Other solutions you've considered
- **Additional context**: Any other relevant information

## Coding Standards

### Python Style

We follow PEP 8 with some modifications:

- **Line length**: 127 characters maximum
- **Indentation**: 4 spaces
- **Imports**: Grouped and sorted
- **Naming**: snake_case for variables and functions
- **Type hints**: Use type hints for all functions

### Code Formatting

We use `black` for code formatting and `isort` for import sorting:

```bash
# Format code
black file_organizer/

# Sort imports
isort file_organizer/
```

### Linting

We use `flake8` for linting:

```bash
# Run linting
flake8 file_organizer/
```

### Documentation

- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain complex logic
- **README**: Keep README up to date
- **API docs**: Update API documentation

## Testing

### Test Structure

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test component interactions
- **GUI tests**: Test user interface components
- **CLI tests**: Test command-line interface

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=file_organizer

# Run specific test file
pytest tests/test_file_organizer.py

# Run with verbose output
pytest -v
```

### Writing Tests

- **Test coverage**: Aim for high test coverage
- **Test names**: Use descriptive test names
- **Test isolation**: Tests should be independent
- **Mocking**: Use mocks for external dependencies
- **Fixtures**: Use pytest fixtures for common setup

### Test Examples

```python
def test_organize_directory_success():
    """Test successful directory organization."""
    config = Config()
    organizer = FileOrganizer(config)

    # Test implementation
    pass

def test_organize_directory_invalid_path():
    """Test organization with invalid path."""
    config = Config()
    organizer = FileOrganizer(config)

    with pytest.raises(ValueError):
        organizer.organize_directory("/invalid/path")
```

## Documentation

### Documentation Types

- **User documentation**: How to use the application
- **API documentation**: Reference for developers
- **Developer documentation**: How to contribute
- **Code comments**: Inline documentation

### Documentation Standards

- **Markdown**: Use Markdown for documentation
- **Examples**: Include code examples
- **Screenshots**: Include screenshots for GUI features
- **Links**: Use relative links when possible
- **Updates**: Keep documentation current

### Updating Documentation

1. **Identify changes**: What documentation needs updating
2. **Update files**: Modify relevant documentation files
3. **Review**: Check for accuracy and completeness
4. **Test**: Verify examples work correctly
5. **Submit**: Include documentation updates in PR

## Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update version**: Update version in setup.py
2. **Update changelog**: Add entry to CHANGELOG.md
3. **Create tag**: Create git tag for version
4. **Build package**: Build distribution packages
5. **Publish**: Publish to PyPI
6. **Create release**: Create GitHub release

## Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and discussions
- **Pull Requests**: For code contributions

### Questions

If you have questions about contributing:

1. **Check documentation**: Look through existing docs
2. **Search issues**: Check for similar questions
3. **Create issue**: Create a new issue with your question
4. **Be specific**: Provide clear details about your question

## Recognition

Contributors will be recognized in:

- **CONTRIBUTORS.md**: List of all contributors
- **Release notes**: Mentioned in release notes
- **GitHub**: Listed as contributors

Thank you for contributing to File Organizer!
