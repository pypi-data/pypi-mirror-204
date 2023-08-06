Since the repo from [here](https://github.com/camillo/yaypm) was not maintained, we set up this new repo. 

The new name `yaypm3` is reflecting our support for python v3.
***

This lib was written by Maciek Kaminski.

I ported it to python3 and hacked a few things.

#YAYPM - Yet Another Yate Python Module. 
It allows to write YATE modules in PYTHON. PYTHON modules comunicate with YATE core via external protocol or run in python interperter embedded in pymodule.

Base concept
YAYPM base concept - deferred - comes from Twisted framework. Twisted project is very well documented, so look there for in-depth explanations of deferreds and its asynchronous programming model, as it won't be repeated here.
For the needs of this tutorial it is enough to say that, deferred is a promise to carry a computation in case of occurence of a specified event. What will be computed is defined by adding success and failure callbacks.
YAYPM allows to create deferreds for specified YATE messages.