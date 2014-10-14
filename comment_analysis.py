import praw
def checkComments(comment,com_count):
    for comment in comment.replies:
        com_count += 1
        print "\t"*com_count,
        print "%s" % comment
        checkComments(comment,com_count)

user_agent = ("comment analysis by grasbergerm")
r = praw.Reddit(user_agent=user_agent)
subreddit = r.get_subreddit('drunk')
post = r.get_submission(submission_id='2j72h3')
for comment in post.comments:
        print "-%s\n" % comment
        com_count = 0
        checkComments(comment,com_count)
