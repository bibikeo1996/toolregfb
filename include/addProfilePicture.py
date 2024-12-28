import requests
from PIL import Image
from io import BytesIO
import random
import string
import time
import os

# Function to generate a random string for filenames
def RandomTenAnh(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to upload and set profile picture
def ThemAnhVaoProfile(user_id, access_token, image_url, save_path, quality=20):
    # Step 1: Download and reduce the quality of the image
    TaiVaNenAnh(image_url, save_path, quality)
    
    # Step 2: Upload the photo to Facebook for the given user ID
    with open(save_path, 'rb') as image_file:
        url = f'https://graph.facebook.com/v21.0/{user_id}/photos'  # Include the user ID in the URL
        files = {'file': image_file}
        params = {'access_token': access_token}
        
        response = requests.post(url, files=files, params=params)
        photo_id = response.json().get('id')
    
    if photo_id:
        # Step 3: Set the uploaded photo as the profile picture for the user
        url = f'https://graph.facebook.com/v21.0/{user_id}/account'
        params = {
            'access_token': access_token,
            'photo': photo_id  # Using the uploaded photo's ID
        }
        response = requests.post(url, params=params)
        print('Profile picture updated:', response.json())
    else:
        print('Error uploading photo:', response.json())


def TaiVaNenAnh(url, save_path, target_size_kb=30, quality=20, resize_factor=0.5):
    # Download the image
    response = requests.get(url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        # Resize the image to reduce the size further
        width, height = image.size
        new_width = int(width * resize_factor)
        new_height = int(height * resize_factor)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        
        # Save the image with reduced quality
        temp_path = "temp_image.jpg"
        image.save(temp_path, "JPEG", quality=quality)

        # Check the size and adjust the quality if needed to reach the target size
        while os.path.getsize(temp_path) > target_size_kb * 1024:
            quality -= 5
            image.save(temp_path, "JPEG", quality=quality)
            if quality < 10:  # Prevent quality from dropping too low
                break

        # Final save to the desired path
        os.rename(temp_path, save_path)
        print(f"Image saved at {save_path} with reduced size.")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# Example usage:
# if __name__ == "__main__":
#     image_url = "https://thispersondoesnotexist.com/"
#     access_token = "EAAD6V7os0gcBO6Uj2InL5u8kvAkWvIzXmaMspGy7YiQVhV4LKrLNz2LcNYbH2UmfWqyXHHd5UrPB8AObj1EVGsDHkyiF5TrZCZCnGIRhK1taRUsCBD4XCi3i1JILYcvbbIBBGx8ienBQpTuSH8PZAQS9o5hBU723eqsoKVRJF2Dz9kCNxaEJ5HkaFtCxZCQ1bhtlyPX6yQZDZD"  # Replace with your access token
#     random_filename = RandomTenAnh() + ".jpg"
#     save_path = f"D:/Workspace/toolregFBWeb/imageDownloaded/{random_filename}"
#     user_id = '61571212798579'
    
#     ThemAnhVaoProfile(user_id, access_token, image_url, save_path)
