<!-- PROJECT BADGES -->
[![Python Version][python-shield]][python-url]
[![MIT License][license-shield]][license-url]

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
## Usage example

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

port_number = 4 * AnyDigit()

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
(?:https?:\/\/)?(?:(?:www\.)?([A-Za-z\d][A-Za-z\d\-.]{1,61}[A-Za-z\d])\.(?:com|org)|(?:\d{1,3}\.){3}\d{1,3}:\d{4})
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

port_number = 4 * AnyDigit()

pre: Pregex = Either(
    HttpUrl(capture_domain=True),
    IPv4() + ":" + port_number
)
```

By using classes found within the *pregex.meta* subpackage, we were able to
construct more or less the same pattern as before only much more easily!

You can learn more about PRegEx by visiting the [PRegEx Documentation Page][docs-url].


<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/python-3.9+-blue
[python-url]: https://www.python.org/downloads/release/python-390/
[license-shield]: https://img.shields.io/badge/license-MIT-brightgreen
[license-url]: https://github.com/werden-wissen/pregex/blob/master/LICENSE.txt
[docs-url]: https://pregex.readthedocs.io/en/latest/