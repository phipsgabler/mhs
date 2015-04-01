# Purpose #

I wrote this script for a university lecture I've taken, because I didn't find anything to calculate hitting sets
automatically. Maybe they're just unheard of, mostly.

Since at the time of writing I only ever had to work with quite small sets, the implementation does not
use any optimized algorithm -- I only translated the definitions into (declarative) Python code. The usage
of power sets introduces exponential complexity; however, this didn't become a practical problem for me yet.

This script requires Python 3; specifically, version 3.3 due to the use of a
[subgenerator delegation](https://www.python.org/dev/peps/pep-0380/). If you want to use an earlier version, change
line 42 (containing `yield from`) to `for y in xs: yield y` (yes, I am stubborn when it comes to language
features I like ;))

## Recap of Definitions ##

In case you're interested in using this, you should know this already, but anyway:

- A hitting set for a set of sets M is a set H such that for each m ∈ M, m ∩ H ≠ ∅; that is,
for each of the sets, at least one element is present in H.
- A hitting set is called minimal if it does not contain any other hitting set.


# Using the script #

The command line interface is implemented by simply passing `argv` to the `mhs` function. Thus, every
separated argument is treated as a set of characters (this means that names of individuals are always
one character long). The output separates sets by newlines and individuals by `,`.

Examples:

```
> ./mhs/mhs.py 12 23
2
1,3

> ./mhs/mhs.py abc bdc
c
b
d,a
```


# Using the functions #

There are two functions of interest in `mhs`: `hitting_sets`, which returns all hitting sets of a set of sets, and
`mhs`, which returns all minimal hitting sets. Both are designed to work as seamlessly as possible with all kinds of
arguments, and take either one iterable of iterables or multiple iterables as arguments (so there's no need to
splice arguments or for an extra function).

Internally, everything is converted to a set of frozensets, so the only assumption on the arguments is that
they are finite iterables of hashable types.

Examples:

```python
> mhs.hitting_sets('123', '234')
{frozenset({'1', '2', '4'}),
 frozenset({'3'}),
 frozenset({'3', '4'}),
 frozenset({'1', '3'}),
 frozenset({'2'}),
 frozenset({'1', '2'}),
 frozenset({'2', '3'}),
 frozenset({'1', '2', '3'}),
 frozenset({'2', '4'}),
 frozenset({'2', '3', '4'}),
 frozenset({'1', '4'}),
 frozenset({'1', '3', '4'}),
 frozenset({'1', '2', '3', '4'})}

> mhs.mhs('123', '234')  # multiple strings
{frozenset({'2'}), frozenset({'1', '4'}), frozenset({'3'})}

> mhs.mhs('12', ('2','3'))  # a string and some other iterable
{frozenset({'2'}), frozenset({'1', '3'})}

> mhs.mhs(x for x in [iter('12'), '23', ('a', '1')]})  # weird combination of generators
{frozenset({'2', 'a'}), frozenset({'1', '2'}), frozenset({'1', '3'})}

```


