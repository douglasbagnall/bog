Author identification using multi-headed recurrent neural networks
==================================================================

This software was developed for the [PAN] 2015 [author identification]
challenge.

[pan]: http://pan.webis.de/
[author identification]: http://www.uni-weimar.de/medien/webis/events/pan-15/pan15-web/author-identification.html

It uses a multi-headed recurrent neural network (RNN) from the [recur]
project. The recur module is in the form of a Python extension, and to
build it you need to have various packages listed in the recur README,
and the python-dev package. `make charmodel.so` is supposed to work.

[recur]: https://github.com/douglasbagnall/recur

This software is copyright Douglas Bagnall and is licensed under the
GPL, version 2 or greater.
