from django.core.management.base import BaseCommand
from records.models import Artist, Record, Genre, RecordImage
import discogs_client
import cloudinary.uploader
import random
import os

# Command requires an application to be created on https://www.discogs.com.
# Documentation for the python3 discogs client can be found here - https://python3-discogs-client.readthedocs.io/en/latest/authentication.html
if os.path.isfile('env.py'):
    DISCOGS_USER_TOKEN = os.environ.get('DISCOGS_USER_TOKEN')
    DEFAULT_ARTIST_IMAGE = os.environ.get('DEFAULT_ARTIST_IMAGE')


class Command(BaseCommand):
    help = ('Fetches record details from discogs and creates an instance '
            'of that record. User must provide release id which can be found '
            'in the discogs.com/release/{release-id}-{release-name}')

    def handle(self, *args, **kwargs):
        d = discogs_client.Client(
            'VinylOnline/1.0', user_token=DISCOGS_USER_TOKEN)

        release_id = input("Please enter release ID:")

        release = d.release(release_id)

        # Checks if the artist is in the database
        artist = release.artists[0].name
        database_artist = Artist.objects.filter(name=artist).first()

        if not database_artist:
            self.stderr.write('No database artist found. Please ensure artist '
                              'exists within database first.')
            return

        # Creates the tracklist with appropriate positions
        release_notes = release.notes
        tracklist_items = ''.join(
            [f'<li>{track.position} | {track.title}</li>'
             for track in release.tracklist])

        # Description includes notes from Discogs about the record
        # In a production environment these could be pulled from own info about releases.
        description = f"""
                <p>{release_notes}</p>
                <br>
                <strong>Tracklist:</strong>
                <ul>
                {tracklist_items}
                </ul>
                """
        # Prices are random for the sake of mass-record creation. These could be
        # set with an input() when obtaining record data.
        prices = [25.00, 45.99, 30.99, 37.99]
        quantity = random.randint(15, 400)
        price = prices[random.randint(0, 3)]
        database_genres = Genre.objects.filter(name__in=release.genres)
        if not database_genres:
            self.stderr.write('No appropriate genres detected in database. '
                              'Please ensure appropriate genres for record '
                              'have been added.')
            return

        # Creates the record instance
        record = Record.objects.create(
            title=release.title,
            artist=database_artist,
            release_year=release.year,
            size='12"',
            rpm='33',
            description=description,
            price=price,
            quantity=quantity
        )

        record.genre.set(database_genres)
        record.save()

        self.stdout.write(f"Record {record.title} has now been created.")
        self.stdout.write(f"Fetching RecordImages for {record.title}...")

        for image in release.images[:5]:
            if image['type'] == 'primary':
                try:
                    upload_result = cloudinary.uploader.upload(image['uri'])
                    record_image = RecordImage.objects.create(
                        record=record,
                        image=upload_result['secure_url'],
                        image_type='Front Cover'
                    )
                    record_image.save()
                    self.stdout.write(
                        f'Record Image for {record.title} uploaded successfully.'
                    )
                except Exception as e:
                    self.stderr.write(
                        f'Failed to upload image for {record.title}: {e}'
                    )
                    continue
            else:
                try:
                    upload_result = cloudinary.uploader.upload(image['uri'])
                    record_image = RecordImage.objects.create(
                        record=record,
                        image=upload_result['secure_url'],
                        image_type='Other'
                    )
                    record_image.save()
                    self.stdout.write(
                        f'Record Image for {record.title} uploaded successfully.'
                    )
                except Exception as e:
                    self.stderr.write(
                        f'Failed to upload image for {record.title}: {e}'
                    )
                    continue
        
        self.stdout.write(f'All images for {record.title} uploaded.')
