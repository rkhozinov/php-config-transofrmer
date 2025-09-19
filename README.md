# PHP Config Transformer

A simple utility that transforms PHP `define()` statements to use environment variables with fallbacks.

## Features

- ✨ Transforms `define('CONSTANT', 'value');` to `define('CONSTANT', getenv('CONSTANT', 'value'));`
- 🔒 Safe file operations - original files remain untouched in `/src`
- 📁 Results written to separate `/result` directory
- 👀 Preview changes before applying them
- 📊 Get statistics about defines in your files
- 🎯 Handles various data types (strings, numbers, booleans, arrays)
- 💻 Cross-platform line ending support

## Installation

```bash
git clone https://github.com/rkhozinov/php-config-transformer.git
cd php-config-transformer
```

## Usage

### Basic Usage

Transform all `.inc` files from `src/` directory to `result/` directory:

```bash
python main.py src/
```

### Custom Output Directory

```bash
python main.py src/ custom-result/
```

### Preview Changes

See what transformations would be made without writing files:

```bash
python main.py --preview src/
```

### Show Statistics

Get statistics about defines in your files:

```bash
python main.py --stats src/
```

## Examples

### Before Transformation

```php
<?php
// Local configuration file

// Boolean feature flags
define('FEATURE_ENABLED', true);
define('DEBUG_MODE', false);

// String configurations
define('API_BASE_URL', 'https://api.example.com');
define('DATABASE_HOST', 'localhost');

// Numeric values
define('MAX_CONNECTIONS', 100);
define('TIMEOUT_SECONDS', 30);

// File paths
define('LOG_PATH', '/var/log/app/');
define('UPLOAD_PATH', '/var/www/uploads/');
```

### After Transformation

```php
<?php
// Local configuration file

// Boolean feature flags
define('FEATURE_ENABLED', getenv('FEATURE_ENABLED', true));
define('DEBUG_MODE', getenv('DEBUG_MODE', false));

// String configurations
define('API_BASE_URL', getenv('API_BASE_URL', 'https://api.example.com'));
define('DATABASE_HOST', getenv('DATABASE_HOST', 'localhost'));

// Numeric values
define('MAX_CONNECTIONS', getenv('MAX_CONNECTIONS', 100));
define('TIMEOUT_SECONDS', getenv('TIMEOUT_SECONDS', 30));

// File paths
define('LOG_PATH', getenv('LOG_PATH', '/var/log/app/'));
define('UPLOAD_PATH', getenv('UPLOAD_PATH', '/var/www/uploads/'));
```

## How It Works

1. **Safe Processing**: Original files in `src/` directory are never modified
2. **Copy First**: Files are copied to `result/` directory before transformation
3. **Smart Detection**: Only transforms `define()` statements that don't already use `getenv()`
4. **Type Preservation**: Maintains original data types and quote styles
5. **Line Ending Support**: Preserves original line endings (LF or CRLF)

## Directory Structure

```
php-config-transformer/
├── main.py              # Main transformer script
├── pyproject.toml       # Python project configuration
├── src/                 # Source files (never modified)
│   ├── config.local.inc
│   └── config.site.inc
├── result/              # Generated files (created after transformation)
├── LICENSE              # MIT License
├── README.md            # This file
└── CLAUDE.md            # Developer documentation
```

## Command Line Options

```
usage: main.py [-h] [--preview] [--stats] [src_dir] [result_dir]

Transform PHP define() statements to use environment variables with fallbacks

positional arguments:
  src_dir       Source directory (default: src)
  result_dir    Result directory (default: result)

optional arguments:
  -h, --help    show this help message and exit
  --preview     Preview changes without writing files
  --stats       Show statistics about defines
```

## Requirements

- Python 3.8+
- No external dependencies

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please use the [GitHub Issues](https://github.com/rkhozinov/php-config-transformer/issues) page.