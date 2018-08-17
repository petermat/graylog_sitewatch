# graylog_sitewatch

A simple Python script checking status of url paths and sending results as GELF log to Greylog. Log-in functionality supported by default.

### Prerequisites

Script was developed and tested on Ubuntu OS. As no linux-specific libralies are used, it should be fully funtional in Windows environments as well.
 
Dev setup:
```
Ubuntu 18.04
Python 3.6
```
RPI setup:
```
Raspberry Pi 2  
Rapbian Version:June 2018
    Release date:2018-06-27
    Kernel version:4.14
Python 3.5
```
Reruirements:
```
pygelf >= 0.3.4
requests >= 2.19.1
urllib3 >= 1.23
```

## Getting Started

- Copy a example config

      # cp config.exmapl.json config.json

- Edit file to match your test cases
    
    Edit server details. TLS supports TLS by defaul
      
      ...
      "graylog_server": "greylog.example.com",
      "gralog_port": 12201,
      ...
      
    Configure texted domain(s) and (optional) login page, credentails and name of csrf cookie key from cookie.
    
      ...
      "domain": "yoursite.com",
      "loginx": {
        "login_url": "https://yoursite.com/login",
        "csrftokenname":"csrftoken",
        "username": "username",
        "password": "password"
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

    See example files config.example.json and config.example_withlogn.json.

### Usage

Running script in verbose (DEBUG) and custom config file:

```
# python graylog_sitewatch.py --verbose --config custom_config.json
```

Script can be scheduler to run by cron:

```
# mkdir workspace && cd workspace
# git clone https://github.com/petermat/graylog_sitewatch.git

# crontab -e
0 */6 * * * cd /home/pi/workspace/graylog_sitewatch && /usr/bin/python3 graylog_sitewatch.py >> /tmp/graylog_sitewatch.log 2>&1

```

Running script from cron with custom virtual environment:
    
Running source from a cronfile won't work as cron uses /bin/sh as its default shell, which doesn't support source. You need to set the SHELL environment variable to be /bin/bash:
```
SHELL=/bin/bash
0 */6 * * * source /path/to/virtualenv/bin/activate && /path/to/graylog_sitewatch.py --verbose > /dev/null
```


## Authors

* **Peter Matkovski** - *Initial work*

See also the list of [contributors](#) who participated in this project.

## License

This project is licensed under the MIT License.

