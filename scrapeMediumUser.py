# Import libraries
import os
import argparse
import requests
from py2neo import Graph, Node, Relationship
from datetime import datetime

#TODO logging to S3

def get_or_create_user_from_user_id(user_id, api_key):
    # API setup
    base_url = "https://medium2.p.rapidapi.com/user"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "medium2.p.rapidapi.com"
    }

    # Neo4j connection (update URI, user, and password as needed)
    graph = Graph("bolt://IP:port", auth=("username", "password"))

    # Check if user already exists in Neo4j
    user = graph.evaluate("MATCH (u:User {id: $id}) RETURN u", id=user_id)
    if user is not None:
        print("User already exists in the database.")
        return user

    # Second API call to get user details
    details_url = f"{base_url}/{user_id}"
    response_details = requests.get(details_url, headers=headers)
    user_details = response_details.json()

    if 'error' in user_details:
        print("Error retrieving user details:", user_details['error'])
        return

    # Create a new user node in Neo4j
    user_node = Node("User",
                     id=user_id,
                     username=user_details['username'],
                     fullname=user_details['fullname'],
                     bio=user_details['bio'],
                     #followers_count=user_details['followers_count'],
                     #following_count=user_details['following_count'],
                     publication_following_count=user_details['publication_following_count'],
                     image_url=user_details['image_url'],
                     twitter_username=user_details['twitter_username'],
                     is_writer_program_enrolled=user_details['is_writer_program_enrolled'],
                     allow_notes=user_details['allow_notes'],
                     medium_member_at=user_details['medium_member_at'],
                     is_suspended=user_details['is_suspended'],
                     top_writer_in=user_details['top_writer_in'],
                     has_list=user_details['has_list'],
                     is_book_author=user_details['is_book_author'],
                     tipping_link=user_details['tipping_link'],
                     bg_image_url=user_details['bg_image_url'],
                     logo_image_url=user_details['logo_image_url'])

    graph.create(user_node)
    print("New user created from user_id:", user_node)
    return user_node

def get_or_create_user(username, api_key):
    # API setup
    base_url = "https://medium2.p.rapidapi.com/user"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "medium2.p.rapidapi.com"
    }

    # Neo4j connection (update URI, user, and password as needed)
    graph = Graph("bolt://IP:port", auth=("username", "password"))

    # First API call to get user_id
    id_url = f"{base_url}/id_for/{username}"
    response_id = requests.get(id_url, headers=headers)
    user_data = response_id.json()
    print(user_data)

    if 'error' in user_data:
        print("Error retrieving user ID:", user_data['error'])
        return

    user_id = user_data['id']

    # Check if user already exists in Neo4j
    user = graph.evaluate("MATCH (u:User {id: $id}) RETURN u", id=user_id)
    if user is not None:
        print("User already exists in the database.")
        return user_id

    # Second API call to get user details
    details_url = f"{base_url}/{user_id}"
    response_details = requests.get(details_url, headers=headers)
    user_details = response_details.json()

    if 'error' in user_details:
        print("Error retrieving user details:", user_details['error'])
        return

    # Create a new user node in Neo4j
    user_node = Node("User",
                     id=user_id,
                     username=user_details['username'],
                     fullname=user_details['fullname'],
                     bio=user_details['bio'],
                     #followers_count=user_details['followers_count'],
                     #following_count=user_details['following_count'],
                     publication_following_count=user_details['publication_following_count'],
                     image_url=user_details['image_url'],
                     twitter_username=user_details['twitter_username'],
                     is_writer_program_enrolled=user_details['is_writer_program_enrolled'],
                     allow_notes=user_details['allow_notes'],
                     medium_member_at=user_details['medium_member_at'],
                     is_suspended=user_details['is_suspended'],
                     top_writer_in=user_details['top_writer_in'],
                     has_list=user_details['has_list'],
                     is_book_author=user_details['is_book_author'],
                     tipping_link=user_details['tipping_link'],
                     bg_image_url=user_details['bg_image_url'],
                     logo_image_url=user_details['logo_image_url'])

    graph.create(user_node)
    print("New user created:", user_node)
    return user_id


