
import requests

BASE_URL = "https://musicbrainz.org/ws/2"

HEADERS = {
    "User-Agent": "MusicBrainzExplorer/1.0 (student project)"
}


def search_artist(artist_name):
    url = f"{BASE_URL}/artist/"

    params = {
        "query": f'artist:"{artist_name}"',
        "fmt": "json",
        "limit": 5
    }

    response = requests.get(
        url, params=params, headers=HEADERS, timeout=15
    )
    response.raise_for_status()

    data = response.json()
    return data.get("artists", [])


def get_artist_releases(artist_id):
    url = f"{BASE_URL}/release/"

    params = {
        "artist": artist_id,
        "fmt": "json",
        "limit": 10
    }

    response = requests.get(
        url, params=params, headers=HEADERS, timeout=15
    )
    response.raise_for_status()

    data = response.json()
    return data.get("releases", [])


def get_release_tracks(release_id):
    url = f"{BASE_URL}/release/{release_id}"

    params = {
        "inc": "recordings",
        "fmt": "json"
    }

    response = requests.get(
        url, params=params, headers=HEADERS, timeout=15
    )
    response.raise_for_status()

    data = response.json()

    tracks = []

    for medium in data.get("media", []):
        for track in medium.get("tracks", []):
            tracks.append(track)

    return data, tracks


def main():
    artist_name = input("Enter an artist name: ").strip()

    if not artist_name:
        print("Please enter an artist name.")
        return

    try:
        artists = search_artist(artist_name)

        if not artists:
            print("No artists found.")
            return

        print("\nMatching artists:")

        for index, artist in enumerate(artists, start=1):
            artist_type = artist.get("type", "Unknown Type")
            country = artist.get("country", "Unknown Country")

            print(
                f"{index}. {artist['name']} - "
                f"{artist_type}, {country}"
            )

        choice = input(
            "\nEnter the number of the artist to view releases: "
        ).strip()

        if not choice.isdigit():
            print("Invalid selection.")
            return

        artist_index = int(choice)

        if not 1 <= artist_index <= len(artists):
            print("Invalid selection.")
            return

        selected_artist = artists[artist_index - 1]

        releases = get_artist_releases(selected_artist["id"])

        if not releases:
            print("No releases found.")
            return

        print(f"\nReleases by {selected_artist['name']}:")

        for index, release in enumerate(releases, start=1):
            title = release.get("title", "Unknown Title")
            date = release.get("date", "Unknown Date")
            print(f"{index}. {title} ({date})")

        release_choice = input(
            "\nEnter the number of a release to view its tracks: "
        ).strip()

        if not release_choice.isdigit():
            print("Invalid selection.")
            return

        release_index = int(release_choice)

        if not 1 <= release_index <= len(releases):
            print("Invalid selection.")
            return

        selected_release = releases[release_index - 1]

        release_details, tracks = get_release_tracks(
            selected_release["id"]
        )

        print(f"\nRelease: {release_details.get('title', 'Unknown Title')}")
        print(f"Date: {release_details.get('date', 'Unknown Date')}")
        print(f"Country: {release_details.get('country', 'Unknown Country')}")

        if not tracks:
            print("No track listing found.")
            return

        print("\nTrack Listing:")

        for track in tracks:
            number = track.get("number", "?")
            title = track.get("title", "Unknown Track")
            length = track.get("length")

            if length is not None:
                seconds = length // 1000
                minutes = seconds // 60
                seconds = seconds % 60
                duration = f"{minutes}:{seconds:02d}"
            else:
                duration = "Unknown duration"

            print(f"{number}. {title} ({duration})")

    except requests.RequestException as error:
        print(f"An API request error occurred: {error}")

    except (ValueError, KeyError) as error:
        print(f"An unexpected data error occurred: {error}")


if __name__ == "__main__":
    main()
