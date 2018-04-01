# From codereview.stackexchange.com
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b

def get_partitions(set_):
    """
    takes as input a list and returns a generator that contains
    all the possible partitions of this list, from 0-partitions
    to n-partitions, where n is the length of this list
    """
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]
