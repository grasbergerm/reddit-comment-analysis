import praw
from operator import itemgetter

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
        comments.extend(str(comment).rstrip('\n').split(' '))
        checkComments(comment,com_count+1)

checkComments = Counter(checkComments)

user_agent = ("comment analysis by grasbergerm - https://github.com/grasbergerm/reddit-comment-analysis")
r = praw.Reddit(user_agent=user_agent)
# Get the subreddit choice
#subreddit = r.get_subreddit(raw_input("What subreddit? "))
# Used for a single submission
submission = r.get_submission(submission_id='2hssj4')
# For subreddit choice
#for submission in subreddit.get_top_from_week(limit=10):
# For single submission
comments = []
comment_dict = {}
for iteration_indent in range(1):
    submission.replace_more_comments(limit=None, threshold=0)
    #all_comments = submission.comments
    orig_comment = 0
    for comment in submission.comments:
        orig_comment += 1
        comments.extend(str(comment).rstrip('\n').split(' '))
        com_count = 0
        checkComments(comment,com_count)
    if (checkComments.counter - orig_comment) <= 10 and (orig_comment <= 10):
        scale = 1
    else:
        scale = 6.0
"""
    print "%s" % submission
    print "ORIGINAL\t",
    print "="*int(round((orig_comment)/scale))
    print "\t",(orig_comment)
    print "REPLIES \t",
    print "="*int(round((checkComments.counter - orig_comment)/scale))
    print "\t",(checkComments.counter - orig_comment),"\n"
    checkComments.counter = 0
"""
comments = [x for x in comments if x is not '']

for wordA in comments:
    occurrences = 0
    for wordB in comments:
        if wordA is wordB:
            occurrences += 1
    comment_dict[wordA] = occurrences
comments = sorted(comment_dict.items(), key=itemgetter(1))
# Top ten most used words
"""for index in range(-1, -11, -1):
    print comments[index][0],
    print "\t" + str(comments[index][1])"""
print comment_dict

