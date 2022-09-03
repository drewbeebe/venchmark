## Venchmark - Open Source Vendor/Third Parity Risk Management System

This is a FOSS project for third party risk management in IT Operations. Knowing who has what data, how sensitive that data may be and understanding the risk landscape in your enterprise is the purpose of using this tool.

It is built using Django (future builds will use Django REST API and pair it with Angular JS Framework for the frontend).

Venchmark is actively developed and we will release quite frequently.

__This is web-based software__. This means there is no executable file (aka no .exe files), and it must be run on a web server and accessed through a web browser. It runs on any Mac OSX, flavor of Linux, as well as Windows, and we will publish a Docker image soon, to help make adoption easier.

-----

### Installation

Installing Venchmark on your server is simple and straight-forward:

Step 1. git clone the repo
Step 2. cd into the repo and run ./genskey.sh
Step 3. run pipenv shell
Step 4. run pip install -r requirements.txt
Step 5. python3 ./manage.py createsuperuser
This will walk you through creating a super user account. You can then use that account to set up the application and users for your organization.
Step 6. python3 ./manage.py runserver

-----
### User's Manual
Soon to come!.

-----
### Bug Reports & Feature Requests

Feel free to check out the [GitHub Issues for this project](https://github.com/drewbeebe/venchmark/issues) to open a bug report or see what open issues you can help with. Please search through existing issues (open *and* closed) to see if your question has already been answered before opening a new issue.

-----

### Upgrading

TBD

------

### Contributing

We welcome your help and contributions! Get in touch with us and we'll be glad to hear from you!