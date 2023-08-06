from functools import wraps
from colorama import Fore, Style


def print_colored(
    *args: any, color: int = Fore.WHITE, sep: str = " ", end: str = "\n"
) -> None:
    """
    Prints the given arguments in the specified color, with the specified separator and ending character.

    Parameters
    ----------
    args : tuple
        Arguments to be printed.
    color : int, optional
        The color in which to print the text, by default Fore.WHITE.
    sep : str, optional
        The separator to be used between the arguments, by default " ".
    end : str, optional
        The character to be used at the end of the printed text, by default "\n".

    Returns
    -------
    None
    """

    print(color, end="")
    print(*args, sep=sep, end="")
    print(Style.RESET_ALL, end=end)


def print_error(*args: any, sep: str | None = " ", end: str | None = "\n") -> None:
    """
    Prints the given arguments as error message in red color, with the specified separator and ending character.

    Parameters
    ----------
    args : tuple
        Arguments to be printed as error message.
    sep : str or None, optional
        The separator to be used between the arguments, by default " ".
    end : str or None, optional
        The character to be used at the end of the printed text, by default "\n".

    Returns
    -------
    None
    """

    print_colored(
        *args,
        color=Fore.RED,
        sep=sep,
        end=end,
    )


def print_log(*args: any, sep: str | None = " ", end: str | None = "\n") -> None:
    """
    Prints the given arguments as a log message in yellow color, with the specified separator and ending character.

    Parameters
    ----------
    args : tuple
        Arguments to be printed as log message.
    sep : str or None, optional
        The separator to be used between the arguments, by default " ".
    end : str or None, optional
        The character to be used at the end of the printed text, by default "\n".

    Returns
    -------
    None
    """

    print_colored(
        *args,
        color=Fore.YELLOW,
        sep=sep,
        end=end,
    )


def print_success(*args: any, sep: str | None = " ", end: str | None = "\n") -> None:
    """
    Prints the given arguments as success message in green color, with the specified separator and ending character.

    Parameters
    ----------
    args : tuple
        Arguments to be printed as success message.
    sep : str or None, optional
        The separator to be used between the arguments, by default " ".
    end : str or None, optional
        The character to be used at the end of the printed text, by default "\n".

    Returns
    -------
    None
    """

    print_colored(
        *args,
        color=Fore.GREEN,
        sep=sep,
        end=end,
    )


def print_return(func):
    """
    Decorator that prints the return value of a function in cyan color and the function name in light blue color.

    Parameters
    ----------
    func : function
        The function to be decorated.

    Returns
    -------
    function
        The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        print(f"{Fore.CYAN}{result} \t\t ", end="")
        print(f"{Fore.LIGHTBLUE_EX} \t <- \t{func.__name__}", end="")
        print(Style.RESET_ALL)

        return result

    return wrapper


def print_return_info(func):
    """
    Decorator that prints the arguments and return value of a function in cyan and blue colors, respectively.

    Parameters
    ----------
    func : function
        The function to be decorated.

    Returns
    -------
    function
        The decorated function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        print(f"{Fore.CYAN}{result} \t\t", end="")
        print(f"{Fore.BLUE} \t <- \t{func.__name__}({args}, {kwargs})")
        print(Style.RESET_ALL)

        return result

    return wrapper
