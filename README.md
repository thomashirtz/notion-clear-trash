# notion-clear-trash

Script to clear the trash of all the workspaces of your Notion account.

This repository is strongly inspired from the project [notion-clear-trash](https://github.com/axyyu/notion-clear-trash) of the user [axyyu](https://github.com/axyyu). However, some modification has been done in order to delete the trash of all the workspaces instead of only the current workspace.

⚠️**Use this script at your own risk, as it will <u>permanently</u> delete pages from your Notion account.**

## Installation

```
pip install git+https://github.com/thomashirtz/notion-clear-trash#egg=notion-clear-trash
```

## Utilization

```
notion-clear-trash `token`
```

The token is the API token, the steps to get it are the following:
 1. Go to [www.notion.so](https://www.notion.so).
 2. Press* `F12` to get to display the `Browser Developer Tools`.
 3. Go to the `Storage` section, then the `Cookies` section, finally search for the value of `token_v2`.
    
