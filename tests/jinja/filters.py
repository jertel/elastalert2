class DummyJinjaFilter:
    """ Custom dummy Jinja2 filter class to test filter loading from a module """
    @staticmethod
    def filter_whisper(value):
        if isinstance(value, str):
            return value.lower()
        return value
