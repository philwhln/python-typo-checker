import itertools
import tokenize
import sys
import keyword

# Function borrowed from: norvig.com/spell-correct.html
# Copyright, Peter Norvig

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

# end of Peter Norving code

def get_names(filename):
    readline = open(filename).readline
    return set(token[1] for token in tokenize.generate_tokens(readline)
            if token[0] == 1 and not token[1] in keyword.kwlist)

def are_similar(word1, word2):
    if word1 == word2:
        return True
    return word1 in edits(word2)

def input_restricted(prompt, correct_input):
    acceptable = False
    while True:
        response = raw_input(prompt)
        if response in correct_input:
            return response

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except:
        print "Usage: python check.py [file]"
        sys.exit(0)

    corrected = open(filename).read()
    names = filter(lambda w: len(w) > 2, get_names(filename))
    
    while True:
        corrections = 0
        
        try:
            name = names.pop()
        except:
            break
        
        similar = set(other for other in names if are_similar(name, other))
        if len(similar) > 1:
            replaced_words = []
            def replaced(w):
                return w in replaced_words
            for a, b in itertools.combinations(similar, 2):
                if not any(map(replaced, [a,b])):
                    response = input_restricted('Found similar [a: %s, b: %s], pick a, b or RETURN to skip: ' %
                                                (a, b), ['a', 'b', ''])
                    if response:
                        correct = a if response == 'a' else b
                        incorrect = b if response == 'a' else a
                        corrected = corrected.replace(incorrect, correct)
                        corrections += 1

    if corrections:
        output = '%s_corrected.py'
        open(output % filename.split('.')[0], 'w').write(corrected)
        print 'Done! Generated %s' % output
    else:
        print 'Done! You made no corrections.'

