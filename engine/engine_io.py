"""
IO for engine

"""

import pickle


def pickle_loader(file_stream):
    """
    define how to load the game content from file stream

    @param file_stream: file stream
    @return: result

    """
    return pickle.load(file_stream)


def pickle_dumper(game_content_raw: list, file_stream) -> bool:
    """
    define how to dump the game content into file stream

    @param game_content_raw: raw game content
    @param file_stream: file stream
    @return: ok or not

    """
    try:
        pickle.dump(game_content_raw, file_stream)
        return True
    except Exception as e:
        print(f"dump game content failed due to {str(e)}")
        return False
