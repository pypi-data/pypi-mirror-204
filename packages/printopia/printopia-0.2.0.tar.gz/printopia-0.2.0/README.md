<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg?&style=for-the-badge&logo=python&logoColor=blue"></a>


Introduction
------------------------------------------------
This code provides functions to print colored messages in the console, as well as decorators to print the return values and arguments of a function.


## Usage

### Functions
The print_colored, print_error, print_log, and print_success functions all take the same arguments:

- *args: the arguments to be printed.
- color: the color in which to print the text (default: white).
- sep: the separator to be used between the arguments (default: " ").
- end: the character to be used at the end of the printed text (default: "\n").

Example usage:

```python
print_colored("This text is white.")
print_error("This text is red.")
print_log("This text is yellow.")
print_success("This text is green.")
```

### Decorators
The print_return and print_return_info decorators can be used to print the return value and/or arguments of a function.

Example usage:

```python
@print_return
def add_numbers(x, y):
    return x + y

add_numbers(2, 3)
## Output:
# 5            <-     add_numbers

@print_return_info
def multiply_numbers(x, y):
    return x * y

multiply_numbers(2, 3)
## Output: 
# 6             <-     multiply_numbers(2, 3)
```

### Dependencies
```shell
colorama = "^0.4.6"
```
________________________________________________________________

