def calculate_median(numbers):
    """
    Calculates the median of a list of numbers.
    """
    if not numbers:
        return None

    n = len(numbers)
    mid_index = n // 2

    if n % 2 == 1:
        return numbers[mid_index]
    else:
        return (numbers[mid_index - 1] + numbers[mid_index]) / 2
