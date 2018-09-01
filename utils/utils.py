from datetime import datetime
from collections import Counter


def find_between(s, start, end):
    return (s.split(start))[1].split(end)[0]


def getdate(time):
    """
    Returns datetime taking an Event's TimeCreated field as input.
    Need to refactor, this is brute force.
    """
    try:
        return datetime.strptime(time, '%m/%d/%Y %I:%M:%S %p')
    except:
        try:
            return datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
        except:
            try:
                return datetime.strptime(time, '%d/%m/%Y %H:%M:%S %p')
            except:
                try:
                    return datetime.strptime(time, '%d.%m.%Y %H:%M:%S')
                except:
                    return datetime.strptime(time, '%d.%m.%Y %I:%M:%S %p')

def getlogontype(type):

    if type == "2":
        return "Interactive"
    elif type == "3":
        return "Network"
    elif type == "4":
        return "Batch"
    elif type == "5":
        return "Service"
    elif type == "7":
        return "Unlock"
    elif type == "8":
        return "NetworkClearText"
    elif type == "9":
        return "RunAs"
    elif type == "10":
        return "RemoteInteractive"
    elif type == "11":
        return "CachedInteractive"
    else:
        return type

### NGRAM ANALYSIS
### Credits to Nelson Santos

def _cleanup(s):
    """Utility function to remove unwanted characters."""
    unwanted_chars = '-_=+()[]{}.'
    return s.translate({ord(c): None for c in unwanted_chars})

def _pre_process(line):
    """Convert the line to all lowercase and splits them on spaces."""
    for word in line.split():
        yield _cleanup(word)

def _n_grams(n, s):
    """Convert a string into an iterator of n_gram strings."""
    return map(''.join, zip(*[s.lower()[i:] for i in range(n)]))

def calculate_weights(n, corpus):
    """Calculate the weights dictionary for a specific n_gram size."""
    return Counter(n_gram
                   for line in corpus
                   for s in _pre_process(line)
                   for n_gram in _n_grams(n, s))

def score(n, s, weights):
    """Assigns a score to a string for a specific n_gram size based on a weights dictionary."""
    return sum(weights[ng] for ng in _n_grams(n, s))/len(s)

