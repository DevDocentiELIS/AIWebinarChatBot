import subprocess
import sys
from Config.colors import ColorText

__OPS_SUCCESS_PREFIX = "[SUCCESS]"
__OPS_FAILURE_PREFIX = "[FAILURE]"


def __get_ollama_models() -> list[str]:
    """Retrieve the list of available models in Ollama.
    :return: List of available models in Ollama. Empty list if no models are found
    """
    try:
        result = subprocess.run(["ollama", "list"],
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)

        models = [line.split()[0] for line in result.stdout.strip().split("\n") if line]
        return models[1:]
    except subprocess.CalledProcessError:
        return []


def __install_selected_model(model: str) -> None:
    """
    Downloads and Installs the selected model in Ollama.
    :param model: model name to be pulled in Ollama
    """
    ops_prefix = f"[CONFIG][OLLAMA][MODEL]"
    print(
        ColorText.colorize(
            f"{ops_prefix} Attempting to download {model}. This may take some time.",
            ColorText.YELLOW
        )
    )

    try:
        process = subprocess.Popen(
            ["ollama", "pull", model],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )

        for line in iter(process.stdout.readline, ""):
            sys.stdout.write("\r" + line.strip())
            sys.stdout.flush()

        process.stdout.close()
        process.wait()

        if process.returncode == 0:
            print("\n" + ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} {model} correctly installed.",
                ColorText.GREEN)
            )
        else:
            print("\n" + ColorText.colorize(
                f"{ops_prefix}{__OPS_FAILURE_PREFIX} Error while installing {model}.",
                ColorText.RED)
            )

    except subprocess.SubprocessError:
        print(ColorText.colorize(
            f"{ops_prefix}{__OPS_FAILURE_PREFIX} Unexpected error occurred.",
            ColorText.RED)
        )


def __check_ollama_installed() -> bool:
    """Check if Ollama is installed by running `ollama --version`.
    :return: True if Ollama is installed else False.
    """
    ops_prefix = f"[CONFIG][OLLAMA]"
    print(ColorText.colorize(f"{ops_prefix} Checking if OLLAMA is correctly installed.", ColorText.CYAN))
    try:
        subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(ColorText.colorize(f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Ollama found.", ColorText.GREEN))
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(ColorText.colorize(f"{ops_prefix}{__OPS_FAILURE_PREFIX} Ollama not found.", ColorText.RED))
        return False


def __check_model_availability(model: str) -> bool:
    """Check if a specific model is found in Ollama.
    :param model: Model name
    :return: True if the model is available, False otherwise
    """
    ops_prefix = f"[CONFIG][OLLAMA][MODEL]"

    print(ColorText.colorize(f"{ops_prefix} Checking if {model} is available in Ollama env.", ColorText.CYAN))
    available_models = __get_ollama_models()
    if model not in available_models:
        print(ColorText.colorize(f"{ops_prefix}{__OPS_FAILURE_PREFIX} {model} not found in Ollama.", ColorText.RED))
        return False

    print(ColorText.colorize(f"{ops_prefix}{__OPS_SUCCESS_PREFIX} {model} found.", ColorText.GREEN))
    return True


def __ollama_model_configuration(model: str) -> None:
    """
    Checks if a specified model is available in Ollama. If not, the model is downloaded and installed
    :param model:
    """

    if not __check_model_availability(model):
        __install_selected_model(model)
        __check_model_availability(model)


def config_ollama_requirements(embedding_model: str, chat_model: str) -> None:
    """
    Runs the entire Ollama configuration for the API
    :param embedding_model: the Ollama model used for info source embedding
    :param chat_model: the Ollama model used for chat
    """
    if __check_ollama_installed():
        __ollama_model_configuration(embedding_model)
        __ollama_model_configuration(chat_model)


if __name__ == "__main__":
    config_ollama_requirements(embedding_model="nomic-embed-text:latest", chat_model="llama3.2:latest")
