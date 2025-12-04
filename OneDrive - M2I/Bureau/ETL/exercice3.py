import requests
import pandas as pd


BASE_URL = "https://jsonplaceholder.typicode.com"

#1

response_users = requests.get(f"{BASE_URL}/users")
response_users.raise_for_status()
users = response_users.json()
print(f"Nb total d'utilisateurs récupérés : {len(users)}")


#2

for user in users:
    print(f"Nom: {user['name']}, Email: {user['email']}")

#3

response_posts_user1 = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
response_posts_user1.raise_for_status()
posts_user1 = response_posts_user1.json()
print(f"Nb posts pour userId=1 : {len(posts_user1)}")

#4

nb_post = {}
try:
    
    response_all_posts = requests.get(f"{BASE_URL}/posts")
    response_all_posts.raise_for_status()
    all_posts = response_all_posts.json()

    
    for post in all_posts:
        user_id = post['userId']
        nb_post[user_id] = nb_post.get(user_id, 0) + 1

    for user in users:
        count = nb_post.get(user['id'], 0)
        print(f"Utilisateur {user['id']} ({user['name']}) a créé {count} posts.")

except requests.exceptions.RequestException as e:
    print(f"Erreur : {e}")
    all_posts = []

#5
try:
    response_comments_post1 = requests.get(f"{BASE_URL}/posts/1/comments")
    response_comments_post1.raise_for_status()
    comments_post1 = response_comments_post1.json()
    print(f"Le post id=1 a {len(comments_post1)} commentaires.")

except requests.exceptions.RequestException as e:
    print(f"Erreur : {e}")
    comments_post1 = []

#6

if not all_posts:
    try:
        response_all_posts = requests.get(f"{BASE_URL}/posts")
        response_all_posts.raise_for_status()
        all_posts = response_all_posts.json()
    except requests.exceptions.RequestException:
        all_posts = []

# Limiter aux 10 premiers posts
top_10_posts = all_posts[:10]
data_for_df = []

for post in top_10_posts:
    post_id = post['id']
    post_title = post['title']
    
    # Récupérer les commentaires pour le post actuel
    try:
        response_comments = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
        response_comments.raise_for_status()
        comments = response_comments.json()
        nombre_commentaires = len(comments)
    except requests.exceptions.RequestException:
        nombre_commentaires = 0 # En cas d'erreur d'API pour un post

    # Ajouter les données à la liste
    data_for_df.append({
        "post_id": post_id,
        "post_title": post_title,
        "nombre_commentaires": nombre_commentaires
    })

# Créer le DataFrame
df_posts_summary = pd.DataFrame(data_for_df)

# Afficher le DataFrame
print("\nDataFrame récapitulatif des 10 premiers posts :")
print(df_posts_summary)
