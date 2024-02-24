import re


def initialize_playlist(target_duration):
    file = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-TARGETDURATION:{target_duration}
#EXT-X-DISCONTINUITY
    """

    with open('../outputs/playlist.m3u8', 'w') as f:
        f.write(file)


def get_target_duration(segment_file):
    with open(segment_file, 'r') as f:
        segment = f.read()

        pattern = r'#EXT-X-TARGETDURATION:(\d+)'
        match = re.search(pattern, segment)
        if match:
            # Récupération de la valeur capturée
            target_duration = match.group(1)
            return target_duration


def add_segment_to_playlist(segment_file):
    with open(segment_file, 'r') as f:
        segment = f.read()

    # parse the playlist and get #EXTINF: and segment URI
    pattern_extinf = r'#EXTINF:(\d+\.\d+),'
    pattern_url = r'http\S+'

    match_extinf = re.search(pattern_extinf, segment)
    match_url = re.search(pattern_url, segment)

    if match_extinf and match_url:
        with open('../outputs/playlist.m3u8', 'a') as f:
            f.write(f"#EXTINF:{match_extinf.group(1)},\n")
            f.write(f"{match_url.group()}\n")
