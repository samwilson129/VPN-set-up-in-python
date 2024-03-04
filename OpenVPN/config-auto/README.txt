This directory or its subdirectories should contain OpenVPN
configuration files each having an extension of .ovpn
that should be automatically started at boot up.

When OpenVPNService is started, a separate OpenVPN
process will be instantiated for each configuration file.

OpenVPN GUI scans this directory and its subdirectories for
configuration files and lists them under the "Persistent Profiles"
menu unless that feature is turned off. If OpenVPN PLAP dll
is registered, these configurations are also accessible from the login
screen for "Start Before Logon".
