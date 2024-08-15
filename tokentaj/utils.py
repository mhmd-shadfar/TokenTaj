def count_pairs(tokens: list[int]) -> dict[tuple, int]:
    """
    Return the count of pairs in tokens.

    Args:
        tokens (list[int]): A list of integers representing the tokens.

    Returns:
        dict[tuple, int]: A dictionary where keys are pairs and values are their associated counts.
    """
    pairs = {}
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        pairs[pair] = pairs.get(pair, 0) + 1
    return pairs

def merge_top_pair(tokens: list[int], pair: tuple[int, int], new_byte: int) -> list[int]:
    """
    Merge the top pair with new_byte

    Args:
        tokens (list[int]): A list of integers representing the tokens.
        pair (tuple[int, int]): A tuple of two integers representing the pair to be merged.
        new_byte (int): An integer representing the new byte to be inserted.

    Returns:
        list[int]: A list of integers representing the modified tokens.
    """
    i = 0
    new_tokens = []
    while i < len(tokens):
        if tokens[i] == pair[0] and tokens[i + 1] == pair[1] and i < len(tokens) - 1:
            new_tokens.append(new_byte)
            i += 2
        else:
            new_tokens.append(tokens[i])
            i += 1
    return new_tokens

def find_min_pair(pairs: dict, merges: dict) -> tuple:
    """
    Find the pair from a dictionary of pairs that has the smallest value.
    
    Args:
        pairs (dict): A dictionary where keys are pairs and values are their associated values.
    
    Returns:
        The pair with the smallest value.
    """
    min_pair = None
    min_value = float("inf")
    
    for pair in pairs:
        value = merges.get(pair, float("inf"))
        
        if value < min_value:
            min_value = value
            min_pair = pair
            
    return min_pair

def find_max_pair(pairs: dict) -> tuple:
    """
    Find the pair from a dictionary of pairs that has the largest value.
    
    Args:
        pairs (dict): A dictionary where keys are pairs and values are their associated values.
    
    Returns:
        The pair with the largest value.
    """
    best_pair = None
    best_value = float("-inf")
    
    for pair, value in pairs.items():
        if value > best_value:
            best_value = value
            best_pair = pair
    
    return best_pair