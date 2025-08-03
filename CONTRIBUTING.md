# Contributing to Krippendorff Alpha Python

Thank you for your interest in contributing to this project! This implementation aims to provide the most accurate and comprehensive Krippendorff's Alpha calculator available in Python.

## Code of Conduct

This project is dedicated to providing a harassment-free experience for everyone. We are committed to creating a welcoming and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Data sample** (if possible and not sensitive)
- **Environment details** (Python version, OS, package versions)

### Suggesting Features

Feature suggestions are welcome! Please:

- **Check existing issues** for similar requests
- **Describe the use case** and why it would be valuable
- **Reference theoretical literature** if applicable
- **Consider backward compatibility**

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** following our coding standards
4. **Add tests** for new functionality
5. **Run the test suite** to ensure nothing breaks
6. **Update documentation** as needed
7. **Commit your changes** (`git commit -m 'Add amazing feature'`)
8. **Push to the branch** (`git push origin feature/amazing-feature`)
9. **Open a Pull Request**

## Development Setup

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/ShWeaam/krippendorff-alpha-python-calculator.git
cd krippendorff-alpha-python-calculator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=krippendorff_alpha

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
black krippendorff_alpha/

# Check linting
flake8 krippendorff_alpha/

# Type checking
mypy krippendorff_alpha/
```

## Coding Standards

### Theoretical Accuracy

**CRITICAL**: Any changes to mathematical formulas must be validated against Krippendorff's theoretical specifications. The implementation must remain 100% compliant with the original methodology.

### Code Style

- Follow **PEP 8** style guidelines
- Use **Black** for code formatting
- Add **type hints** for all functions
- Write **comprehensive docstrings**
- Include **examples** in docstrings

### Testing

- **Unit tests** for all new functions
- **Integration tests** for complete workflows
- **Theoretical validation** against known results
- **Edge case testing** for robustness

### Documentation

- Update **README.md** for new features
- Add **docstring examples** for new functions
- Update **API documentation** as needed
- Include **theoretical justification** for changes

## Theoretical Compliance

This implementation follows Klaus Krippendorff's "Content Analysis: An Introduction to Its Methodology" (4th Edition, 2019). Any modifications must:

1. **Maintain theoretical accuracy** - No shortcuts or approximations
2. **Preserve mathematical formulas** - Exact implementation required
3. **Handle all measurement scales** - Nominal, ordinal, interval, ratio
4. **Support proper bootstrap methodology** - Unit resampling required
5. **Validate input appropriately** - Scale-specific data checking

### Red Lines (Do Not Modify Without Extreme Caution)

- **Core alpha formula**: α = 1 - (D_o / D_e)
- **Distance functions**: Scale-specific δ functions
- **Bootstrap resampling**: Unit-based resampling method
- **Data validation**: Scale-appropriate input checking

## Pull Request Guidelines

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Theoretical compliance verified

### PR Description Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Testing
How has this been tested?

## Theoretical Compliance
How does this maintain/improve theoretical accuracy?

## Breaking Changes
List any breaking changes

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Theoretical compliance verified
- [ ] Backward compatibility maintained
```

## Release Process

1. **Version bump** in `__init__.py` and `pyproject.toml`
2. **Update CHANGELOG.md**
3. **Create release tag**
4. **Build and publish** to PyPI
5. **Update documentation**

## Community

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: weaam.2511@gmail.com for sensitive issues

## Recognition

Contributors will be acknowledged in:
- **CONTRIBUTORS.md** file
- **Release notes**
- **Academic citations** where appropriate

Thank you for helping make this the most accurate and comprehensive Krippendorff's Alpha implementation available!

## References

- Krippendorff, K. (2019). *Content Analysis: An Introduction to Its Methodology* (4th ed.). SAGE Publications.
- [Project Documentation](./docs/)
- [Theoretical Validation Report](./docs/validation/)