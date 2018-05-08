

class Config:
    """Default Flask configuration inherited by all environments. Use this for development environments."""
    pass


class TestConfig(Config):
    pass


class ProductionConfig(Config):
    pass


