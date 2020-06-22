# Tests with XRootD

The `conf` folder contains the configuration files for the xrootd proxy plugin:
* `client-plugin-proxy.conf`: put it in `$HOME/.xrootd/client.plugins.d` to automatically prepend the plugin URL to the xrootd URL provided by the user.
* `proxy.conf` configuration file for the proxy machine itself. This needs at least to be launched as a different user.