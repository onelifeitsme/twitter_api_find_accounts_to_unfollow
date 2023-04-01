import requests
import tweepy
import time

client = tweepy.Client('AAAAAAAAAAAAAAAAAAAAAAkebQEAAAAAmpzxzNABmgMUqsFytnKci%2BtI7jQ%3DEuphW1Hg5YtlCJS26xi8LjZDbuAGBT1RaeiFvPFgAbmUkACmll', wait_on_rate_limit=True)



me = client.get_user(id=1157422413073854464).data


def get_my_followings(me):
    """Список моих подписок"""
    paginator = tweepy.Paginator(
        client.get_users_following,  # The method you want to use
        me.id,  # Some argument for this method
        max_results=100,  # How many tweets asked per request
    )
    return [user for user in paginator.flatten(limit=500)]


def get_users_tweets(user) -> list:
    """Список твитов юзера (300 последних)"""
    paginator = tweepy.Paginator(
        client.get_users_tweets,  # The method you want to use
        user.id,  # Some argument for this method
        max_results=100,  # How many tweets asked per request
        exclude='replies',
    )
    return [tweet for tweet in paginator.flatten(limit=300)]



def check_if_i_liked_tweet(tweet) -> bool:
    """лайкал ли я твит"""
    users_who_liked = client.get_liking_users(id=tweet.id).data
    if users_who_liked:
        return me in users_who_liked
    return False


my_following_list = get_my_followings(me)
users_to_unfollow = []


for user in my_following_list:
    try:
        print(f'Провермяем юзера {user.username}')
        users_tweets = get_users_tweets(user)
        for tweet in users_tweets:
            if check_if_i_liked_tweet(tweet):
                print(f'https://twitter.com/{user.username} проверку прошёл')
                break
            if tweet == users_tweets[-1] and not check_if_i_liked_tweet(tweet):
                users_to_unfollow.append(f'https://twitter.com/{user.username}')
                print(f'https://twitter.com/{user.username} проверку не прошёл')
    except requests.exceptions.ReadTimeout:
        time.sleep(300)
        print(f'Провермяем юзера {user.username}')
        users_tweets = get_users_tweets(user)
        for tweet in users_tweets:
            if check_if_i_liked_tweet(tweet):
                print(f'https://twitter.com/{user.username} проверку прошёл')
                break
            if tweet == users_tweets[-1] and not check_if_i_liked_tweet(tweet):
                users_to_unfollow.append(f'https://twitter.com/{user.username}')
                print(f'https://twitter.com/{user.username} проверку не прошёл')





with open('to_unfollow.txt', mode='w') as f:
    for u in users_to_unfollow:
        f.write(u)
        f.write('\n')





