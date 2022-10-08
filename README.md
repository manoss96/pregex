<!-- PROJECT BADGES -->
[![Python Version][python-shield]][python-url]
[![MIT License][license-shield]][license-url]
[![Coverage][coverage-shield]][coverage-url]

<!-- What is PRegEx? -->
## What is PRegEx?

Let's face it, although RegEx is without a doubt an extremely useful tool, its syntax has been repeatedly proven to be quite hard for people to read and to memorize. This is mainly due to RegEx's declarative nature, which many programmers are not familiar with, as well as its extensive use of symbols that do not inherently relate to their functionality within a RegEx pattern, thus making them easy to forget. To make matters even worse, RegEx patterns are more often than not tightly packed with large amounts of information, which our brains just seem to be struggling to break down in order to analyze effectively. For these reasons, building even a simple RegEx pattern for matching URLs can be quite a painful task for many people.

This is where PRegEx comes in! PRegEx, which stands for Programmable Regular Expressions, is a Python package that can be used in order to construct Regular Expression patterns in a more human-friendly way. Through the use of PRegEx, one is able to fully utilize the powerful tool that is RegEx without having to deal with any of its nuisances that seem to drive people crazy! PRegEx achieves that by offering the following:

1. An easy-to-remember syntax that resembles the good ol' imperative way of programming!
2. No longer having to group patterns or escape meta characters, as both are handled internally by PRegEx!
3. Modularity to building RegEx patterns, as one can easily break down a complex pattern into multiple simpler ones which can then be combined together.
4. A higher-level API on top of Python's built-in "re" module, providing access to its core functionality and more, while saving you the trouble of having to deal with "re.Match" instances.

And remember, no matter how complex the abstraction, it's always just a pure RegEx pattern that sits underneath which you can fetch and use any way you like!


<!-- Installation -->
## Installation

You can start using PRegEx by installing it via pip. Note that "pregex" requires Python >= 3.9.

```sh
pip install pregex
```


<!-- Usage example -->
## Usage Example

In PRegEx, everything is a Programmable Regular Expression, or "Pregex" for short. This makes it easy for simple Pregex instances to be combined into more complex ones! Within the code snippet below, we construct a Pregex instance that will match any URL that ends with either ".com" or ".org" as well as any IP address for which a 4-digit port number is specified. Furthermore, in the case of a URL, we would like for its domain name to be separately captured as well.

```python
from pregex.core.classes import AnyLetter, AnyDigit, AnyFrom
from pregex.core.quantifiers import Optional, AtLeastAtMost
from pregex.core.operators import Either
from pregex.core.groups import Capture
from pregex.core.pre import Pregex

# Define main sub-patterns.
http_protocol = Optional('http' + Optional('s') + '://')

www = Optional('www.')

alphanum = AnyLetter() | AnyDigit()

domain_name = \
    alphanum + \
    AtLeastAtMost(alphanum | AnyFrom('-', '.'), n=1, m=61) + \
    alphanum

tld = '.' + Either('com', 'org')

ip_octet = AnyDigit().at_least_at_most(n=1, m=3)

port_number = (AnyDigit() - '0') + 3 * AnyDigit()

# Combine sub-patterns together.
pre: Pregex = \
    http_protocol + \
    Either(
        www + Capture(domain_name) + tld,
        3 * (ip_octet + '.') + ip_octet + ':' + port_number
    )
```

We can then easily fetch the resulting Pregex instance's underlying RegEx pattern.
```python
regex = pre.get_pattern()
```

This is the pattern that we just built. Yikes!
```
(?:https?:\/\/)?(?:(?:www\.)?([A-Za-z\d][A-Za-z\d\-.]{1,61}[A-Za-z\d])\.(?:com|org)|(?:\d{1,3}\.){3}\d{1,3}:[1-9]\d{3})
```

Besides from having access to its underlying pattern, we can use a Pregex instance to find matches within a piece of text. Consider for example the following string:
```python
text = "text--192.168.1.1:8000--text--http://www.wikipedia.org--text--https://youtube.com--text"
```
By invoking the instance's "get_matches" method, we are able to scan the above string for any possible matches:
```python
matches = pre.get_matches(text)
```

Looks like there were three matches:
```python
['192.168.1.1:8000', 'http://www.wikipedia.org', 'https://youtube.com']
```

Likewise, we can invoke the instance's "get_captures" method to get any captured groups.
```python
groups = pre.get_captures(text)
```
As expected, there were only two captured groups since the first match is not a URL and therefore it does not contain a domain name to be captured.
```python
[(None,), ('wikipedia',), ('youtube',)]
```

Finally, you might have noticed that we built our pattern by utilizing
various classes that were imported from modules under *pregex.core*. These
modules contain classes through which the RegEx syntax is essentially replaced.
However, PRegEx also includes another set of modules, namely those under
subpackage *pregex.meta*, whose classes build upon those in *pregex.core* so
as to provide numerous pre-built patterns that you can just import and use
right away!

