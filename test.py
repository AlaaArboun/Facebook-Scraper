import facebook
import requests
import pymongo

# Initialisation de l'API Facebook

token="access token"
graph = facebook.GraphAPI(token)

# Initialisation de la connexion à la base de données MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['my_database']
collection = db['my_collection']

# Paramètres de la recherche
search_query = 'Jacques Chirac'  # votre requête de recherche
search_limit = 100  # nombre de résultats à collecter

# Collecte des résultats de recherche depuis Facebook
search_results = graph.request('/search?q=' + search_query + '&type=post&limit=' + str(search_limit))

# Parcourir les résultats et collecter les détails
for post in search_results['data']:
    post_id = post['id']
    post_message = post['message'] if 'message' in post else ''
    post_image = ''
    post_comments = []
    
    # Collecter les images associées au post s'il y en a
    if 'attachments' in post:
        attachments = post['attachments']['data'][0]
        if 'media' in attachments:
            post_image = attachments['media']['image']['src']
    
    # Collecter les commentaires associés au post
    comment_count = post['comments']['summary']['total_count']
    if comment_count > 0:
        comments = graph.request('/' + post_id + '/comments?limit=' + str(comment_count))
        for comment in comments['data']:
            post_comments.append(comment['message'])
    
    # Enregistrer les détails du post dans la base de données MongoDB
    post_details = {
        'id': post_id,
        'message': post_message,
        'image': post_image,
        'comments': post_comments
    }
    collection.insert_one(post_details)
