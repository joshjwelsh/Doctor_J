import sys
import spotipy
import spotipy.util as util
import cred
import pandas as pd


scope = 'playlist-modify-public'
liked_songs = []
ids = []
rows = []
fields = []
names = []
filename = "song_analysis-2.csv"

def beating_limit(sp, liked_playlist):
	liked_songs_id = []
	for i in range(0,50):
		print("beatin limit " + str(i))
		results = sp.current_user_saved_tracks(limit=20, offset=i*20)
		for item in results['items']:
			track = item['track']
			liked_playlist.append(track['name'])
			liked_songs_id.append(track['id'])

	return liked_songs_id

def rowifier(feature_arg, rows):
	for f in feature_arg:
		rows.append(f.values())
	return rows

def fieldCreator(sp, fields, ids):
	f1 = sp.audio_features(ids[0])
	fields = f1[0].keys()
	return fields


def featuresCreator(sp, ids, rows):
	count = 0
	for id in ids:
		if count == 500: print('loading table:',count)
		feature = sp.audio_features(id)
		rows = rowifier(feature, rows)
		count += 1
	return rows

def createCSV(fields, rows):
    frame = dict()
    count = 0
    for f in fields:
        frame[f] = rows[count]
        count+=1

    df = pd.DataFrame(data=rows, columns=fields)
    df.to_csv(filename)

def names(liked_songs):
	df = pd.DataFrame(data=[liked_songs,ids])
	df.to_csv('id_names.csv')

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

token = util.prompt_for_user_token(username, scope, cred.ID, cred.ID_SECRET,
                                cred.REDIRECT)


if token:
    sp = spotipy.Spotify(auth=token)
    ids = beating_limit(sp, liked_songs)
    fields = fieldCreator(sp, fields, ids)
    # rows = featuresCreator(sp, ids, rows)
    names(liked_songs)
    # createCSV(fields, rows)

else:
    print("Can't get token for", username)
