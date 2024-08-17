# padlet py
 A Padlet API wrapper written in python using async/await syntax

 ## Usage

### Get started
 ``` 
 pip install padlet-py 
 ```
In your file:
 ```py
import padlet

api_key = "pdlt_0000"  # your padlet api key.
board_id = "mwrsf0033"  # The board id you are interested in.

# Create an user object.
user = padlet.user(api_key)

# This will create a board object, but it won't have any data yet.
board = user.board(board_id)
```
```py
# You must fetch the data from the api using:
await board.fetch()
# The board attributes, sections, and posts (including attachments) are 
# now loaded into the object.
 ```

 ### How to use
 ```py
# The boards posts are stored in a dictionary by their ID.
a_post_that_i_need = board.posts['post_id']
a_section_that_i_need = board.sections['section_id']
 ```
 At the moment, this dictionary is editable, so take care to not overwrite any values in it. \
 You can .fetch() the board again to load the posts and sections again from scratch.
 

 Heres you can create a post to the padlet board:
 ```py
async def create_post():
    # I'm going to grab the first section of my board
    section = board.sections.values()[0] 
    await board.create('args go here')
 ```
 Here are the args that you can pass to the .create() function:

 |Arg|Type|Optional?|
 |---|---|---|
 | subject | str | No |
 | body | str | No |
 | color | Literal['red', 'orange', 'green', 'blue', 'purple'] | Yes |
 | attachment_url | str | Yes |
 | attachment_caption | str | Yes |
 | status | Literal['approved', 'pending_moderation', 'scheduled'] | Yes |
 | map | map_object | Yes |
 | canvas | canvas_object | Yes |
 | previous_post | post_object | Yes |

Notice that some of the args are `objects`. You can deal with those like this:
```py
# Import all the objects you need
from padlet import user, map_object, canvas_object, post_object, section_object

async def create(section: section_object):
    # You can create your own map object by the method below
    # or depending on your needs, reference one from another post
    map = map_object()
    map.latitude = 321
    map.longitude = 321
    map.location_name = 'Python HQ'

    # You can also construct your own post object, using just the id.
    post = post_object()
    post.id = 'post_id'
    # Again, you its recommended that you reference another post from the board:
    post = section.board.posts['post_id'] 

    await section.create(subject='Python',
                         body='Just testing',
                         status='approved',
                         map=map,
                         previous_post=post)
```


## Caveats?
At the moment this wrapper does not deal with ratelimits or error codes. That is already planned.

I also hope to make this wrapper more forwards compatible, so that it doesn't break due to any sudden changes in the padlet API.

