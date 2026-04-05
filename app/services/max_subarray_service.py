def max_subarray(arr):
    if not arr:
        return {}

    max_sum = arr[0]
    current = arr[0]
    start = end = temp_start = 0

    for index in range(1, len(arr)):
        if arr[index] > current + arr[index]:
            current = arr[index]
            temp_start = index
        else:
            current += arr[index]

        if current > max_sum:
            max_sum = current
            start = temp_start
            end = index

    return {
        "max_sum": max_sum,
        "start_index": start,
        "end_index": end,
    }
