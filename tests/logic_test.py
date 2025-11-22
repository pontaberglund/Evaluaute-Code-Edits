def calculate_median(numbers):
    """
    Calculates the median of a list of numbers.
    """
    if not numbers:
        return None

    n = len(numbers)
    mid_index = n // 2

    # THE FLAW: This logic assumes 'numbers' is sorted, but it never sorts it.
    # For input [10, 2, 5], it returns 2. The correct median is 5.
    if n % 2 == 1:
        return numbers[mid_index]
    else:
        return (numbers[mid_index - 1] + numbers[mid_index]) / 2


# Example usage for testing
data = [10, 2, 5]
result = calculate_median(data)
print(f"Calculated Median: {result}")
