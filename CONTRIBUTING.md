# Contributing to SEO Analyzer Pro

First off, thank you for considering contributing to SEO Analyzer Pro! It's people like you that make SEO Analyzer Pro such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment (OS, Python version, etc)**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* End all files with a newline
* Update documentation as needed

---

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Styleguide

All Python must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/):

* Use 4 spaces for indentation (never tabs)
* Maximum line length: 88 characters
* Use type hints for all function signatures
* Write docstrings for all public functions and classes

Example:

```python
def analyze_keyword(keyword: str, language: str = "en") -> Dict[str, Any]:
    """
    Analyze keyword for SEO metrics.
    
    Args:
        keyword: The keyword to analyze
        language: Language code (en, fr, es, de)
        
    Returns:
        Dictionary with analysis results
    """
    pass
```

### Documentation Styleguide

* Use [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/)
* Reference methods and classes in markdown with the custom `{method}` or `{class}` roles
* Use proper spelling and grammar

---

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help organize and categorize issues and pull requests.

* `bug` - Something isn't working
* `enhancement` - New feature or request
* `documentation` - Improvements or additions to documentation
* `good-first-issue` - Good for newcomers
* `help-wanted` - Extra attention is needed
* `question` - Further information is requested
* `wontfix` - This will not be worked on

---

## Recognition

Contributors will be recognized in:
* CHANGELOG.md
* GitHub contributors page
* Project README (for significant contributions)

---

## Questions?

Feel free to contact us:
* Email: contributors@seoanalyzerpro.com
* GitHub Issues: github.com/seoanalyzerpro/issues

Thank you for contributing! 🎉
