#!/usr/bin/env python3


__doc__ = """Yes, it is slow. But sufficient for small sets.
Usage from python:

  > import mhs
  > list(mhs.mhs({9,1}, {2,3,6,9,0}))
  [frozenset({9}),
   frozenset({2, 1}),
   frozenset({3, 1}),
   frozenset({6, 1}),
   frozenset({0, 1})]

Or, as script (interpreting parameter strings as sets of characters):

  > ./mhs.py 91 23690
  9
  6,1
  0,1
  1,2
  3,1
"""


from itertools import chain, combinations
from functools import reduce
from operator import or_


# taken from itertools documentation: https://docs.python.org/3.4/library/itertools.html#itertools-recipes
def powerset(it):
    """For any finite iterable, iterate the set of all subsets."""
    xs = list(it)
    return map(frozenset, chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1)))


def _prepare_sets(sets, *rest):
    """ Turns the accepted argument format into one set of frozensets."""
    def _itercons(x, xs):
        yield x
        yield from xs  # in earlier versions you must replace this line by a loop

    return {frozenset(s) for s in (_itercons(sets, rest) if rest else sets)}


def hitting_sets(sets, *rest):
    """For given set-like objects, iterate all hitting sets.

    Expected arguments: either an enumerable of sets, or multiple sets

    A hitting set is a set which contains at least on element of each set.
    """

    all_sets = _prepare_sets(sets, *rest)

    union = reduce(or_, all_sets, set())
    # for p in powerset(union):
    #     if all(p & s for s in all_sets):
    #         yield p
    return {p for p in powerset(union) if all(p & s for s in all_sets)}


def mhs(sets, *rest):
    """For given set-like objects, iterate all minimal hitting sets.

    A hitting set is minimal if it has no proper subset which is a hitting set, too.
    """

    all_sets = _prepare_sets(sets, *rest)

    # for h in hitting_sets(all_sets):
    #     if not any(p in hitting_sets(all_sets) for p in powerset(h) if p != h):
    #         yield h

    return {h for h in hitting_sets(all_sets)
            if not any(p in hitting_sets(all_sets) for p in powerset(h) if p != h)}


def main(argv):
    """Calculates minimal hitting sets from input. Each parameter is interpreted
    as a separate set of characters (so only length 1 names are possible).
    """
    result = mhs(map(set, argv[1:]))
    for s in result:
        print(','.join(s))


if __name__ == '__main__':
    import sys
    if any(h == sys.argv[1] for h in ['--help', '-h']):
        print(__doc__)
    else:
        main(sys.argv)








