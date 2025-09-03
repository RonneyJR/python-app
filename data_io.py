import json
import os
from datetime import datetime


def remove_vietnamese_signs(text: str) -> str:
    # Replace Vietnamese characters with their non-accented equivalents
    replacements = {
        'àáạảãâầấậẩẫăằắặẳẵ': 'a',
        'ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ': 'A', 
        'èéẹẻẽêềếệểễ': 'e',
        'ÈÉẸẺẼÊỀẾỆỂỄ': 'E',
        'òóọỏõôồốộổỗơờớợởỡ': 'o', 
        'ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ': 'O',
        'ìíịỉĩ': 'i',
        'ÌÍỊỈĨ': 'I',
        'ùúụủũưừứựửữ': 'u',
        'ƯỪỨỰỬỮÙÚỤỦŨ': 'U',
        'ỳýỵỷỹ': 'y',
        'ỲÝỴỶỸ': 'Y',
        'đ': 'd',
        'Đ': 'D'
    }
    
    for vietnamese, latin in replacements.items():
        for char in vietnamese:
            text = text.replace(char, latin)
    return text

def build_alias(name: str) -> str:
    # Remove Vietnamese characters
    name = remove_vietnamese_signs(name)
    # Replace hyphens with spaces
    name = name.replace('-', ' ')
    # Convert to lowercase
    name = name.lower()
    # Trim spaces
    name = name.strip()
    # Replace spaces with hyphens
    name = name.replace(' ', '-')
    # Remove any characters that aren't a-z, 0-9, or hyphen
    name = ''.join(c for c in name if c.isalnum() or c == '-')
    # Replace multiple hyphens with single hyphen
    while '--' in name:
        name = name.replace('--', '-')
    return name


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent = 4)

def create_user(email, password, name, birthday = "", gender = ""):
    users = load_json("data/users.json")
    users.append({
        "id": len(users) + 1,
        "email": email,
        "password": password,
        "name": name,
        "birthday": birthday,
        "gender": gender,
        "avatar": ""
    })
    write_json("data/users.json", users)

def get_user_by_id(id):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            return user
    return None

def get_user_by_email(email):
    users = load_json("data/users.json")
    for user in users:
        if user["email"] == email:
            return user
    return None

def get_user_by_email_and_password(email, password):
    users = load_json("data/users.json")
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
    return None

def update_user(id, name, birthday = "", gender = ""):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            user["id"] = id
            user["name"] = name
            user["birthday"] = birthday
            user["gender"] = gender
            break
    write_json("data/users.json", users)

def update_user_avatar(id, avatar):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            user["avatar"] = avatar
            break
    write_json("data/users.json", users)

def get_songs_by_name_json(name):
    """Get songs by name using JSON file"""
    try:
        songs = load_json("data/songs.json")
        if not name:
            return songs[:50]
        
        name_lower = name.lower()
        filtered_songs = []
        for song in songs:
            if (name_lower in song.get('name', '').lower() or 
                name_lower in song.get('alias', '').lower() or
                name_lower in song.get('artist_names', '').lower()):
                filtered_songs.append(song)
                if len(filtered_songs) >= 50:
                    break
        return filtered_songs
    except Exception as e:
        print(f"Error loading songs from JSON: {e}")
        return []

def get_first_15_songs_json():
    """Get first 15 songs using JSON file"""
    try:
        songs = load_json("data/songs.json")
        return songs[:15]
    except Exception as e:
        print(f"Error loading songs from JSON: {e}")
        return []

def get_song_by_id_json(song_id):
    """Get song by ID using JSON file"""
    try:
        songs = load_json("data/songs.json")
        # Compare IDs as strings to be robust to int/str mismatches
        target_id = str(song_id)
        for song in songs:
            if str(song.get('id')) == target_id:
                return song
        return None
    except Exception as e:
        print(f"Error loading song from JSON: {e}")
        return None

# New playlist functions using JSON
def is_song_in_user_playlist_json(user_id, song_id):
    """Check if song is in user's playlist using JSON"""
    try:
        playlists = load_json("data/playlists.json")
        song_id_str = str(song_id)
        user_id_str = str(user_id)
        for playlist in playlists:
            if (str(playlist.get('user_id')) == user_id_str and 
                str(playlist.get('song_id')) == song_id_str):
                return True
        return False
    except Exception as e:
        print(f"Error checking playlist: {e}")
        return False

def get_user_playlist_songs_json(user_id):
    """Get all songs in user's playlist using JSON"""
    try:
        playlists = load_json("data/playlists.json")
        songs = load_json("data/songs.json")
        
        user_songs = []
        user_id_str = str(user_id)
        for playlist in playlists:
            if str(playlist.get('user_id')) == user_id_str:
                song_id = str(playlist.get('song_id'))
                for song in songs:
                    if str(song.get('id')) == song_id:
                        user_songs.append(song)
                        break
        return user_songs
    except Exception as e:
        print(f"Error loading playlist songs: {e}")
        return []

def add_song_to_user_playlist_json(user_id, song_id):
    """Add song to user's playlist using JSON"""
    try:
        playlists = load_json("data/playlists.json")
        
        # Check if song already exists
        if is_song_in_user_playlist_json(user_id, song_id):
            return False
        
        # Get song details
        song = get_song_by_id_json(song_id)
        if not song:
            return False
        
        # Generate next ID
        next_id = 1
        if playlists:
            next_id = max(p.get('id', 0) for p in playlists) + 1
        
        new_playlist_item = {
            'id': next_id,
            'user_id': user_id,
            'song_id': song_id,
            'name': 'My Playlist',
            'song_name': song.get('name', ''),
            'image_path': song.get('image_path', ''),
            'file_path': song.get('file_path', '')
        }
        
        playlists.append(new_playlist_item)
        write_json("data/playlists.json", playlists)
        return True
    except Exception as e:
        print(f"Error adding song to playlist: {e}")
        return False

def remove_song_from_user_playlist_json(user_id, song_id):
    """Remove song from user's playlist using JSON"""
    try:
        playlists = load_json("data/playlists.json")
        
        # Remove all matching playlist items
        playlists = [p for p in playlists 
                     if not (p.get('user_id') == user_id and p.get('song_id') == song_id)]
        
        write_json("data/playlists.json", playlists)
        return True
    except Exception as e:
        print(f"Error removing song from playlist: {e}")
        return False

def add_song_to_history_json(user_id, song_id):
    """Append a play event to history with timestamp."""
    history = load_json("data/history.json")
    # Don't duplicate consecutive same song for the same user
    if history and str(history[-1].get('user_id')) == str(user_id) and str(history[-1].get('song_id')) == str(song_id):
        return False
    history.append({
        'user_id': user_id,
        'song_id': song_id,
        'played_at': datetime.now().isoformat(timespec='seconds')
    })
    write_json("data/history.json", history)
    return True

def get_user_history_songs_json(user_id, limit=50):
    """Get recent songs a user played, newest first."""
    history = load_json("data/history.json")
    songs = load_json("data/songs.json")
    user_items = [h for h in history if str(h.get('user_id')) == str(user_id)]
    # Sort by played_at descending
    user_items.sort(key=lambda x: x.get('played_at', ''), reverse=True)
    result = []
    seen = set()
    for item in user_items:
        sid = str(item.get('song_id'))
        if sid in seen:
            continue
        for song in songs:
            if str(song.get('id')) == sid:
                result.append(song)
                seen.add(sid)
                break
        if len(result) >= limit:
            break
    return result