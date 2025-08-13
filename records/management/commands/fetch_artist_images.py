from django.core.management.base import BaseCommand
from records.models import Artist
import discogs_client
import cloudinary.uploader
import os

# Command requires an application to be created on https://www.discogs.com.
# Documentation for discogs can be found here - https://www.discogs.com/developers
if os.path.isfile('env.py'):
    DISCOGS_USER_TOKEN = os.environ.get('DISCOGS_USER_TOKEN')
    DEFAULT_ARTIST_IMAGE = os.environ.get('DEFAULT_ARTIST_IMAGE')


class Command(BaseCommand):
    help = 'Fetches artist images from Discogs and uploads them to Cloudinary.'

    def handle(self, *args, **kwargs):
        d = discogs_client.Client(
            'VinylOnline/1.0', user_token=DISCOGS_USER_TOKEN)

        for artist in Artist.objects.all():
            self.stdout.write(f'Search for artist: {artist.name}')

            # Checks if the artist has an image already set
            if artist.image and DEFAULT_ARTIST_IMAGE not in artist.image.url:
                self.stdout.write(
                    f'Skipping {artist.name}, custom image already set')
                continue

            # Search for the artist on Discogs
            results = d.search(artist.name, type='artist')
            if not results:
                self.stderr.write(f'No results found for {artist.name}')
                continue

            discogs_artist = results[0]

            # Check if the artist has images
            if not (hasattr(discogs_artist, 'images')
                    or not discogs_artist.images):
                self.stderr.write(f'No images found for {artist.name}')
                continue

            first_image_url = discogs_artist.images[0]['uri']

            self.stdout.write(
                f"Found image for {artist.name}: {first_image_url}")

            # Upload image to Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(first_image_url)
                artist.image = upload_result["secure_url"]
                artist.save()
                self.stdout.write(f'Saved image for {artist.name}')
            except Exception as e:
                self.stderr.write(
                    f'Failed to upload image for {artist.name}: {e}')
