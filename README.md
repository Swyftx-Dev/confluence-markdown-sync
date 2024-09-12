# Confluence Markdown Sync Action

This GitHub Action copies the contents of a Markdown .md file or an entire folder of markdown files to Confluence Cloud Pages. It can create a new Confluence page for each file and organise subfolders as child pages.

## Getting Started

```yml
# .github/workflows/my-workflow.yml
on: [push]

jobs:
  dev:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - uses: Swyftx-Dev/confluence-markdown-sync@v2
        with:
          from: './docs/runbooks'  # Specify folder path
          to: '123456'     # Root page ID in Confluence
          cloud: <my-confluence-cloud-id>
          user: <my.user@example.org>
          token: <my-token>

```

## Authentication

Uses basic auth for the rest api.

- `cloud`: The ID can be found by looking at your confluence domain: `https://<cloud>.atlassian.net/...`

- `user`: The user that generated the access token

- `token`: You can generate the token [here](https://id.atlassian.com/manage-profile/security/api-tokens). Link to [Docs](https://confluence.atlassian.com/cloud/api-tokens-938839638.html)

- `to`: The page ID can be found by simply navigating to the page where you want the content to be postet to and looke at the url. It will look something like this: `https://<cloud-id>.atlassian.net/wiki/spaces/<space>/pages/<page-id>/<title>`

## Syncing Folders and Subfolders
- from: You can specify a single markdown file or an entire folder of markdown files.
-- If a folder is specified, each .md file in the folder will be synced as a new Confluence page.
-- Subfolders will be recursively traversed, and child pages will be created for each subfolder, maintaining the folder structure in Confluence.
- to: The page ID where the folder will be uploaded. For folders, this represents the root page under which new pages and subpages will be created.

### Using secrets

It's **higly reccomended** that you use secrets!

To use them you need them to specify them before in your repo. [Docs](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets)

Then you can use them in any input field.

```yml
# .github/workflows/my-workflow.yml
# ...
token: ${{ secrets.token }}
```

## Development

1. Clone the repo
2. Install [act](https://github.com/nektos/act)
3. Create the same config in the repo folder as in the getting started section above.
4. Change `uses:  Swyftx-Dev/confluence-markdown-sync ` -> `uses: ./`
5. Create an example markdown file `Some.md` and set it in the config `from: './Some.md'`
6. Run locally `act -b`

### With secrets

You can simply create a `.secrets` file and specify it to `act`.

```
TOKEN=abc123
```

```yml
# .github/workflows/dev.yml
# ...
token: ${{ secrets.token }}
```

```bash
act -b --secret-file .secrets
```
