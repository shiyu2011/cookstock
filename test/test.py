import tickertick as tt
import tickertick.query as query
from datetime import datetime, timezone

def get_feed(ticker):
    feed = tt.get_feed(
        query = query.And(
            query.BroadTicker(ticker),
            query.StoryType(query.StoryTypes.CURATED)
        )
    ) # SEC filings from Apple Inc.
    return feed

def get_time_difference(story):
    event_time = story.time
    current_time = datetime.now(timezone.utc)
    time_difference = current_time - event_time
    td_seconds = time_difference.total_seconds()
    if td_seconds < 60:
        result = f"{int(td_seconds)} seconds ago"
    elif td_seconds < 3600:
        minutes = td_seconds // 60
        result = f"{int(minutes)} minutes ago"
    elif td_seconds < 86400:
        hours = td_seconds // 3600
        result = f"{int(hours)} hours ago"
    else:
        days = td_seconds // 86400
        result = f"{int(days)} days ago"
    return result, td_seconds

def return_story(stories, timeCut=2):
    # convert timeCut from days to seconds
    newStories = []
    timeCut = int(timeCut) * 86400
    for story in stories:
        _, td_seconds = get_time_difference(story)
        if td_seconds < timeCut:
            newStories.append(story)
    return newStories
        
        
# Example usage
ticker = "DSP"
feed = get_feed(ticker)
story = return_story(feed, timeCut=2)