```python

from pregex.core.pre import Pregex
from pregex.core.classes import AnyDigit
from pregex.core.operators import Either
from pregex.meta.essentials import HttpUrl, IPv4

port_number = (AnyDigit() - '0') + 3 * AnyDigit()

pre: Pregex = Either(
    HttpUrl(capture_domain=True, is_extensible=True),
    IPv4(is_extensible=True) + ':' + port_number
)
```

By using classes found within the *pregex.meta* subpackage, we were able to
construct more or less the same pattern as before only much more easily!

## Solving Wordle with PRegEx

We are now going to see another example that better exhibits the *programmable* nature of PRegEx.
More specifically, we will be creating a Wordle solver function that, given all currently known
information as well as access to a 5-letter word dictionary, utilizes PRegEx in order to return
a list of candidate words to choose from as a possible solution to the problem.

### Formulating what is known

First things first, we must think of a way to represent what is known so far regarding the
word that we're trying to guess. This information can be encapsulated into three distinct
sets of letters:

1. **Green letters**: Letters that are included in the word, whose position within it is known.
2. **Yellow letters**: Letters that are included in the word, and while their exact position is
   unknown, there is one or more positions which we can rule out. 
3. **Gray letters**: Letters that are not included in the word.

Green letters can be represented by using a dictionary that maps integers (positions) to strings (letters).
For example, ``{4 : 'T'}`` indicates that the word we are looking for contains the letter ``T`` in its
fourth position. Yellow letters can also be represented as a dictionary with integer keys, whose values
however are going to be lists of strings instead of regular strings, as a position might have been ruled
out for more than a single letter. For example, ``{1 : ['A', 'R'], 3 : ['P']}`` indicates that even though
the word contains letters ``A``, ``R`` and ``P``, it cannot start with either an ``A`` or an ``R`` as
well as it cannot have the letter ``P`` occupying its third position. Finally, gray letters can be simply
stored in a list.

In order to have a concrete example to work with, we will be assuming that our current
information about the problem is expressed by the following three data structures:

```python
green: dict[int, str] = {4 : 'T'}
yellow: dict[int, list[str]] = {1 : ['A', 'R'], 3 : ['P']}
gray: list[str] = ['C', 'D', 'L', 'M', 'N', 'Q', 'U']
```

### Initializing a Pregex class instance

Having come up with a way of programmatically formulating the problem, the first step towards
actually solving it would be to create a ``Pregex`` class instance:
```python
wordle = Pregex()
```

Since we aren't providing a ``pattern`` parameter to the class's constructor, it automatically
defaults to the empty string ``''``. Thus, through this instance we now have access to all methods
of the ``Pregex`` class, though we are not really able to match anything with it yet.

### Yellow letter assertions

Before we go on to dictate what the valid letters for each position within the word
are, we are first going to deal with yellow letters, that is, letters which we know are
included in the word that we are looking for, though their position is still uncertain.
Since we know for a fact that the sought out word contains these letters, we have to
somehow make sure that any candidate word includes them as well. This can easily be
done by using what is known in RegEx lingo as a *positive lookahead assertion*,
represented in PRegEx by the less intimidating *FollowedBy*! Assertions are used in
order to *assert* something about a pattern without really having to *match* any additional
characters. A positive lookahead assertion, in particular, dictates that the pattern to which
it is applied must be followed by some other pattern in order for the former to constitute
a valid match.

In PRegEx, one is able to create a ``Pregex`` instance out of applying a positive
lookahead assertion to some pattern ``p1`` by doing the following:

```python
from pregex.core.assertions import FollowedBy

pre = FollowedBy(p1, p2)
```

where both ``p1`` and ``p2`` are either strings or ``Pregex`` instances. Futhermore, in the
case that ``p1`` already is a ``Pregex`` class instance, one can achieve the same result with:

```python
pre = p1.followed_by(p2)
```

Having initialized ``wordle`` as a ``Pregex`` instance, we can simply simply do
``wordle.followed_by(some_pattern)`` so as to indicate that any potential match
with ``wordle`` must be followed by ``some_pattern``. Recall that ``wordle`` merely
represents the empty string, so we are not really matching anything at this point.
Applying an assertion to the empty string pattern is just a neat little trick one
can use in order to validate something about their pattern before they even begin
to build it.

Now it's just a matter of figuring out what the value of ``some_pattern`` is.
Surely we can't just do ``wordle = wordle.followed_by(letter)``, as this results
in ``letter`` always having to be at the beginning of the word. Here's however what
we can do: It follows from the rules of Wordle that all words must be comprised of five
letters, any of which is potentially a yellow letter. Thus, every yellow letter is certain
to be preceded by up to four other letters, but no more than that. Therefore, we need a
pattern that represents just that, namely *four letters at most*. By applying quantifier
``at_most(n=4)`` to an instance of ``AnyUppercaseLetter()``, we are able to create such
a pattern. Add a yellow letter to its right and we have our ``some_pattern``. Since there
may be more than one yellow letters, we make sure that we iterate them all one by one so
as to enforce a separate assertion for each:

