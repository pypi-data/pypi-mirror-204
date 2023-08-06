<a href="https://www.extrinsec.com">
  <img src="https://cdn.extrinsec.com/images/logos/logo.png" />
</a>

Runtime application self-protection platform for [Python](https://www.python.org).

```Python
# set required environment variables ES_POLICY_GROUP_NAME and ES_LICENSE_KEY as provided or configured in your app, e.g.
# os.environ["ES_POLICY_GROUP_NAME"] = "observeAll.ability";
# os.environ["ES_LICENSE_KEY"] = "<your unique license key>";

# load the appdefender module
import 'appdefender'
```

## Installation

```console
python3 -m pip install appdefender
```

It is recommended that you register an account on https://app.extrinsec.com/ and configure your own policy rules for the best protection.

## Features

- Quick and simple setup
- **Observe**, **Deny** or **Grant** any combination of the following
  - outbound network data
  - read/write tmp or app directories
  - create/spawn child processes
- Option to terminate process for policy violations
- Ability to whitelist domains
- Fast & Reliable, no wrapping or monkey-patching of your code
- Easy collaboration between dev and ops teams with role based access
- View all events centrally in the web application

## Docs & Community

- [Website](https://www.extrinsec.com/appdefender)
- [App](https://app.extrinsec.com/)
- [FAQ](https://www.extrinsec.com/faq)
- Community Support

## License

© Copyright 2023 Extrinsec LLC, all rights reserved.
