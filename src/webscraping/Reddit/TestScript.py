from pmaw import PushshiftAPI

api = PushshiftAPI()
posts = api.search_submissions(subreddit="rust", limit=None)
print(f'{len(posts)} posts retrieved from Pushshift')
