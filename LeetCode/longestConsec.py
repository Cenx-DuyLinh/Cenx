nums = [2, 1, 3, 5, 100, 200, 6, 7, 8, 9]
numSet = set(nums)
longest = 0

for n in numSet:
    # check if its the start of a sequence
    if (n - 1) not in numSet:
        length = 1
        while (n + length) in numSet:
            length += 1
        longest = max(length, longest)

print(longest)
