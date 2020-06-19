import spotipy
import sys
import spotipy.util as util


def auth():
    if len(sys.argv) > 1:
        username = sys.argv[1]


    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
	    sp = spotipy.Spotify(auth=token)
        print('Hello')
    
    else:
    print("Can't get token for", username)



if __name__=='__main__':
    auth()
