seed_phrase = ""
db_url = "sqlite+aiosqlite:///./zeply.db"
bind = '0.0.0.0:8080'
log_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters=dict(
        std=dict(
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        ),
    ),
    handlers=dict(
        stderr={
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std',
            'stream': 'ext://sys.stderr',
        },
    ),
    loggers={
        'sqlalchemy.engine.Engine': dict(
            level='DEBUG',
        ),
    },
    root=dict(
        level='DEBUG',
        propagate=True,
        handlers=['stderr'],
    ),
)
