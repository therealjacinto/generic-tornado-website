This repository aims to provide a generic, login-required website back-end using the [tornado](http://www.tornadoweb.org/en/stable/) framework written in python. This repository provides a working website (with minimal effort to setup) that includes 3 webpages: login, main menu, and a new user page. 

There are a few key features I included that every private website requires:
* A login system: In this repository, login is controlled using Google Oauth2. It is setup so that the user must provide their google credentials and google will send a token to the back-end once their account has been verified. There are two reasons why authentication was done this way. First, to provide an example of how to setup Google Oauth2 in a website, and second, to avoid the need of storing passwords in the database. Which brings us to our next feature...
* A database: This back-end uses SQLAlchemy as the database toolkit. Because there are many options to use as a database, SQLAlchemy makes it easy to switch systems (PostgreSQL, MySQL, SQLite, etc.) by changing a line of code. This makes connecting the backend to an existing database much easier than if the code was committed to a particular system. The database is used to store a users google id, their email, their name, their desired display name, and the date they joined.
* Cookie creation: The login system verifies if a user is logged in or not through secure cookies. The user is not allowed to access any files or pages in the website unless they are logged in. If they are not logged in, they are redirected to login page. These cookies can also be used for websockets.

In summary, the aim of this project is to provide a generic, login-required website that provides minimal effort to setup and is geared towards people who are unfamiliar with tornado as a back-end or who want to set something up quickly.

### Note:
I have made an effort to comment all the python code in this repository. Please go through all the code so that you understand what each line does and why it is necessary. This will help you in modifying this repository to your particular needs.

### What to install

I developed this repository on Windows, however because of the nature of Python, setup and implementation should be the same across all platforms.

The back-end is written entirely in Python 3 (for this project, I used Python 3.5.1), and thus requires you to install the latest version [here](https://www.python.org/downloads/). If you are unfamiliar with Python, I recommend going through the tutorials on their [website](https://docs.python.org/3/tutorial/index.html) as this project is not for beginner Python users.

After installing Python, we will need to install the required libraries to run our code. This repository requires 2 libraries, which are installed using `pip`. On windows, this can be done by opening the command prompt as an administrator, and running `pip install [library]` where [library] is the library you want to install (for example, when you install the tornado library, you would execute `pip install tornado` in the command prompt). The libraries required are:
* [tornado](https://pypi.python.org/pypi/tornado): web back-end framework (used version 4.3 in this project)
* [PyJWT](https://pypi.python.org/pypi/PyJWT): used to decrypt the google oauth2 keys (used version 1.4.0 in this project)
* [cryptography](https://pypi.python.org/pypi/cryptography): used by PyJWT to decrypt RSA signatures (used version 1.3.1 in this project)
* [SQLAlchemy](https://pypi.python.org/pypi/SQLAlchemy): database toolkit for storing users (used version 1.0.12 in this project)

### Setup

Once everything is installed, there are a couple things you will need to setup for the code to work properly:

1. In order to use Google OAuth 2.0, you will need to create a client ID using your own Google account so that Google will know who is requesting keys. This can be done by navigating to [console.developers.google.com](https://console.developers.google.com), clicking on "Credentials" under "API Manager" on the left-hand pane (if this is your first project you will need to follow steps to create a new project) , then in the "Credentials" sub-menu, create an "OAuth client ID" by clicking the "Create credentials" drop-down menu. You will need to add `localhost:8888/login/google` to the list of "Authorized redirect URIs" (this basically tells Google the path in your application that users are redirected to after they have authenticated with Google. If you are not using this repository on a development machine, or are planning to use another port other than 8888, this will need to reflect that). Once your ID has been created, you will need the Client ID and Client secret values.

2. Create a `settings.py` file and save it to whever main.py lives: Currently, my settings file is included in the gitignore file so that I can hide things like my cookie-secret and the Google OAuth 2.0 Client ID credentials. The settings file is just a file with the necessary import commands and a dictionary of settings. It should look something like this:
  ```python
  import os

  settings = {
      "cookie_secret": "generate_own_random_value", # For secure cookies
      "login_url": "/login",  # For the @tornado.web.authenticated decorator
      "google_oauth": {"key": "[Client ID]", "secret": "[Client secret]"}, # Google developer console credential
      "redirect_uri": "http://localhost:8888/login/google",  # Should match what you have in Google developer console
      "xsrf_cookies": True,  # To prevent cross-site request forgery
      "template_path": os.path.join(os.path.dirname(__file__), "templates"),  # Contains html files
      "static_path": os.path.join(os.path.dirname(__file__), "static")  # Contains static files, such as .css or .js. Not
                                                                      # necessary for this project. For more information
                                                                      # on templates and static files, see tornado docs.
  }
  ```

3. Database (optional): if you are planning to connect this to a database, do so via the
  ```python
  engine = create_engine('sqlite:///:memory:', echo=True)
  ```
line in `main.py`. Otherwise, it is currently setup to save the database in your local memory and will delete itself when you stop running the server.

### Deployment
Once everything is setup, you can deploy your application. On windows, you can do this by opening your command prompt, navigating to the directory that contains `main.py` using the `cd` command, and executing `python main.py`. Once the server has been activated, navigate to `localhost:8888` using your web browser and you should see the login page.

### Note
It is important to note that this is an http server, not an https server. It would be a good idea to use https since you are using sensitive google account information. All this requires is for you to add in your SSL certificate option as demonstrated [here](http://stackoverflow.com/a/18307308).