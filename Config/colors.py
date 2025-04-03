class ColorText:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    GREEN = '\033[92m'

    @staticmethod
    def colorize(text, color):
        return f"{color}{text}{ColorText.RESET}"



