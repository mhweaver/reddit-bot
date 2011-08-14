import pickle
import time
import reddit
import markov

class markovWrapper:
    ''' This is just to make dealing with the markov object slightly easier.
        
        I really don't want to have to think too hard about stuff like saving
        and loading the markov object in my main() function.
    '''
    def __init__(self, path='.markov', order=3):
        self._load(path, order)
    def _load(self, path, order):
        try:
            f = open(path, 'rb')
            self.markov = pickle.load(f)
            self.markov.order = order
            f.close()
        except:
            print 'Unable to load existing Markov dict. Creating a new one.'
            self.markov = markov.MarkovChain(order=order)
    
    def save(self, path='.markov'):
        with open(path, 'wb') as f:
            pickle.dump(self.markov, f, pickle.HIGHEST_PROTOCOL)
            
    def add_comments(self, comments):
        for comment in comments:
            self.markov.add(comment.body.split(" "))
            
    def output(self):
        return " ".join(self.markov.random_output())

def main():
    r = reddit.Reddit(user_agent="markov_comment_generator")
    my_markov = markovWrapper(path='.markov', order=3)
    
    print "Size of markovWrapper:", len(my_markov.markov)
        
    comments = r.get_all_comments(limit=100, place_holder=None)
    my_markov.add_comments(comments)
    
    print my_markov.output()
    my_markov.save()
if __name__ == '__main__':
    main()