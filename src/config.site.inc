<?php
// Site-specific configuration file example
// This file demonstrates database and server configuration patterns

// Database configuration
define('DB_HOST', 'localhost');
define('DB_PORT', 3306);
define('DB_NAME', 'my_application');
define('DB_USER', getenv('DB_USER'));
define('DB_PASSWORD', getenv('DB_PASSWORD'));
define('DB_CHARSET', 'utf8mb4');
define('DB_COLLATION', 'utf8mb4_unicode_ci');

// Search engine configuration
define('SEARCH_ENGINE', 'elasticsearch');
define('SEARCH_HOST', 'localhost');
define('SEARCH_PORT', 9200);
define('SEARCH_INDEX', 'my_application');
define('SEARCH_ENABLED', true);

// Cache configuration
define('CACHE_DRIVER', 'redis');
define('CACHE_HOST', 'localhost');
define('CACHE_PORT', 6379);
define('CACHE_PREFIX', 'myapp_');
define('CACHE_TTL', 3600);

// Session configuration
define('SESSION_DRIVER', 'file');
define('SESSION_LIFETIME', 120);
define('SESSION_PATH', '/tmp/sessions/');
define('SESSION_SECURE', true);
define('SESSION_HTTP_ONLY', true);

// Mail configuration
define('MAIL_DRIVER', 'smtp');
define('MAIL_HOST', 'smtp.example.com');
define('MAIL_PORT', 587);
define('MAIL_USERNAME', getenv('MAIL_USERNAME'));
define('MAIL_PASSWORD', getenv('MAIL_PASSWORD'));
define('MAIL_ENCRYPTION', 'tls');
define('MAIL_FROM_ADDRESS', 'noreply@example.com');
define('MAIL_FROM_NAME', 'My Application');

// File storage configuration
define('FILESYSTEM_DRIVER', 'local');
define('STORAGE_PATH', '/var/www/storage/');
define('PUBLIC_PATH', '/var/www/public/');
define('MAX_FILE_SIZE', 10485760);

// Logging configuration
define('LOG_CHANNEL', 'daily');
define('LOG_LEVEL', 'debug');
define('LOG_PATH', '/var/log/myapp/');
define('LOG_MAX_FILES', 14);

// Queue configuration
define('QUEUE_DRIVER', 'redis');
define('QUEUE_HOST', 'localhost');
define('QUEUE_PORT', 6379);
define('QUEUE_DEFAULT', 'default');

// Broadcasting configuration
define('BROADCAST_DRIVER', 'pusher');
define('PUSHER_APP_ID', getenv('PUSHER_APP_ID'));
define('PUSHER_APP_KEY', getenv('PUSHER_APP_KEY'));
define('PUSHER_APP_SECRET', getenv('PUSHER_APP_SECRET'));
define('PUSHER_APP_CLUSTER', 'mt1');

// Redis configuration for multiple services
define('REDIS_HOST', 'localhost');
define('REDIS_PASSWORD', getenv('REDIS_PASSWORD'));
define('REDIS_PORT', 6379);
define('REDIS_DATABASE', 0);

// Server configuration
define('APP_URL', 'https://example.com');
define('FORCE_HTTPS', true);
define('TRUSTED_PROXIES', ['127.0.0.1']);
define('USE_HTTPS', true);

// Maintenance mode
define('MAINTENANCE_MODE', false);
define('MAINTENANCE_MESSAGE', 'Website is under maintenance. Please check back soon.');

// Security settings
define('CSP_ENABLED', true);
define('HSTS_ENABLED', true);
define('XSS_PROTECTION', true);
define('FRAME_OPTIONS', 'SAMEORIGIN');

// API rate limiting
define('RATE_LIMIT_ENABLED', true);
define('RATE_LIMIT_ATTEMPTS', 60);
define('RATE_LIMIT_MINUTES', 1);

// Backup configuration
define('BACKUP_ENABLED', true);
define('BACKUP_PATH', '/var/backups/myapp/');
define('BACKUP_RETENTION', 30);