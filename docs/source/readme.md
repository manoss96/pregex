(about-pregex)=

# About PRegEx

This page serves as a quick introduction to the PRegEx package.


<!-- What is PRegEx? -->
## What is PRegEx?

Let's face it, although RegEx is without a doubt an extremely useful tool, its syntax has been repeatedly proven to be quite hard for people to read and to memorize. This is mainly due to RegEx's declarative nature, which many programmers are not familiar with, as well as its extensive use of symbols that do not inherently relate to their functionality within a RegEx pattern, thus making them hard to remember. To make matters even worse, RegEx patterns are more often than not tightly packed with large amounts of information, which our brains just seem to be struggling to break down in order to analyze effectively.

For the above reasons, building even a simple RegEx pattern for matching URLs can be quite a painful task for many people. This is where PRegEx comes in! PRegEx, which stands for Programmable Regular Expressions, is a Python package that can be used in order to construct Regular Expression patterns in a more human-friendly way. Through the use of PRegEx, one is able to fully utilize the powerful tool that is RegEx without having to deal with any of its nuisances that seem to drive people crazy! PRegEx achieves that by offering the following:

1. An easy-to-remember syntax that resembles the good ol' imperative way of programming!
2. Adds modularity to building RegEx patterns, as you can easily break down a complex pattern into simpler sub-patterns which can then be combined together.
3. No longer having to escaping meta characters such as "." and "*" as this is handled internally by PRegEx!
4. Acts as a higher-level API on top of Python's built-in "re" module, providing access to its core functionality while saving you the trouble of having to deal with "re.Match" instances.
5. No matter how complex the abstraction, it's always just a pure RegEx pattern that sits underneath which you can fetch and use any way you like!


<!-- Installation -->
## Installation

You can start using PRegEx by simply installing it via pip:

```sh
pip install pregex
```


<!-- Usage example -->
## Usage example

In PRegEx, everything is a Programmable Regular Expression, or "Pregex" for short. This makes it easy for simple Pregex instances to be combined into more complex ones! Within the code snippet below, we construct a Pregex instance that will match any URL that ends with either ".com" or ".org" as well as any IP address for which a 4-digit port number is specified. Furthermore, in the case of a URL, we would like for its domain name to be separately captured as well.

```python
from pregex.quantifiers import Optional, AtLeastOnce, AtLeastAtMost
from pregex.classes import AnyButWhitespace, AnyButFrom, AnyDigit
from pregex.groups import CapturingGroup
from pregex.tokens import Backslash
from pregex.operators import Either
from pregex.pre import Pregex

pre: Pregex = \
        Optional("http" + Optional('s') + "://") + \
        Optional("www.") + \
        Either(
            CapturingGroup(
                AtLeastOnce(AnyButWhitespace() | AnyButFrom(":", Backslash()))
            ) +
            Either(".com", ".org"),

            3 * (AtLeastAtMost(AnyDigit(), min=1, max=3) + ".") +
            1 * AtLeastAtMost(AnyDigit(), min=1, max=3) +
            ":" + 4 * AnyDigit() 
        )
```

We can then easily fetch the resulting Pregex instance's underlying RegEx pattern.
```python
regex = pre.get_pattern()
```

This is the pattern that we just built. Yikes!
```
(?:https?\:\/\/)?(?:www\.)?(?:([^\s\:\\]+)(?:\.com|\.org)|(?:\d{1,3}\.){3}\d{1,3}\:\d{4})
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
As expected, there were only two captured groups since the first match is not a URL and therefore it does not contain a domain name to be captured.
```python
[(None,), ('wikipedia',), ('youtube',)]
```

You can learn more about how PRegEx works by reading the documentation or by directly cloning the [PRegEx Github repository][repo-url] to play around with.


<!-- What to expect next? -->
## What to expect next?

Currently, the pregex package's core modules are still being built. In the near future, more modules will follow that will rely upon the package's core modules in order to provide abstractions for even more complex RegEx patterns!

<!-- MARKDOWN LINKS & IMAGES -->
[repo-url]: https://github.com/manoss96/pregex