# Cyber Security Base 2023 - Project I

This is a demonstration of a vulnerable Django web application called `berries`. The server runs by default at `127.0.0.1:8000` and the app can be found at `127.0.0.1:8000/berries`. The admin page is `127.0.0.1:8000/admin`.

## Project overview

The makeshift purpose of the app is for users to add their foraged berries into a database and for other users to view in the app.

At first visit to `/berries` a user is welcomed and presented with a login form. There are two demo users and an admin account in the project for testing and they are:

- `alice:redqueen`
- `bob:squarepants`
- `admin:admin`

The HTML file corresponding to `/berries` is rendered differently once a user is logged in. After a successful login it displays a list of entries made by users. 

*(NOTE: At its default configuration, to demo security flaws, the list does not show the details correctly. This is because the Django templates are designed to work with the built-in database API and not raw SQL queries which I'm using to demonstrate injection. To test XSS in practice you must first fix the SQL injection flaw so that the `entry_list.html` includes links to the detail page.)*

## Flaws from the OWASP 2017 Top 10

1. Security Misconfiguration
    - Default or weak credentials (`admin:admin`)
2. Broken Access Control
    - Modifying URL grants access to details meant for authenticated users only
3. Injection
    - Filtering the entry list inserts unsanitized user input from a form into a raw SQL query
4. Cross-Site Scripting (XSS)
    - Detail view of an entry allows commenting. The comment is not checked for malicious input, e.g. using `<script>` tags works as they are not escaped. *(NOTE: To test XSS in practice you must first fix the SQL injection flaw so that the `entry_list.html` includes links to the detail page.)*
5. Broken Authentication
    - Session timeouts are (in my opinion) too long

## FLAW 1: Security Misconfiguration

The project’s superuser was created using a very bad combination of username and password, ‘admin:admin’, despite Django’s prompts about weak credentials. If any attacker wishes to try and gain access to the admin page this combination of username and password would probably be one of the first ones to try. Gaining access to admin rights compromises the whole application so this is a major issue.

Fixing can be done in a terminal via the `manage.py` file and `changepassword` argument. Type `python3 manage.py changepassword <username>` to start the process. In this particular case in place of ‘<username>’ you would of course write `admin`. You can also change the password via the browser in the admin page.

## FLAW 2: Broken Access Control

The base URL leads to a welcome page that is rendered differently depending on whether a user is logged in or not. From this page you cannot do much if you don’t log in. However, there is a flaw where you can access the detail view page of a berry entry just by manually altering the URL in the browser. For example, typing `127.0.0.1:8000/berries/entry/1` in the address bar will land you on the detail page even if you are not logged in. This is a flaw that leads to unauthorized information disclosure as these details are meant for valid users only.

The fix for this is quite simple thanks to the Django framework. You need to use a decorator for the appropriate view in `views.py`. The appropriate decorator `@login_required()` is already in place in the code but is commented out. It is set to redirect to the “main” page i.e `127.0.0.1.:8000/berries` because that’s where the login form is. So just by uncommenting that line, the problem is now fixed. You could also use a different approach by checking if the `request.user.is_authenticated` and then act accordingly, but the decorator is cleaner [1].

## FLAW 3: Injection

When a user is logged in, the root page shows an unordered list of all entries posted by users. There is a possibility to filter that list based on the `berry_type` property. This is now implemented in a very unsafe way where the value from the form field is placed directly without any sanitation to a raw SQL query which filters the list. This allows an attacker to inject SQL into the query and compromise the application.

*(NOTE: Because Django templates are meant to work with databases using the built-in API and not raw SQL the demonstration of this fault makes the `entry_list.html` template not render correctly while the corresponding view in `views.py` is using the unsafe way of filtering. Both the `entry_list` view and `entry_list.html` have the correct versions in the code commented out.)*

To fix such an obvious way to inject SQL directly into a query it is best to use the database API provided by the Django framework. It has built in measures to protect from SQL injection [2]. Like mentioned above, the correct way to filter the list is already in the code but just commented out.

## FLAW 4: Cross-Site Scripting (XSS)

Relating to the previous fault, due to built-in security measures in Django the demonstration of this fault requires purposefully bypassing the protection. In the `entry_detail.html` there is a feature that allows users to add comments to entries. Comments are database objects and have a property called `text`. In the `entry_detail.html` the value of the `comment.text` attribute is tagged as `safe` which means it bypasses Django’s own HTML escaping system. This makes it possible to include working `<script>` tags in the comment and makes the application vulnerable to XSS where an attacker could for example steal cookies and gain access to a valid user’s session.

Like mentioned the fix for this is very easy. Simply remove the `safe` tag from the template’s context variable to enable Django’s automatic HTML escaping again. [3]

## FLAW 5: Broken Authentication

From my app’s flaws this is the most ambiguous. The session timeout is defined in `settings.py` to equal to roughly 30 days in seconds. According to OWASP this can be considered a security flaw, since if a valid user forgets to explicitly log out of the app on a (public) computer, an attacker using the same computer later now has access to the user’s authenticated session. In my app’s case there isn’t any real sensitive information used or stored but this is still a privacy concern at the very least and in some other app this might be a more serious flaw. I see the session time out mainly as a UX vs security case. Not forcing the user to log in every time they use the app can lead to a more pleasant UX on expanse of security. I would however argue that there should be some sort of a prompt or setting where the user can decide if they want to remain logged in or not and they should be informed about the risks of staying logged in.

Like I tried to reason above, in my opinion, there is no single clearly defined “fix” for this. You can set for example the `SESSION_COOKIE_AGE` property in `settings.py` to whatever you prefer, and it will overwrite the global default setting from `django/conf/global_settings.py` which is two weeks. Depending on the nature of the app the proper value could be anything from seconds to hours to weeks. There is also an option to set the session to expire when the browser is closed. More advanced users can also set session properties programmatically.[4][5]

References:

[1]https://docs.djangoproject.com/en/4.2/topics/auth/default/#limiting-access-to-logged-in-users  
[2]https://docs.djangoproject.com/en/4.2/topics/security/#sql-injection-protection  
[3]https://docs.djangoproject.com/en/4.2/topics/security/#cross-site-scripting-xss-protection  
[4]https://docs.djangoproject.com/en/4.2/ref/settings/#session-cookie-age  
[5]https://docs.djangoproject.com/en/4.2/topics/http/sessions/#using-sessions-in-views
