import miniflux
from typing import Any, Dict, List
from lumeny.ConfigLoader import ConfigLoader
import random

# write a function that connects to miniflux client using api key and url
def connect_miniflux(url: str, api_key: str) -> miniflux.Client:
    return miniflux.Client(url, api_key=api_key)

# a function that prints all the feeds' name and id
def print_feeds(feeds: List[Dict]) -> None:
    # sort by feed id
    feeds.sort(key=lambda feed: feed["id"])
    # print number of feeds
    print(f"Number of feeds: {len(feeds)}")
    for feed in feeds:
        print(f"Feed id: {feed['id']}, Feed name: {feed['title']}")
        # print such that title ,id and site_url are aligned

# write a function that get all the entries from a feed, optionally select by starred or unread, and return a list of entry id
def get_entries_from_feed(
    client: miniflux.Client, feed_id: int, starred: bool = False, unread: bool = False
) -> List[int]:
    # get entries from feed
    entries: Dict = client.get_entries(feed_id= feed_id, starred=starred, unread=unread)
    
    # since the entries are cut if the number is above 100, we need to fetch the entries again with limit from total
    total: int = entries["total"]
    entries: List[Dict] = client.get_entries(feed_id = feed_id, starred=starred, unread=unread, limit=total)
    # assert that the total is equal to the length of entries
    assert total == len(entries["entries"])
    
    # print type of total
    print(f"Total type: {type(total)}")
    
    # get only entry id
    entry_ids: List[int] = [entry["id"] for entry in entries['entries']]
    return entry_ids

# write a function to find feed by its id, use map instead of for loop
def find_feed_by_id(feed_id: int, feeds: List[Dict]) -> Dict:
    return next(filter(lambda feed: feed["id"] == feed_id, feeds))

# TODO create embedding from feed content

# TODO add feeds' embedding to "liked" category in embeddings

# TODO randomly select n feeds from all unread feeds

# TODO randomly select n feeds from all started feeds

def test():
    
    # connect
    config_loader = ConfigLoader()
    config = config_loader.get_config()
    miniflux_config = config["miniflux"]
    client: miniflux.Client = connect_miniflux(
        miniflux_config["url"], miniflux_config["api"]
    )

    # get feed ids
    feeds: List[Dict] = client.get_feeds()
    # get only id
    feed_ids: List[int] = [feed["id"] for feed in feeds]
    
    print("feed ids are as follows: ")
    print(feed_ids)

    # randomly choose a feed from given feed ids
    feed_id: int = random.choice(feed_ids)
    print(f"randomly chosen feed id is: {feed_id} ")

    # get feed by id
    feed: Dict = find_feed_by_id(feed_id, feeds)
    print(f"feed with id {feed_id} is: {feed['title']}")
    
    # get entries from feed
    entries = get_entries_from_feed(client, feed_id)
    
    # print total number of entries
    print(f"Total number of entries: {len(entries)}")
    


if __name__ == "__main__":
    test()
