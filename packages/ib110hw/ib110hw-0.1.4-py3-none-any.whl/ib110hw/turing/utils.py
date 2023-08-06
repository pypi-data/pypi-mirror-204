from .dtm import DTM
from ._helpers import (
    read_file,
    get_configuration,
    get_dtm_transition_function,
    validate_configuration,
    validate_dtm_transitions,
)
from typing import Optional
from sys import stderr


def load_dtm_from_file(file_path: str) -> Optional[DTM]:
    """
    Loads a DTM from a file if it is valid.
    Returns None if the configuration is invalid and prints the error to stderr.

    Args:
        file_path (str): Path to the file with configuration.

    Returns:
        Optional[DTM]: DTM if configuratin is valid, None otherwise.
    """
    definition = read_file(file_path)

    config_err = validate_configuration(definition)
    transitions_err = validate_dtm_transitions(definition)
    if config_err or transitions_err:
        print(config_err or transitions_err, file=stderr)
        return None

    init, acc, rej, abc = get_configuration(definition)
    transitions = get_dtm_transition_function(definition)

    return DTM(
        states={*transitions.keys()},
        input_alphabet=abc,
        acc_states=acc,
        initial_state=init,
        rej_states=rej,
        transitions=transitions,
    )


if __name__ == "__main__":
    pass
