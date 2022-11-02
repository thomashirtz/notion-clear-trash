from notion.client import NotionClient
from typing import Dict, List, Any


def get_space_dict(client: NotionClient) -> Dict[str, str]:
    try:
        spaces = client.post("loadUserContent", {}).json()["recordMap"]["space"]
        return {space_id: space_dict['value']['name'] for space_id, space_dict in spaces.items()}
    except KeyError as e:
        return {client.current_space.id: 'Default space'}


def get_trash(client: NotionClient, space_id: str) -> List[str]:
    query = {
              "type": "BlocksInSpace",
              "query": "",
              "filters": {
                "isDeletedOnly": True,
                "excludeTemplates": False,
                "isNavigableOnly": True,
                "requireEditPermissions": False,
                "ancestors": [],
                "createdBy": [],
                "editedBy": [],
                "lastEditedTime": {},
                "createdTime": {}
              },
              "sort": "Relevance",
              "limit": 1000,
              "spaceId": space_id,
              "source": "trash"
            }
    results = client.post('/api/v3/search', query)
    block_ids = results.json()['results']
    return [block_id['id'] for block_id in block_ids]


def chunks(lst: List[Any], n: int) -> List[Any]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def delete_permanently(client: NotionClient, block_ids: List[str]) -> None:
    for block_batch in chunks(block_ids, 10):
        try:
            client.post("deleteBlocks", {"blockIds": block_batch, "permanentlyDelete": True})
            print(f'Deleted: {block_batch}')
        except Exception as e:
            print(f"Couldn't delete: {block_batch} ({e})")


if __name__ == "__main__":
    token = input('Please enter your auth token: ')
    client = NotionClient(token_v2=token)
    space_dict = get_space_dict(client)
    for space_id, space_name in space_dict.items():
        print(space_name)
        block_ids = get_trash(client, space_id)
        delete_permanently(client, block_ids)
        print()

    print('Successfully cleared all trash blocks.')