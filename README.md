
[//]: # (Mixture of GitHub markdown and HTML. HTML is needed for formatting.)

***
<div align=center> <h2>
GabbieBot: A simple chat bot
</h2> </div>

<div align=center> <h4> By: Eric G. Kratz </h4> </div>

***

### GabbieBot

[![GPL license](https://img.shields.io/badge/license-GPLv3-blue.svg?style=flat)](https://github.com/kratman/ChatBot/blob/master/src/GPL_LICENSE)

### Build tests

**Travis CI build:** [![Build Status](https://travis-ci.org/kratman/ChatBot.svg?branch=master)](https://travis-ci.org/kratman/ChatBot)

### Introduction

Gabbie is a simple artifical intelligence (i.e. a chat bot) for learning
and teaching machine learning techniques.

Gabbie uses a Markov chain model to mimic the speech patterns in books.
Markov chain models use the previous words to predict the next word in
the sentence. Gabbie can use the previous two words or the previous three
words to pick the next word. Additionally, Gabbie prefers to use words which
appear more frequently in the books.

Markov chains algorithms are relatively easy to design, but they are very
sensitive to the input source and the number of words in the chain. One of the
primary advantages of the algorithm is that allows Gabbie to asily learn any
language.

### Installation

To install GabbieBot, clone the git repository:
```
user:$ mkdir GabbieBot
user:$ git clone https://github.com/kratman/ChatBot.git ./GabbieBot/
```

The Makefile can produce both the documentation and the binaries.
```
user:$ make install
```

### Training

Gabbie can be taught to speak using plain text books and lists of canned
responses.
```
user:$ TrainGabbie BookFileName <...>
```
Note: <...> represents additional books which are optional to include.

Gabbie will also learn as users interact with her; through conversations or
by playing twenty questions. After training, Gabbie's memories are stored in
the Knowledge directory. Gabbie can be forced to forget by running the
"GabbieForget" script or by manually removing the memory text files.

### Usage

The simplest way to interact with Gabbie is to call the RunGabbie script from
the command line.
```
 user:$ ./bin/RunGabbie

  or

 user:$ ./bin/RunGabbie "<...>"
```
Note: The <...> can be replaced with any input string, but the quotes
are required.
