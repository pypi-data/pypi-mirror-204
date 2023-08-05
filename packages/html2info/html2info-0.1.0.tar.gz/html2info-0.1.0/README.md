# html2info

`html2info` is a Python package that allows you to parse LinkedIn profiles from raw HTML and return structured information in JSON format.

## Features

- Extracts profile information such as name, title, location, profile photo, about, experience, and education.
- Returns a JSON object containing the parsed data.

## Installation

Install `html2info` using pip:

```bash
pip install html2info
```

## Usage

Here's an example of how to use html2info:

from html2info.linkedin import Person

url = "https://www.linkedin.com/in/iglovikov/"
raw_data = "..."  # Raw HTML content of the LinkedIn page

person = Person(url, raw_data)
person.parse()
print(person.to_dict())

```json
{
  "linkedin_url": "https://www.linkedin.com/in/iglovikov/",
  ...
}
```
