# graylog_sitewatch

A simple Python script checking status of url paths and sending results as GELF log to Greylog. Log-in functionality supported by default.

### Prerequisites

Script was developed and tested on Ubuntu OS. As no linux-specific libralies are used, it should be fully funtional in Windows environments as well.
 
Dev setup:
```
Ubuntu 18.04
Python 3.6
```
Prod setup:
```
Raspberry Pi 2 & rapbian X
Python 3.X
```

## Getting Started

- Copy a example config

      cp config.exmapl.json config.json

- Edit file to match your test cases
    
    Edit server details. TLS supports TLS by defaul
      
      ...
      "graylog_server": "greylog.example.com",
      "gralog_port": 12201,
      ...
      
    Configure texted domain(s) and (optional) login page and credentails
    
      ...
      "domain": "google.com",
      "loginx": {
        "post": "aaa",
        "username": "aaa",
        "password": "aaa"
      }
      ...
      
    For domain, create individual lookups with (optional) regexes to check and/or with (optional) minimal size of response content treshold.
    
        ...
        "url": "https://www.google.com",
        "description":"index googlepage",
        "patterns": 
            [
            "Google",
            "Gmail"
            ],
        "size_min": 1234 
        ...

### Usage

Running script in verbose (DEBUG) and custom config file:

```
python graylog_sitewatch.py --verbose --config custom_config.json
```

Script can be scheduler to run by cron:

```
% crontab -e
+ 
```

Running script from cron with custom virtual environment:

```

```


## Authors

* **Peter Matkovski** - *Initial work*

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License.

