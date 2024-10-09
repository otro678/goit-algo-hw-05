def binary(array, target):
    low, high = 0, len(array) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        
        if array[mid] == target:
            return (iterations, array[mid])
        
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            upper_bound = array[mid]
    
    if upper_bound is None and low < len(array):
        upper_bound = array[low]
    
    return (iterations, upper_bound)

sorted_array = [1.2, 3.4, 5.5, 6.6, 7.6, 8.8, 10.1, 12.5]
target_value = 7.0

result = binary(sorted_array, target_value)
print(result) 