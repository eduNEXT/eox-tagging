# eox-tagging

## Features

Place your plugin features list.

## Installation

### Open edX devstack

- Clone this repo in the src folder of your devstack.
- Open a new Lms/Devstack shell.
- Install the plugin as follows: pip install -e /path/to/your/src/folder
- Restart Lms/Studio services.

## Usage

Examples:

```
"EOX_TAGGING_DEFINITIONS":[
  {
    "tag_type":"example_tag_1",
    "belongs_to": "User",    # default = Site
    "validate_target_type": "User",
    "validate_access": "Private",
    "validate_tag_value": {"in": ['value1, value2']}
  },
  {
    "tag_type":"example_tag_2",
    "belongs_to": "Site",
    "validate_target_type": {"object":"CourseOverview"},
    "validate_tag_value": {"OpaqueKey": "course_key"}
    "validate_<FIELD>": {"regex": "yes|no"} | {"in": ["list"]} | "exists": true
  },
  {
    "tag_type":"example_tag_3"
    "validate_target_type": "Enrollment",
    "validate_expiration_date": "exists",
  },
  {
    "tag_type":"example_tag_4"
    "validate_target_type": "CourseUnit",
    "validate_tag_value": {"OpaqueKey": "resourse_locator"}
    "validate_expiration_date": "exists",
  }
]

```



## Contributing

Add your contribution policy. (If required)