def retrieve_and_link_articles(user_id, api_key):
    print("Retrieving articles for user:", user_id)
    base_url = "https://medium2.p.rapidapi.com"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "medium2.p.rapidapi.com"
    }

    # Neo4j connection (update with your credentials)
    graph = Graph("bolt://IP:port", auth=("username", "password"))

    # Retrieve articles associated with the user
    articles_url = f"{base_url}/user/{user_id}/articles"
    response = requests.get(articles_url, headers=headers)
    articles_data = response.json()
    print("Extracted articles data")
    print(articles_data)

    if 'associated_articles' not in articles_data:
        print("No articles found or error in fetching articles.")
        return

    article_ids = articles_data['associated_articles']

    for article_id in article_ids:
        # Fetch detailed information for each article
        article_url = f"{base_url}/article/{article_id}"
        article_response = requests.get(article_url, headers=headers)
        article_info = article_response.json()

        # Create or update an Article node
        article_node = graph.nodes.match("Article", id=article_id).first()
        if not article_node:
            article_node = Node("Article", id=article_id)
            graph.create(article_node)
            print(f"Created new Article node: {article_id}")

        # Update Article properties
        article_node.update({
            "title": article_info.get('title'),
            "subtitle": article_info.get('subtitle'),
            "published_at": article_info.get('published_at'),
            "last_modified_at": article_info.get('last_modified_at'),
            "word_count": article_info.get('word_count'),
            "reading_time": article_info.get('reading_time'),
            "url": article_info.get('url'),
            "unique_slug": article_info.get('unique_slug'),
            "image_url": article_info.get('image_url'),
            "lang": article_info.get('lang'),
            "is_series": article_info.get('is_series'),
            "is_locked": article_info.get('is_locked'),
            "is_shortform": article_info.get('is_shortform'),
            "top_highlight": article_info.get('top_highlight')
        })
        graph.push(article_node)

        # Manage relationships for tags and topics
        for tag in article_info.get('tags', []):
            tag_node = graph.nodes.match("Tag", name=tag).first()
            if not tag_node:
                tag_node = Node("Tag", name=tag)
                graph.create(tag_node)
            graph.merge(Relationship(article_node, "HAS_TAG", tag_node))

        for topic in article_info.get('topics', []):
            topic_node = graph.nodes.match("Topic", name=topic).first()
            if not topic_node:
                topic_node = Node("Topic", name=topic)
                graph.create(topic_node)
            graph.merge(Relationship(article_node, "COVERS_TOPIC", topic_node))

        # Handle publication if exists
        if article_info.get('publication_id'):
            publication_node = graph.nodes.match("Publication", id=article_info.get('publication_id')).first()
            if not publication_node:
                publication_node = Node("Publication", id=article_info.get('publication_id'))
                graph.create(publication_node)
            graph.merge(Relationship(article_node, "PUBLISHED_IN", publication_node))

        # Manage the authored relationship
        user_node = graph.nodes.match("User", id=user_id).first()
        if user_node:
            authored = Relationship(user_node, "AUTHORED", article_node)
            graph.merge(authored, "User", "id")
            print(f"Linked {user_id} to {article_id}")

        # Handle fans and claps
        fans_url = f"{base_url}/article/{article_id}/fans"
        fans_response = requests.get(fans_url, headers=headers)
        fans_data = fans_response.json()

        for fan_id in fans_data.get('fans', []):
            fan_node = graph.nodes.match("User", id=fan_id).first()
            if not fan_node:
                fan_node = Node("User", id=fan_id)
                graph.create(fan_node)

            # Check if the clap event already exists to prevent duplication
            event_exists = graph.evaluate(
                "MATCH (u:User)-[r:CLAPPED_ON]->(a:Article {id: $article_id}) WHERE u.id = $fan_id RETURN r",
                article_id=article_id, fan_id=fan_id)
            if not event_exists:
                # Create a new clapping event
                clapped_on = Relationship(fan_node, "CLAPPED_ON", article_node, timestamp=str(datetime.now()))
                graph.create(clapped_on)
                print(f"New clapping event added for fan {fan_id} on article {article_id}")

def create_follower_nodes_and_relationships(user_id, api_key):
    base_url = "https://medium2.p.rapidapi.com/user"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "medium2.p.rapidapi.com"
    }

    # Neo4j connection (update with your credentials)
    graph = Graph("bolt://IP:port", auth=("username", "password"))

    # Function to handle the pagination of followers
    def fetch_and_create_followers(user_id, after=None):
        params = {'count': 25}
        if after:
            params['after'] = after

        # Fetch followers
        url = f"{base_url}/{user_id}/followers"
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Create nodes and relationships in Neo4j
        for follower_id in data.get('followers', []):
            #follower_node = Node("User", id=follower_id)
            follower_node = get_or_create_user_from_user_id(follower_id, api_key)
            graph.merge(follower_node, "User", "id")

            # Establish relationship with the main author
            main_author = graph.nodes.match("User", id=user_id).first()
            if main_author:
                relationship = Relationship(follower_node, "IS_FOLLOWED_BY", main_author)
                graph.create(relationship)

        # Recursively fetch next page of followers if available
        next_follower_id = data.get('next')
        if next_follower_id:
            fetch_and_create_followers(user_id, after=next_follower_id)

    # Start the process
    fetch_and_create_followers(user_id)

def create_following_nodes_and_relationships(user_id, api_key):
    base_url = "https://medium2.p.rapidapi.com/user"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "medium2.p.rapidapi.com"
    }

    # Neo4j connection (update with your credentials)
    graph = Graph("bolt://IP:port", auth=("username", "password"))

    # Function to handle the pagination of following
    def fetch_and_create_following(user_id, after=None):
        #params = {'count': 25}
        params = {}
        #if after:
        #    params['after'] = after

        # Fetch following
        url = f"{base_url}/{user_id}/following"
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Create nodes and relationships in Neo4j
        for following_id in data.get('following', []):  # Assuming JSON response structure is similar to followers
            # Get or create user node for the following_id
            following_node = get_or_create_user_from_user_id(following_id, api_key)
            graph.merge(following_node, "User", "id")

            # Establish relationship with the main author
            main_author = graph.nodes.match("User", id=user_id).first()
            if main_author:
                relationship = Relationship(main_author, "FOLLOWS", following_node)
                graph.create(relationship)

        # Recursively fetch next page of following if available
        #next_following_id = data.get('next')
        #if next_following_id:
        #    fetch_and_create_following(user_id, after=next_following_id)

    # Start the process
    fetch_and_create_following(user_id)

def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Get user ID from Medium')
    parser.add_argument('username', type=str, help='Username to get ID for')

    # Parse the command line arguments
    args = parser.parse_args()

    # Get RAPIDAPI_KEY from the environment
    api_key = "YOUR_RAPID_API_KEY"
    user_id = get_or_create_user(args.username, api_key)
    retrieve_and_link_articles(user_id, api_key)
    create_follower_nodes_and_relationships(user_id, api_key)
    create_following_nodes_and_relationships(user_id, api_key)

if __name__ == "__main__":
    main()