


class BaseMessages:
    """Base class for validation messages with naming functionality"""

    @classmethod
    def get_message_type(cls, message):
        """Returns the constant name for a given message value"""
        for name, value in vars(cls).items():
            if isinstance(value, str) and value == message and not name.startswith('_'):
                return name
        return "UNKNOWN USE CASE"