<!-- PROJECT BADGES -->
[![Contributors][python-shield]][python-url]
[![MIT License][license-shield]][license-url]

## PRegEx - Programmable Regular Expressions

PRegEx is a Python module that can be used in order to construct Regular Expression patterns in a more human-friendly way.

<!-- Installation -->
### Installation

You can start using PRegEx by installing it via pip:

```sh
pip install pregex
```


<!-- USAGE EXAMPLES -->
### Usage

In PRegEx, everything is a Programmable Regular Expression, or "Pregex" for short. This makes it easy for simple Pregex instances to be combined into more complex ones! Within the code snippet below, we construct a Pregex instance that will match any URL that ends with either ".com" or ".org" as well as any IP address for which a 4-digit port number is specified. Furthermore, in the case that a match is a URL it's domain name will be separately captured as well.

```python
from pregex.classes import AnyFrom, AnyDigit, AnyWhitespace
from pregex.quantifiers import Optional, Enforced
from pregex.groups import CapturingGroup
from pregex.tokens import Backslash
from pregex.operators import Either
from pregex.pre import Pregex

pre: Pregex = \
        Optional("http" + Optional('s') + "://") + \
        Optional("www.") + \
        Either(
            Enforced(AnyDigit() | AnyFrom(".")) +
            ":" + 
            4 * AnyDigit(),
            
            CapturingGroup(
                Enforced(~ (AnyWhitespace() | AnyFrom(":", Backslash())))
            ) +
            Either(".com", ".org")
        )
```

We can then easily fetch the resulting Pregex instance's underlying RegEx pattern.
```python
regex = pre.get_pattern()
```

This is the RegEx pattern that the above method returns. Yikes!
```python
(?:https?\:\/\/)?(?:www\.)?(?:[0-9\.]+\:[0-9]{4}|([^\r\:\n\x0c\\ \t\x0b]+)(?:\.com|\.org))
```

Besides from having access to its underlying pattern, we can use a Pregex instance to find matches within a string. Consider for example the following piece of text:
```python
text = "text--192.168.1.1:8000--text--http://www.wikipedia.orghttps://youtube.com--text"
```
We can scan the above string for any possible matches by invoking the instance's "get_matches" method:
```python
matches = pre.get_matches(text)
```

Looks like there were three matches:
```python
['192.168.1.1:8000', 'http://www.wikipedia.org', 'https://youtube.com']
```

Likewise, we can invoke the instance's "get_groups" method to get any captured groups.
```python
groups = pre.get_groups(text)
```
As expected, there were only two captured groups as the first match is not a URL and therefore there did not exist a domain name to capture.
```python
[(None,), ('wikipedia',), ('youtube',)]
```

<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/python-3.9-blue
[python-url]: https://www.python.org/downloads/release/python-390/
[license-shield]: https://img.shields.io/badge/license-MIT-brightgreen
[license-url]: https://github.com/werden-wissen/pregex/blob/master/LICENSE.txt