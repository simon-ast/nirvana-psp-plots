def dqf_conversion(dqf_array):
    """DOC!!"""
    bad_indicies = []

    for i in range(len(dqf_array)):
        # True if designated bits are active, False otherwise
        bad_index = entry_handling(dqf_array[i], i)

        if bad_index is not None:
            bad_indicies.append(bad_index)


def entry_handling(dqf_array_entry, entry_index):
    """DOC!"""
    # DESCRIBE THIS!
    twobyte_int = format(dqf_array_entry, "b").zfill(16)
    twobyte_list = list(twobyte_int)

    # Check by bit engagement
    # TODO: this needs to be updated
    bad_bit = [0, 8, 10]

    # DESCRIBE THIS
    for ind in bad_bit:
        if twobyte_list[:- (ind + 1)] == 1:
            return entry_index
        else:
            pass

    return None

