# notion-clear-trash

Script to clear the trash of all the workspace of your Notion account.

This repository is strongly inspired from the [notion-clear-trash](https://github.com/axyyu/notion-clear-trash) from [https://github.com/axyyu]. However, some modification has been done in order to delete the trash from all the workspace instead of the current's workspace.

**/!\ Use this script at your own risk, as it will permanently delete pages from your Notion account.**

## Installation

```
pip install git+https://github.com/thomashirtz/notion-clear-trash#egg=notion-clear-trash
```

## Utilization

```
notion-clear-trash `token`
```

The token is the API token, it can be found by:
 1. going to [www.notion.so](https://www.notion.so).
 2. Press `F12` to get to display the `Browser Developer Tools`.
 3. Go to the `Storage` section, then the `Cookies` section, finally search for the value of `token_v2`.
    