# Iseq resources

Scripts that allow you to:
1) Adding a new tool to the JSON file
2) Iterating over the tools in the JSON file and checking the latest version, and in the case of a new version, adding a tooltip to JIRA
3) Update existing tool/database record in JSON after updating tool/database

## Install

```
pip install iseqresources
```

## Requirements

- python >=3.6
- jira >= 3.3.0
- requests >= 2.22.0
- python-gitlab >= 3.7.0


## Adding a new tool

First specify if you want to add tool or database. Input JSON file (`--input-json`) is from gitlab repo at path `json/tools.json` or `json/databases.json`. Default is `json/tools.json`.

```
add_tool --tools
```
or
```
add_tool --databases
```

You can also run on a local file:

```
add_tool \
    --input-json "/path/to/json/tools_or_databases.json"
```

It is better to add new tool directly to json file.

## Checking versions and add task to JIRA

Input JSON file (`--input-json` and `--info-json`) are from gitlab repo at path `json/tools.json` or `json/databases.json` and `json/info.json`. Default is `json/tools.json`.

```
check_versions --tools
```
or
```
check_versions --databases
```

You can also run on a local files:

```
check_versions \
    --input-json "/path/to/json/tools_or_databases.json" \
    --info-json "/path/to/json/info.json"
```

## Update existing tool/database record in JSON

Input JSON file (`--input-json`) is from gitlab repo at path `json/tools.json` or `json/databases.json`. Default is `json/tools.json`.

```
update_record --tools
```
or
```
update_record --databases
```

You can also run on a local file:

```
update_record \
    --input-json "/path/to/json/tools_or_databases.json"
```
