# release-to-jira

A GitHub action to automatically create releases on JIRA.

Uses manual tag name versus automatic to allow push by PR.

Creates a release on Github. Uses its auto-generated description to find related JIRA issues and updates their "Fix versions" field. If a release matching the tag doesn't exist on JIRA, it will be automatically created.

This flow assumes auto-generated release notes will include JIRA issue keys. This can be achieved by including JIRA issue key in PR titles.

## Inputs

|Input|Description|Example|
|---|---|---|
|`jira_server`|JIRA server URL.|`https://company.atlassian.net`|
|`jira_project`|JIRA project key.|`PRJ`|
|`jira_user`|JIRA user with project admin permission.|`apiuser@company.com`|
|`jira_token`|JIRA token. Managed [here](https://id.atlassian.com/manage-profile/security/api-tokens).|`abcdef12345678`|
|`release_tag`|Manual name for release tag|`v20.0.1`|

## Usage

Run when a new tag is created:

```yaml
on:
  push:
    branches:        
      - 'main'
jobs:
  jira-release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: Medsien/release-to-jira@main
        with:
          jira_server: 'https://company.atlassian.net'
          jira_project: 'PRJ'
          jira_user: 'user@company.com'
          jira_token: '${{ secrets.JIRA_TOKEN }}'
          release_tag: 'v20.0.1'
```
