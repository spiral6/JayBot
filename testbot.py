import discord
from discord.ext import tasks, commands
import praw
import tempfile
import yaml

class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        # self.checkAnimePosts.start()
        # self.checkStarCitizenPosts.start()

    async def on_message(self, message):
        # str(message.author) returns the author as String, not User.member
        if (str(message.author) == config['discord_admin_username'] and message.content == 'Hello JayBot'):
            await message.channel.send('sup cunt')
        elif (str(message.author) == config['discord_admin_username'] and message.content == '!testSC'):
            await self.testStarCitizenPosts()
        elif (message.content == 'Hello JayBot'):
            await message.channel.send('yeh')
        # print('Message from {0.author}: {0.content}'.format(message))

    @tasks.loop(seconds=10.0)
    async def checkAnimePosts(self): 
        try:
            #animu channel on Jay's server
            channel = self.get_channel(int(config['anime_channel_id']))
            # print(self.get_channel(int(config['anime_channel_id'])))
            
            previous_post_file = open('previous_anime_post.txt', 'a+')
            previous_post_file.seek(0)
            previous_post_id = previous_post_file.readline()
            print('')
            print('Previous post from /u/{0} has the id: '.format(config['anime_reddit_username']) + previous_post_id)

            for post in reddit.redditor(config['anime_reddit_username']).submissions.new(limit=1):
                current_post = post
                current_post_id = post.id
                print('Current post from /u/{0} has the id: '.format(config['anime_reddit_username']) + current_post_id)

            if str(current_post_id) != str(previous_post_id):
                print('Both posts do not match. Updating.')
                post_message = post.title + '\n' + post.url
                await channel.send(post_message)
                temppostfile = tempfile.NamedTemporaryFile(mode="r+")
                temppostfile.write(current_post_id)
                previous_post_file.close()
                previous_post_file = open('previous_anime_post.txt','w+')
                previous_post_file.write(current_post_id)
                temppostfile.close()
                previous_post_file.close()
            else:
                print('Both posts match. Ignoring.')
                previous_post_file.close()
            print('')
        except:
            # Damn I'm lazy. - Shamee
            print('Exception occurred. Unknown.')
            pass

    async def testStarCitizenPosts(self): 
        try:
            # channel = self.get_channel(int(config['star_citizen_channel_id']))
            channel = self.get_channel(int(config['debug_channel_id']))
            # print(self.get_channel(int(config['star_citizen_channel_id'])))
            
            previous_post_file = open('previous_star_citizen_post.txt', 'a+')
            previous_post_file.seek(0)
            # previous_post_id = previous_post_file.readline()
            print('')

            current_posts = []
            previous_post_ids = []
            post_message = None

            for post in reddit.redditor(config['star_citizen_reddit_username']).submissions.new(limit=2):
                current_posts.append(post)
                print('Current post from /u/{0} has the id: '.format(config['star_citizen_reddit_username']) + post.id)
            
            for old_post in previous_post_file:
                previous_post_ids.append(str(old_post.rstrip()))
                print('Previous post from /u/{0} has the id: '.format(config['star_citizen_reddit_username']) + str(old_post.rstrip()))

            
            previous_post_exists = [False] * len(previous_post_ids)

            for previous_post_id in previous_post_ids:
                for current_post in current_posts:
                    if(str(current_post.id) == str(previous_post_id)):
                        previous_post_exists[int(previous_post_ids.index(previous_post_id))] = True

            for previous_posts_check in range(0,len(previous_post_ids)):
                if not previous_post_exists[previous_posts_check]:
                    print('Posts do not match. Updating.')
                    new_post = current_posts[previous_posts_check]
                    post_message = new_post.title + '\n' + new_post.url
                    await channel.send(post_message)                
                else:
                    print('Both posts match. Ignoring.')
                
            if(post_message is not None):
                previous_post_file = open('previous_star_citizen_post.txt','w+')
                for current_post in current_posts:
                    previous_post_file.write(current_post.id + '\n')
                previous_post_file.close()

            print('')
        except:
            # Damn I'm lazy. - Shamee
            print('Exception occurred. Unknown.')
            pass

    @tasks.loop(seconds=10.0)
    async def checkStarCitizenPosts(self): 
        try:
            #animu channel on Jay's server
            channel = self.get_channel(int(config['star_citizen_channel_id']))
            # print(self.get_channel(int(config['star_citizen_channel_id'])))
            
            previous_post_file = open('previous_star_citizen_post.txt', 'a+')
            previous_post_file.seek(0)
            previous_post_id = previous_post_file.readline()
            print('')
            print('Previous post from /u/{0} has the id: '.format(config['star_citizen_reddit_username']) + previous_post_id)

            for post in reddit.redditor(config['star_citizen_reddit_username']).submissions.new(limit=1):
                current_post = post
                current_post_id = post.id
                print('Current post from /u/{0} has the id: '.format(config['star_citizen_reddit_username']) + current_post_id)

            if str(current_post_id) != str(previous_post_id):
                print('Both posts do not match. Updating.')
                post_message = post.title + '\n' + post.url
                await channel.send(post_message)
                temppostfile = tempfile.NamedTemporaryFile(mode="r+")
                temppostfile.write(current_post_id)
                previous_post_file.close()
                previous_post_file = open('previous_star_citizen_post.txt','w+')
                previous_post_file.write(current_post_id)
                temppostfile.close()
                previous_post_file.close()
            else:
                print('Both posts match. Ignoring.')
                previous_post_file.close()
            print('')
        except:
            # Damn I'm lazy. - Shamee
            print('Exception occurred. Unknown.')
            pass

with open('config.yaml') as c:
    config = yaml.load(c, Loader=yaml.FullLoader)
c.close()


reddit = praw.Reddit(user_agent=config['reddit_user_agent'],
                     client_id=config['reddit_id'], 
                     client_secret=config['reddit_secret'])
print(reddit.read_only)
print(reddit.auth.scopes())


client = MyClient()
client.run(config['discord_key'])


