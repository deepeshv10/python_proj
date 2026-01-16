def mutate_string(string, position, character):
    """
    Replace a character at a specific position in a string.

    Since strings are immutable in Python, this function converts the string
    to a list, modifies the character at the given position, and joins it back.

    Args:
        string (str): The original string to be modified.
        position (int): The index position where the character should be replaced.
        character (str): The new character to insert at the specified position.

    Returns:
        str: A new string with the character replaced at the given position.

    Example:
        >>> mutate_string("hello", 1, 'a')
        'hallo'
    """
    x = list(string)
    x[position] = character
    new_string = "".join(x)
    return new_string

if __name__ == '__main__':
    s = input()
    i, c = input().split()
    s_new = mutate_string(s, int(i), c)
    print(s_new)