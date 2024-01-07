from functools import cache


@cache
def num_possible_arrays(string: str, nums: str, base_level=True) -> int:
    num = 0
    # Split the nums into a list of ints
    # Use of a string argument `nums` to allow caching
    nums = [int(x) for x in nums.split(",")] if nums else []

    # End of a recursion - empty contiguous integer list
    # So return 1 if there are no further `#` characters
    # in remaining string (valid solution), and return 0
    # if there are `#` characters (invalid solution)
    if nums == []:
        return not any([c == "#" for c in string])

    # The ends of the string can be fiddly to deal with.
    # Padding with `.` characters does not affect the solution
    # but avoids special cases for ends of original string
    if base_level:
        string = "." + string + nums[-1] * "."

    # Loop from nidex 1: skip first character, as there must be
    # a gap between contiguous blocks. On first iteration,
    # there is an extra '.' character prepended
    # Loop until len(string) - nums[0]: block of length nums[0]
    # must fit into remaining string for a valid solution
    for i in range(1, len(string) - nums[0]):
        char = string[i]

        if char in ["#", "?"]:
            # Conditions to check if block can start here
            # First condition: all nums[0] next characters are '#' or '?'
            condition_1 = all([c in ["#", "?"] for c in string[i : i + nums[0]]])

            # Second condition: the character after the next nums[0]
            # characters cannot be a '#' (must be a gap between blocks)
            condition_2 = string[i + nums[0]] != "#"

            # Third condition: Previous character cannot be a '#'
            # for a similar reason
            condition_3 = string[i - 1] != "#"

            if all([condition_1, condition_2, condition_3]):
                # Convert back to string
                next_nums = ",".join([str(x) for x in nums[1:]])

                # Recurse on remaining string after block, with one fewer
                # remaining block to consider
                num += num_possible_arrays(string[i + nums[0] :], next_nums, False)

        # Once a '#' character is hit, the next block must start here
        if char == "#":
            break

    return num


def unfold_input(array: str, nums: str, factor: int = 5) -> tuple[str]:
    arrays = factor * [array]
    nums = factor * [nums]
    return ("?".join(arrays), ",".join(nums))
