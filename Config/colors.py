class ColorText:
    """
    Color text lass, used for providing auto color-code parsing
    """
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    GREEN = '\033[92m'

    @staticmethod
    def colorize(text, color: str):
        """
        creates a coloured string based on color code
        :param text: a string of text to be coloured
        :param color: color code for the color, available using ColorText class attributes (CYAN, YELLOW, RED, GREEN)
        :return: string with applied color codes for printing purpose
        """
        return f"{color}{text}{ColorText.RESET}"



