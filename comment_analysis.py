import praw

# Used to count recursive calls to checkComments
class Counter(object) :
    def __init__(self, fun) :
        self._fun = fun
        self.counter=0
    def __call__(self,*args, **kwargs) :
        self.counter += 1
        return self._fun(*args, **kwargs)

# Used to recursively grab replies to comments
def checkComments(comment,com_count):
    for comment in comment.replies:
        print "\t"*com_count,
        print "%s" % comment
        checkComments(comment,com_count+1)

checkComments = Counter(checkComments)

user_agent = ("comment analysis by grasbergerm - https://github.com/grasbergerm/reddit-comment-analysis")
r = praw.Reddit(user_agent=user_agent)
subreddit = r.get_subreddit('drunk')
post = r.get_submission(submission_id='2j92q0')
orig_comment = 0
for comment in post.comments:
    orig_comment += 1
    print "-%s\n" % comment
    com_count = 0
    print checkComments(comment,com_count)
    print checkComments.counter - orig_comment
print orig_comment
