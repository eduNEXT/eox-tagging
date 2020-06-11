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
    "owner_object_type": "User",    # default = Site
    "validate_target_object_type": "User",
    "validate_access": {"equals":"Private"},
    "validate_tag_value": {"in": ['value1, value2']}
  },
  {
    "tag_type":"example_tag_2",
    "owner_object_type": "Site",
    "validate_target_object": {"object":"CourseOverview"},
    "validate_tag_value": {"OpaqueKey": "CourseKey"}
    "validate_<FIELD>": {"regex": "yes|no", "in": ["list"], "exists": true}
  },
  {
    "tag_type":"example_tag_3"
    "validate_target_object_type": "Enrollment",
    "validate_expiration_date": {"exists": True},
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
