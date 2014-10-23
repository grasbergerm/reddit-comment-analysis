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
        if type(comment) is praw.objects.MoreComments:
            comment.comments()
        #print "\t"*com_count,
        #print "%s" % comment
        checkComments(comment,com_count+1)

checkComments = Counter(checkComments)

user_agent = ("comment analysis by grasbergerm - https://github.com/grasbergerm/reddit-comment-analysis")
r = praw.Reddit(user_agent=user_agent)
# Get the subreddit choice
subreddit = r.get_subreddit(raw_input("What subreddit? "))
# Used for a single submission
#submission = r.get_submission(submission_id='2j92q0')
for submission in subreddit.get_top_from_week(limit=10):
    submission.replace_more_comments(limit=None, threshold=0)
    #all_comments = submission.comments
    orig_comment = 0
    for comment in submission.comments:
        orig_comment += 1
        #print "-%s\n" % comment
        com_count = 0
        checkComments(comment,com_count)
    if (checkComments.counter - orig_comment) <= 10 and (orig_comment <= 10):
        scale = 1
    else:
        scale = 6.0
    print "%s" % submission
    print "ORIGINAL\t",
    print "="*int(round((orig_comment)/scale))
    print "\t",(orig_comment)
    print "REPLIES \t",
    print "="*int(round((checkComments.counter - orig_comment)/scale))
    print "\t",(checkComments.counter - orig_comment),"\n"
    checkComments.counter = 0