```python
from pregex.core.classes import AnyUppercaseLetter

yellow_letters_list: list[str] = [l for letter_list in yellow.values() for l in letter_list]

at_most_four_letters = AnyUppercaseLetter().at_most(n=4)

for letter in yellow_letters_list:
    wordle = wordle.followed_by(at_most_four_letters + letter)
```

By executing the above code snippet we get a ``Pregex`` instance which
represents the following RegEx pattern:

```
(?=[A-Z]{,4}A)(?=[A-Z]{,4}R)(?=[A-Z]{,4}P)
```

### Building valid character classes

After we have made sure that our pattern will reject any words that do not contain
all the yellow letters, we can finally start building the part of the pattern that
will handle the actual matching. This can easily be achived by performing five
iterations, one for each letter of the word, where at each iteration ``i`` we
construct a new character class, which is then appended to our pattern based
on the following logic:

* If the letter that corresponds to the word's i-th position is known, then
  make it so that the pattern only matches that letter at that position.

* If the letter that corresponds to the word's i-th position is not known,
  then make it so that the pattern matches any letter except for gray letters,
  green letters, as well as any yellow letters that may have been ruled out for
  that exact position.

The following code snippet does just that:

```python
from pregex.core.classes import AnyFrom

for i in range(1, 6):
    if i in green:
        wordle += green[i]
    else:
        invalid_chars_at_pos_i = gray + list(green.values())
        if i in yellow:
            invalid_chars_at_pos_i += yellow[i]
        wordle += AnyUppercaseLetter() - AnyFrom(*invalid_chars_at_pos_i)
```

After executing the above code, ``wordle`` will contain the following
RegEx pattern:

```
(?=[A-Z]{,4}A)(?=[A-Z]{,4}R)(?=[A-Z]{,4}P)[BE-KOPSV-Z][ABE-KOPRSV-Z][ABE-KORSV-Z]T[ABE-KOPRSV-Z]
```

### Matching from a dictionary

Having built our pattern, the only thing left to do is to actually use it to
match candidate words. Provided that we have access to a text file containing
all possible Wordle words, we are able to invoke our ``Pregex`` instance's
``get_matches`` method in order to scan said text file for any potential matches. 

```python
words = wordle.get_matches('word_dictionary.txt', is_path=True)
```

### Putting it all together

Finally, we combine together everything we discussed into a single function that
spews out a list of words which satisfy all necessary conditions so that they
constitute possible solutions to the problem.

```python
def wordle_solver(green: dict[int, str], yellow: dict[int, list[str]], gray: list[str]) -> list[str]:

    from pregex.core.pre import Pregex
    from pregex.core.classes import AnyUpperCaseLetter, AnyFrom

    # Initialize pattern as the empty string pattern.
    wordle = Pregex()

    # This part ensures that yellow letters
    # will appear at least once within the word.
    yellow_letters_list = [l for letter_list in yellow.values() for l in letter_list]
    at_most_four_letters = AnyUppercaseLetter().at_most(n=4)
    for letter in yellow_letters_list:
        wordle = wordle.followed_by(at_most_four_letters + letter)

    # This part actually dictates the set of valid letters
    # for each position within the word.
    for i in range(1, 6):
        if i in green:
            wordle += green[i]
        else:
            invalid_chars_at_pos_i = gray + list(green.values())
            if i in yellow:
                invalid_chars_at_pos_i += yellow[i]
            wordle += AnyUppercaseLetter() - AnyFrom(*invalid_chars_at_pos_i)

    # Match candidate words from dictionary and return them in a list.
    return wordle.get_matches('word_dictionary.txt', is_path=True)
```

By invoking the above function we get the following list of words:

```python
word_candidates = wordle_solver(green, yellow, gray)

print(word_candidates) # This prints ['PARTY']
```

Looks like there is only one candidate word, which means that we
can consider our problem solved!

You can learn more about PRegEx by visiting the [PRegEx Documentation Page][docs-url].


<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/python-3.9+-blue
[python-url]: https://www.python.org/downloads/release/python-390/
[license-shield]: https://img.shields.io/badge/license-MIT-brightgreen
[license-url]: https://github.com/werden-wissen/pregex/blob/master/LICENSE.txt
[coverage-shield]: https://coveralls.io/repos/github/manoss96/pregex/badge.svg?branch=main&service=github
[coverage-url]: https://coveralls.io/github/manoss96/pregex?branch=main
[docs-url]: https://pregex.readthedocs.io/en/latest/