# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PHP Config Transformer is a command-line utility that converts PHP `define()` statements to use environment variables with fallbacks. It reads original configuration files from the `src/` directory and writes transformed files to the `result/` directory.

## Purpose

This tool helps modernize PHP configuration files by:
- Converting hardcoded values to environment variable-based configuration
- Maintaining backward compatibility with default values
- Supporting Docker and cloud deployment patterns
- Enabling environment-specific configuration without code changes

## Simple Usage

The main transformer is `main.py` with a simple CLI interface:

### Transform Files (Default)
```bash
python main.py src/
```
- Reads all `.inc` files from `src/`
- Transforms define() statements to use getenv() with defaults
- Writes results to `result/` directory
- Preserves original formatting and comments

### Custom Output Directory
```bash
python main.py src/ custom_output/
```
- Transform files to custom output directory

### Preview Changes
```bash
python main.py --preview src/
```
- Shows what changes would be made without modifying files
- Displays first few changes for each file

### Show Statistics
```bash
python main.py --stats src/
```
- Shows statistics about defines in source files
- Displays counts of transformable vs already getenv() defines

## Key Features

- **Safe**: Original files remain untouched in `src/`
- **Preserves formatting**: Maintains original line structure and comments
- **Selective**: Only transforms defines that don't already use getenv()
- **Multi-typed**: Handles strings, booleans, numbers, and arrays
- **Automatic**: Processes all `.inc` files in directory
- **No backup needed**: Always writes to separate result directory

## Directory Structure

```
php-config-transformer/
├── src/                    # Original configuration files (untouched)
│   ├── config.local.inc    # Local configuration examples
│   └── config.site.inc     # Site configuration examples
├── result/                 # Transformed files (generated)
│   ├── config.local.inc    # Transformed with getenv()
│   └── config.site.inc     # Transformed with getenv()
├── main.py                 # Single file with all logic
├── README.md               # GitHub documentation
├── CLAUDE.md              # This file
└── LICENSE                # MIT License
```

## Transformation Examples

**Before:**
```php
define('FEATURE_ENABLED', true);
define('API_BASE_URL', 'https://api.example.com');
define('MAX_CONNECTIONS', 100);
define('DB_PASSWORD', 'secret');
```

**After:**
```php
define('FEATURE_ENABLED', getenv('FEATURE_ENABLED', true));
define('API_BASE_URL', getenv('API_BASE_URL', 'https://api.example.com'));
define('MAX_CONNECTIONS', getenv('MAX_CONNECTIONS', 100));
define('DB_PASSWORD', getenv('DB_PASSWORD'));
```

## Implementation Notes

### Regex Patterns
The tool uses two main regex patterns:
- `define_pattern`: Matches define() statements with various quote styles and spacing
- `getenv_pattern`: Detects if getenv() is already being used

### Value Type Handling
- **Strings**: Preserved with original quotes
- **Booleans**: `true`/`false` converted to PHP boolean values
- **Numbers**: Integers and floats preserved as-is
- **Arrays**: PHP array syntax preserved

### Line Ending Preservation
Original line endings (`\n`, `\r\n`) are preserved to maintain file compatibility across different systems.

### Error Handling
- Gracefully handles malformed define() statements
- Skips commented lines and complex expressions
- Provides clear error messages for file operations

## Development

### Adding New Features
1. All logic is contained in `main.py` - no external dependencies
2. The `EnvTransformer` class handles all transformation logic
3. CLI interface uses Python's built-in `argparse` module

### Testing
- Test with the provided example files in `src/`
- Use `--preview` to verify changes before applying
- Use `--stats` to understand what will be transformed

### Code Style
- Follows Python PEP 8 guidelines
- Type hints included for better code understanding
- Comprehensive docstrings for all public methods

## Environment Variables

The tool helps migrate to environment-based configuration. Common patterns:

**Database Configuration:**
```php
define('DB_HOST', getenv('DB_HOST', 'localhost'));
define('DB_USER', getenv('DB_USER', 'root'));
define('DB_PASSWORD', getenv('DB_PASSWORD'));
```

**Feature Flags:**
```php
define('DEBUG_MODE', getenv('DEBUG_MODE', false));
define('MAINTENANCE_MODE', getenv('MAINTENANCE_MODE', false));
```

**API Configuration:**
```php
define('API_KEY', getenv('API_KEY'));
define('API_BASE_URL', getenv('API_BASE_URL', 'https://api.example.com'));
```

This tool is particularly useful for:
- Docker containerization
- CI/CD pipeline configuration
- Multi-environment deployments
- Security best practices (no secrets in code)