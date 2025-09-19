<?php
// Local configuration file example
// This file demonstrates various PHP define() statement patterns

// Boolean feature flags
define('FEATURE_ENABLED', true);
define('DEBUG_MODE', false);
define('MAINTENANCE_MODE', false);

// String configurations
define('API_BASE_URL', 'https://api.example.com');
define('DATABASE_HOST', 'localhost');
define('CACHE_DRIVER', 'redis');
define('APP_NAME', 'My Application');
define('APP_ENV', 'production');

// Numeric values
define('MAX_CONNECTIONS', 100);
define('TIMEOUT_SECONDS', 30);
define('CACHE_TTL', 3600);
define('MAX_UPLOAD_SIZE', 10485760);
define('PORT', 8080);

// File paths
define('LOG_PATH', '/var/log/app/');
define('UPLOAD_PATH', '/var/www/uploads/');
define('CONFIG_PATH', '/etc/app/config/');

// API keys and secrets (would normally use getenv())
define('API_KEY', getenv('API_KEY'));
define('DB_PASSWORD', getenv('DB_PASSWORD'));
define('SECRET_KEY', getenv('SECRET_KEY'));

// Array configuration examples
define('ALLOWED_FILE_TYPES', ['jpg', 'png', 'gif', 'pdf']);
define('SUPPORTED_LANGUAGES', ['en', 'es', 'fr', 'de']);

// Version information
define('APP_VERSION', '1.0.0');
define('API_VERSION', 'v2');

// Email settings
define('ADMIN_EMAIL', 'admin@example.com');
define('SUPPORT_EMAIL', 'support@example.com');
define('NO_REPLY_EMAIL', 'noreply@example.com');

// Security settings
define('HASH_ALGORITHM', 'sha256');
define('SESSION_LIFETIME', 7200);
define('MAX_LOGIN_ATTEMPTS', 5);

// Third-party service URLs
define('PAYMENT_GATEWAY_URL', 'https://payments.example.com/api');
define('EMAIL_SERVICE_URL', 'https://mail.example.com/api/v1');
define('CDN_BASE_URL', 'https://cdn.example.com');

// Feature toggles for different modules
define('ENABLE_PAYMENTS', true);
define('ENABLE_NOTIFICATIONS', false);
define('ENABLE_ANALYTICS', true);
define('ENABLE_CHAT', false);

// Performance settings
define('ENABLE_CACHING', true);
define('ENABLE_COMPRESSION', true);
define('MINIFY_ASSETS', false);