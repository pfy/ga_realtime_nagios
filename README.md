Google Analytics Realtime for Nagios
=======================================

Installation
----

#### Requirements
You need 
[Google Analytics Realtime Beta API Access](https://docs.google.com/forms/d/1qfRFysCikpgCMGqgF3yXdUyQW4xAlLyjKuOoOEFN2Uw/viewform) and a valid client_secret.json file which you can get from the [google cloud console](https://cloud.google.com/console#/project).
You need the view ID of a google anlytics realtime account.

##### Developer Machine
Install the required python modules

	pip install oauth2client

copy `client_secret_*.json` to `client_secrets.json`

run the authentification flow

	python auth.py
	
This should generate a file called: `analytics.dat`

##### Server Machine

Copy `analytics.dat` to the server, to `/etc/nagios3/analytics.dat` and `chown nagios /etc/nagios3/analytics.dat`. The auth flow has to reset the token sometimes, so it needs write permission.

Install the required python modules

	pip install oauth2client google-api-python-client nagiosplugin
	
Copy `ga_realtime.py` to the the server and test it:

	python ga_realtime.py -D /etc/nagios3/analytics.dat -V YOUR_VIEW_ID
	
It should output something like:
	
	REALTIMEVISITORS OK - activeVisitors is 266 | activeVisitors=266;;;0


Move `ga_realtime.py` to the nagios3 plugin directory. In Debian Based Systems, this is: `/usr/lib/nagios/plugins`

Make an entry in the nagios3 commands file `/etc/nagios3/commands.cfg`

	define command{
        command_name    ga_realtime
        command_line    $USER1$/ga_realtime.py -D /etc/nagios3/google_auth_data -V $ARG1$ -w $ARG2$ -c $ARG3$
	}

Add service checks in your nagios files


	define service{
        use                             BASE_SERVICE
        host                            HOST
        service_description             activeVisitors
        check_command                   ga_realtime!YOUR_VIEW_ID!WARN_LEVEL!CRITICAL_LEVEL
	}

Restart Nagios `/etc/init.d/nagios3 restart`


Copyright and License
----
This projected is licensed under the terms of the GPL license.

&copy; 2013 David Gunzinger, [Smooh GmbH](https://www.smooh.ch)

