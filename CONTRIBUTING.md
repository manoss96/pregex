
Contributing to pregex
============================

There are two main ways to contribute to pregex:

1. **Bug Hunting**: It is more probable than not that there are currently 
   a number of bugs silently waiting to be discovered! If you happen to stumble
   upon one of them while using pregex, please raise an issue labeled as **bug**,
   in which you report your findings as well as explain how one can reproduce
   the bug. Furthermore, if you're up for a challenge you can even create a
   new branch just for the issue and try to tackle the problem yourself!

2. **Propose an addition/modification**: Everything good can be even better!
   If you have an idea that you think might improve pregex, you can raise an
   issue labeled as **enhancement**, in which you discuss your idea.

You can raise an issue by visiting the [Issues Page][issues-page].

Setting up a development environment
-------------------------------------
Regardless of whether you want to work on fixing a bug or implementing a new feature,
you should be able to set up a separate development environment just for pregex. The
fastest way to do this would be the following:

1. Either clone or download the "pregex" repository to your local machine.
2. Add the path pointing to the project's "src" directory on your local machine to the "PYTHONPATH" environmental variable.
	- Make sure that "PYTHONPATH" is included in "PATH" as well.
3. Create and activate a new Python 3.9 environment that you will use solely for development purposes regarding pregex.
	- Make sure that you don't pip install pregex on this environment.

After doing the above, you should be good to go!

Running the tests
-------------------------------------
For a pull request to be merged, it is important that it passes all tests defined
within the project. In order to ensure that, you can run the tests yourself by
simply going into the project's "tests" directory and executing the following
command:
```
python3 -m unittest
```
Make sure that you've set up your development environment as explained in the
corresponding section or else it is very likely that the above command will fail.


Code of Conduct
---------------

Please be nice to each other and abide by the principles of the [Python Software Foundation][psf-coc].

<!-- MARKDOWN LINKS & IMAGES -->
[issues-page]: https://github.com/manoss96/pregex/issues
[psf-coc]: https://www.python.org/psf/codeofconduct/