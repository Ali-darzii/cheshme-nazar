import logging

class SingleLevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level
    def filter(self, record):
        return record.levelno == self.level
      
AppServerLog = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'info_filter': {
            '()': SingleLevelFilter,
            'level': logging.INFO,
        },
        'warning_filter': {
            '()': SingleLevelFilter,
            'level': logging.WARNING,
        },
        'error_filter': {
            '()': SingleLevelFilter,
            'level': logging.ERROR,
        }
    },
    'loggers': {
        'cheshme-nazar': {
            'handlers': ['info', 'warning', 'error'],
            'level': 'INFO',
            'propagate': False,
        }
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'filename': 'log/python/api/info.log',
            'formatter': 'simpleRe',
            'filters': ['info_filter']
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'filename': 'log/python/api/warning.log',
            'formatter': 'simpleRe',
            'filters': ['warning_filter']
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'filename': 'log/python/api/error.log',
            'formatter': 'simpleRe',
            'filters': ['error_filter']
        },
    },
    'formatters': {
        'simpleRe': {
            'format': '{levelname} {asctime} {pathname} {module} {lineno} - {message}',
            'style': '{'
        }
    }
}