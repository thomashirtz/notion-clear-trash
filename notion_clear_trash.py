from typing import Dict
from typing import Iterator
from typing import List
from typing import TypeVar

from notion.client import NotionClient

T = TypeVar('T')


# todo GitHub descriptions, ...
# todo requirements
# todo setup
# todo readme
# todo pre-commit
# todo post on reddit
# todo add TQDM


def get_space_dict(client: NotionClient) -> Dict[str, str]:
    """Function that returns a mapping from `space_id` to `space_name` using
    a Notion client.

    Args:
        client: Notion client.

    Returns:
        Mapping `space_id` to `space_name`.
    """
    response = client.post(endpoint='loadUserContent', data={}).json()
    space_list = response['recordMap']['space']
    return {id_: dct['value']['name'] for id_, dct in space_list.items()}


def get_trashed_block_id_list(client: NotionClient, space_id: str) -> List[str]:
    """Function that retrieve a list of `block_id` in the trash of a specific
    `space_id` using a Notion Client.

    Args:
        client: Notion client.
        space_id: Space id.

    Returns:
        List of block_id that are in the trash.
    """
    query = {
        'type': 'BlocksInSpace',
        'query': '',
        'filters': {
            'isDeletedOnly': True,
            'excludeTemplates': False,
            'isNavigableOnly': True,
            'requireEditPermissions': False,
            'ancestors': [],
            'createdBy': [],
            'editedBy': [],
            'lastEditedTime': {},
            'createdTime': {},
        },
        'sort': 'Relevance',
        'limit': 1000,
        'spaceId': space_id,
        'source': 'trash',
    }
    results = client.post(endpoint='/api/v3/search', data=query)
    block_list = results.json()['results']
    return [block_id['id'] for block_id in block_list]


# todo docstring
def delete_permanently(
        client: NotionClient,
        block_id_list: List[str],
        chunk_size=10,
) -> None:
    for block_id_batch in chunk_iterator(block_id_list, chunk_size=chunk_size):
        try:
            query = {
                'blockIds': block_id_batch,
                'permanentlyDelete': True,
            }
            client.post(endpoint='deleteBlocks', data=query)
            print(f'\tDeleted: {block_id_batch}')
        except Exception as e:
            print(f"\tCouldn't delete: {block_id_batch} ({e})")


# todo improve docstring
def chunk_iterator(lst: List[T], chunk_size: int) -> Iterator[List[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def main() -> int:  # todo docstring
    # Parsing arguments
    token = input('Please enter your auth token: ')  # todo argparse

    # Get the client and the spaces
    client = NotionClient(token_v2=token)
    space_dict = get_space_dict(client=client)

    # Iterating through the spaces to delete the trashed pages
    for space_id, space_name in space_dict.items():
        print(space_name)
        block_id_list = get_trashed_block_id_list(
            client=client, space_id=space_id,
        )
        delete_permanently(client=client, block_id_list=block_id_list)
        print()

    # Logging and returning the exit code
    print('Successfully cleared all trash blocks.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
