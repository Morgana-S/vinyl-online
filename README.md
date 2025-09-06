# Vinyl Online - E-Commerce focused Web Application for Purchasing Vinyl Records
![Vinyl Online Device Mockups](/documentation/images/mockups/all-devices-black.png)

# About
Vinyl Online is an e-commerce site with a focus on selling vinyl records. Vinyl Online is a web application that utilises HTML, CSS, JavaScript and Python, as well as utilising the Django and Bootstrap frameworks. E-Commerce utility is also provided using Stripe.

**The deployed version of the site can be accessed [here.](https://vinyl-online-d54f03c987e4.herokuapp.com/)**

# UI/UX Design
Following on from my work with [Ourglass](https://github.com/Morgana-S/ourglass), I made this project as user-centric as possible also. The wireframes for this project can be found [here](/documentation/wireframes/vinyl-online-wireframes.pdf), but a brief writeup of my considerations will be provided below.

In the process of developing the UI and UX for Vinyl Online, I focused on three archetypes of user, and aimed to find representative examples of each amongst the people I know. These three archetypes are as follows:

- **Audiophiles**: People who are interested in vinyl records for the sound quality.
- **Art enthusiasts**: People who are interested in vinyl records for the album art.
- **Traditionalists**: Older people who are used to listening to and prefer vinyl record players over more modern media tools, such as digital or CDs.

The wireframes will outline how I considered each of these audiences, including how to capture each audience, and profiles on representative members of each archetype.
Given that Vinyl Online simultaneously wants to appeal to these three seperate archetypes, the most pleasing UI 'theme' was one that was high contrast but visually appealing. As such, I decided that a dark site with white text and red accents was the most desirable approach. This kind of theme is reminiscent of rock music, and also really helps the album art for each record to 'pop' on the page. Bootstrap's built-in classes were instrumental in achieving this design. For ordinary site users, bootstrap's 'danger' class, ordinarily used for warnings, is used to promote the user pathway; buttons to interact with the site often have a red background. Tooltips and Font Awesome icons were also employed to keep the site's modern feel, while helping to explain each button's purpose.

Vinyl Online was created with the following design principles in mind:

- Simple, but Detailed: If you are just looking to purchase a specific record, that process is very straightforward, but if you wish to find more information about pressings and formats, each record detail page has this information.

- Make discovery easy: Records can be found by searching by artist or record name, but users can also browse records in a variety of ways, including by latest release, by all records, and by genres.

- Site interaction as a dialogue: The community part of the site is very important. This houses all of the two-way interactions between the user, but especially reviews and support tickets. The foundation has been laid for the user to interact with site staff in ways that benefit them, which is a practice that will keep users coming back.

- Responsivity: Bootstrap has made it very easy to create responsive site designs - when paired with media queries, it helps to ensure that all site pages look good on almost any device.

# Target Audiences

Vinyl Online targets three main audiences, as discussed in the UI/UX seciton above. Personas have been created for each type of audience, but I'll summarise the desires of each audience here:

## Audiophiles

- The website should contain as much information about the records as possible.
- There should be plenty of information on after-purchase support.
- It should be immediately obvious where to go for whatever the user needs.

## Art Enthusiasts

- The album covers should be front and center, with plenty of high quality images of each record.
- Design should be consistent and uniform, however - that way it's very easy for users to intuit how to navigate the site.
- Customer support should be easy to access; this allows users to feel confident in their purchases.

## Traditionalists

- There should be information on the site that allows users to know the business is operating 'The Right Way'.
- Contact information should be front and center - highlighting the fact that human-to-human support was available is also important.
- A wide variety of records is also important to stock - Vinyl Online needs to cater to different tastes.

## General

- Website should be simple in design, and not center around those who are capable with technology.
- User interaction is important and keeps users coming back for more.

# Epics and User Stories

Early on in the design phase of the website, I created the Vinyl Online User Pathway, which is a flowchart that envisions how users would interact with the site.
![Vinyl Online User Pathway](/documentation/diagram-files/vinyl-online-user-pathway-white-bg.png)

This diagram helped me with mapping out the website into **Themes, Epics, and User Stories**.

## Themes

Themes within the pathway are expressed as general categories for what exactly the user is doing - Navigaton, Authentication, Engagement and Checkout.

## Epics

Each of these themes was then broken down into one or more Epics - these Epics were named for the actual action the user intends to take;
 for example, with the Navigation theme, the epics include **Finding Content** and **Moving Between Site Pages**.

 ## User Stories

 Each of these Epics was then broken down into individual user stories. The full details of each epic and their user stories can be found in the wireframes, and each user story is labelled with both its Theme and MoSCoW prioritization category on the [Issues Page](https://github.com/Morgana-S/vinyl-online/issues?q=is%3Aissue%20state%3Aclosed) and [Project Board](https://github.com/users/Morgana-S/projects/5), but an example has been provided below:

 ### EPIC - Finding Content (where to find records)

#### User Stories

As a **site user**, I can **search for records using a variety of terms** so I can **find the exact record I'm looking for**.

**Acceptance Criteria**

**AC1** - The site contains a search bar which allows users to search for records.

**AC2** - There should be an option to search by both album name and artist name.

**AC3** - Leaving the search field blank will lead to a search that includes all records.

**AC4** - The records should be sorted in a sensical order, and have the option to resort the search query by alphabetical order or release date.

---

As an **audiophile**, I want **to browse by genre using a dropdown list** so I can **explore records in styles I enjoy**.

**Acceptance Criteria**  

**AC1** – The navigation bar should have a "search by genre" button which contains a dropdown list of genres.

**AC2** – Selecting a genre displays results only for records that fall under that category.  

**AC3** – Selecting a record from the search result will take the user to the record details page.

# Features

## Index Page
![Index Page](/documentation/images/feature-images/index.gif)

The site has an index page which displays a hero carousel for site features that the user will be interested in, such as featured records as well as a way to quickly navigate to latest releases and popular genres.

## Context-sensitive Navbar
![Navbar](/documentation/images/feature-images/navbar.gif)

The users navbar changes depending on if they are logged in or not, providing relevant options to both authenticated and anonymous users. Staff users will also have options on their navbar to assist with site management.

## Search For Records
![Search Async](/documentation/images/feature-images/search.gif)
![Search Page](/documentation//images/feature-images/search-results.gif)

Users are able to search for records or artists using the search bar at the top of the page. This utilises async requests to obtain relevant results without necessarily refreshing the page - however, if the user wishes to see a full list of results, pressing search will take them to a results page, which has pagination for both artists and records.

## Record Details
![Record Details](/documentation/images/feature-images/record-detail.gif)

Users can browse individual record detail pages, which contains images for the record, allows them to add records to the basket, and shows reviews for the record if they exist. The user receives a toast if they add the record to their cart, and their cart in the top right of the site updates with the current item count. Users can also click the eye icon next to the artist name to view the artist page, and the genre badges to browse by that genre.

## Reviewing Records
![Reviewing Records](/documentation/images/feature-images/reviewing-records.gif)

Users who have purchased records - and those records have been delivered - can leave reviews for the records and service they've received. These reviews need to be approved by an administrator before being visible to the public.

The reviews are aggregated and count towards the records average rating based on the review ratings on each review.

## Deleting Reviews
![Deleting Reviews](/documentation/images/feature-images/deleting-reviews.gif)

Reviews can also be deleted by the user, if they wish to write a different review. Reviews are not currently editable, as I do not foresee a user's review needing to change after being posted.

## Adding Records
![Adding Records](/documentation/images/feature-images/adding-records.gif)

Staff can add records via the record management section. Filling out a form and adding images is possible - records are initially hidden from sale by default, but this can be disabled if the staff is happy with the record details.

## Django Custom Commands for Adding Records using the Discogs API
![Fetch Artist Images](/documentation/images/feature-images/fetch-artists.gif)
![Fetch Album](/documentation/images/feature-images/fetch-album.gif)

As part of the lengthy process of populating the records, I made use of the Discogs API to populate artist photos and record inforamtion. While this isn't accessible on the front-end side of things, back-end administrators will likely find this useful.

## Form Verification
![Form Validation](/documentation/images/feature-images/form-validation.gif)

All forms that the user is exposed to are validated to ensure that any necessary information is provided.

## Editing Records
![Editing Records](/documentation/images/feature-images/editing-records.gif)

Records can be edited by staff users from the record detail page, allowing for changes to be immediately seen by editors and users.

## Deleting Records
![Deleting Records](/documentation/images/feature-images/deleting-records.gif)

Staff users can also delete records from the record detail page.

## Artist Details
![Artist Details](/documentation/images/feature-images/artist-details.gif)

Each artist also has a debut page with a short bio, as well as the genres their music covers and their available records.

## Adding Artists
![Adding Artists](/documentation/images/feature-images/adding-artists.gif)

Artists can be added to the site on the front end with a simple form.

## Editing Artists
![Editing Artists](/documentation/images/feature-images/editing-artists.gif)

Artist information and profile photos can be changed by staff to reflect any changes in details.

## Deleting Artists
![Deleting Artists](/documentation/images/feature-images/deleting-artists.gif)

Artists can also be deleted from their Artist Detail page.

## Shopping Basket
![Shopping Basket](/documentation/images/feature-images/shopping-basket.gif)

The user has access to a shopping basket when adding records, which shows the records in the basket, costs, features automatically updating pricing based on quantities, and also shows users suggestions on records if their basket is empty.

## Checkout
![Checkout Process](/documentation/images/feature-images/checkout.gif)

The checkout process includes payment processed by Stripe, and provides the user with an order confirmation as well as an email copy of their order.

## Selecting Addresses for Authenticated Users
![Selecting Addresses](/documentation/images/feature-images/selecting-addresses.gif)

Authenticated users can select from their delivery addresses, but they can also add a new address and then save this to their preferred addresses for an expediated checkout process.

## Record Analytics
![Record Analytics](/documentation/images/feature-images/record-analytics.gif)

Staff have access to the record analytics page for the site, whcih contains information about the most popular sales, low stock of records, and a graph of weekly sales.

## Order Confirmation
![Order Confirmation](/documentation/images/feature-images/order-confirmation.gif)

As well as receiving an email confirmation, authenticated users can view their order history on their profile.

## Account Registration and Login
![Account Registration](/documentation/images/feature-images/account-registration.gif)
Users are able to register accounts on the website using django all-auth. Users are then required to verify their email address as part of the account creation process.
Django Allauth's default templates have been replaced with custom ones that match the site's design.

## Account Profile
![Profile](/documentation/images/feature-images/profile.gif)

Accounts have a profile page, which contains information about the user's information, delivery addresses, order history and support tickets. Users can also change their password on the profile, allowing it to act as a hub for account details.

## Editing Profile Details
![Editing Profile](/documentation/images/feature-images/editing-profile.gif)

Profile information can be edited easily from the profile page.

## Adding Delivery Addresses
![Adding New Delivery Addresses](/documentation/images/feature-images/adding-delivery-addresses.gif)

Adding new delivery addresses is simple, and these addresses will then show up in the checkout part of the site.

## Removing Delivery Addresses
![Removing Delivery Addresses](/documentation/images/feature-images/removing-delivery-addresses.gif)

When a user no longer needs their delivery address, deleting it is simple, and confirmation is acquired to ensure that the user wants to delete.

## Viewing Order History
![Order History](/documentation/images/feature-images/order-history.gif)

Authenticated users can see their previous orders in the profile section, allowing them to easily keep track of what's happening with their order.

## Contacting Support
![Contacting Support](/documentation/images/feature-images/contact-support.gif)

Support tickets can be created for a variety of issues, and the user will receive an email to their email address confirming the support ticket has been created.


## Viewing Support Tickets
![Viewing Support Tickets](/documentation/images/feature-images/viewing-support-tickets.gif)

All users can access their support ticket via the link in the email they receive, but authenticated users can also access their support tickets via the profile page when logged in.

## Account Logout
![Account Logout](/documentation/images/feature-images/logout.gif)

Users can also sign out of their account at any time, allowing for them to navigate the site using public devices.

## Privacy Policy
![Privacy Policy](/documentation/images/feature-images/privacy-policy.gif)

The website features a privacy policy generated with a Privacy Policy generator. This allows users to understand how collected data is used and is vital from a regulatory perspective.

## Newsletter Signup
![Newsletter Subscription](/documentation/images/feature-images/newsletter.gif)

Both authenticated and anonymous users are able to subscribe to the newsletter, and will receive an email confirming they have been signed up.

## Robots.txt
![Robots.txt](/documentation/images/feature-images/robots.txt.png)

The site features a Robots.txt file, which defines how crawlers are used to access parts of the site.

## Sitemap.xml

![Sitemap.xml](/documentation/images/feature-images/sitemap.xml.png)

The site also has a Sitemap, which provides information about the pages and layout of the site, making them more accessible to search engine crawlers.

# Models

This project uses a variety of models, some of which have CRUD functionality for users of the site. A lot of the models in the records app have limited front-end CRUD functionality due to their
use cases - it's not often that a user, staff or otherwise, would need to delete a genre, for example. However, for most models on the site, CRUD functionality does exist in one form or another, whether to authenticated or staff users. These models were laid out in an Entity Relationship Diagram for advanced planning of the project details, which has been included below (full image size can be found [here](/documentation/diagram-files/vinyl-online-erd.png) if the below image is too small):

![Site Models](/documentation/diagram-files/vinyl-online-erd.png)

Details of the models can be found below:

## Records App

### Artist Model

The artist model acts as a database model for storing information about artists, primarily used to link records together by artist.
Fields include id, name, slug, image, debut_year, and bio.

The artist model acts as the foundation of the records app - the records are linked to their artist by foreign key. 

The model contains custom save function infrastructure which allows for slugs to be automatically generated, and users can also see which genres the musician makes, which are served from the collection of the artists records.

### Genre Model

The Genre model acts as a secondary category for records to be found by - this allows users to browse records by genre. Consisting of some
basic fields, such as name, slug, color and description, color is mostly used to populate the "genre badges" that feature on the record detail pages. 
Description is a part of the model which isn't presently being used, but the existence of the field allows for further expansion of genre related search later on.

As with the artist model, slugs are automatically generated.

### Record Model

The record model is the real backbone and purpose of the site - this contains information about the records, such as the title, slug, artist and genres, release year, size, rpm,
a description of the record, when the record was added to the site, price, quantity and whether the record is viewable by the public. It contains foreignkeys that correlate to the artist and genre models.

Slug generation is also automatic, and to simplify images for album covers, there's a function to get the front cover from the RecordImage model. A function also exists to call the average rating from the records reviews, if the record has any.

### RecordImage Model

As a supplementary to the Record Model, to allow for records to have multiple images, a RecordImage model was implemented. Each instance contains a record foreignkey, image url from cloudinary, as well as the image type - robust image type formatting was initially planned, but due to the tedium of obtaining record images and ordering them, most images are now categorised as 'Front Cover' or 'Other'.

### Review Model

The review model is the core of user interactivity with the records that they purchase. Containing information on the author, record, ratings for various aspects of the services offered by the site, store feedback, and review text, it acts as a hub model for users giving feedback on both the records and the service they've received from the site.

Record ratings are rendered into FontAwesome star icons to allow for reviews on the record page to have a pleasing visual style.

## Community App

### UserProfile Model

Allowing users to add their personal information to their profile makes for a smoother checkout process. Containing information that relates to the user model, the user's name, contact phone number, and contact email, this also allows the user to specify a different email or phone number on an order than the email address that's related to their account.

If the user's account email is the only email on the account, it is the one used when the profile is created. The UserProfile and DeliveryAddress models have a close relationship with the Order model, and are often used to pre-populate fields in the checkout process for authenticated users.

### DeliveryAddress Model

Seperating delivery addresses out from the User Profile allows the user to have multiple delivery addresses. Containing a label for easy identification, as well as the standard expected delivery fields, these delivery addresses are selectable in the checkout process by authenticated users.

### SupportTicket Model

This is the primary model for creating support tickets. I decided to use a UUID identifier to obscurify support tickets - this allows for anonymous users to access their support tickets if they decide to not log in while also making sure random people can't access them directly (as opposed to having support tickets with a url of support/ticket/1, support/ticket/2, etc.). Support tickets have an associated user, which also allows for authenticated users to see their support tickets on their profile page.

### NewsletterSubscriber Model

Users are also able to subscribe to the newsletter with a limited subscriber model, which can take an existing user, a name, and an email. This model is very rudimentary, but can be expanded upon to include user preferences for contact. I've touched on newsletter implementation in the future improvements section below.

## Checkout App

### Order Model

Orders are the backbone of the e-commerce aspect of the site, and contain information relating to the user's contact details, delivery address, order costs, and order contents via the OrderItem Model below. There is a custom update_total method as part of the order which automatically updates when a line item is added.

### OrderItem Model

This model is a supplementary model to the Order model; it keeps track of the record being purchased, the quantity of records, and how much the total cost is. This allows for a permanent record of the pricing of a purchase, which is important when record prices can change.

# Testing, Bugs & Code Validation

For details of automated and manual tests, bugs, and code validation, please see the [TESTING.MD](/TESTING.md) document.

# Changes, and Considerations whilst the project was underway

Limitations arose out of the sourcing of the record information; while Discogs API was useful in obtaining vast quantities of record information which would have taken a considerable amount of time to collect manually, this also meant that the related models were limited to information that related to Discogs formatting of that information; for example, while there is options to change RPM and Size in a lot of models, most records on Discogs do not list this information in a readily available format. As a result, most records collected via the Discogs API have the same RPM. 

Pricing and Size also faced a similar conundrum; in future implemetations of the project, I would recommend developing an understanding of the database inventory system that is beign used to populate the records before developing models.


# Potential Future Improvements

## Internationalization

At present, the site is very UK-Centric; it only takes UK phone numbers and only provides prices in GBP. A future improvement would be to expand on the delivery address system to allow for countries that are not the UK, pricing that is internationalized, etc.

## Newsletter Implementation

As of writing, there is a way to subscribe to the newsletter via the site, but no actual implementation of a newsletter. Further implementation could involve actually sending out monthly newsletters with discount codes, concert ticket giveaways, etc.

## Record Discovery

At the moment record discovery is very rudimentary, due to the limited number of records on the site. With the addition of more records, it would also be possible to add better record discovery,
including discovery based on user tastes, past orders, etc.


# Deployment

## Deployment to Heroku

The project was deployed to Heroku soon after being started. The steps to deploy are as follows:

1. For or clone this repository directly on GitHub, or using your IDE terminal with the following code:
    - `git clone https://github.com/Morgana-S/vinyl-online.git`
2. Create a new application on Heroku:
    - This requires singing up for a Heroku account, which you can do [here.](https://signup.heroku.com/login)
    - Once your account has been created, and you are on the user dashboard, you will need to create a new app and give it a name.
    - In the settings tab, ensure the correct config vars are in place. In this project, you will need to define to following vars:
        - `SECRET_KEY` - This will be your secret key for Django.
        - `DATABASE_URL` - The url for your database. This project uses a remote postgresql database.
        - `CLOUDINARY_URL` - The url for your cloudinary account.
        - `DISCOGS_USER_TOKEN` - The user token for your discogs account. This is needed to access the commands in the records app.
        - `DEFAULT_ARTIST_IMAGE` - Sets the default image used in your cloudinary account for new artists.
        - `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` - The email host for the project to send emails.
        - `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` - Your API keys and webhook endpoint secret for Stripe.
    - In the Deploy Tab, ensure the Heroku Application is linked to your cloned version of this GitHub repo.
    - Ensure that your Procfile contains only the following code:
        - `web: gunicorn vinyl_online.wsgi:application`
        - The Procfile has been included with this project, but please ensure that Heroku recognizes this Procfile if your version of the project fails to deploy.
    - Ensure that the `requirements.txt` file is included also, to ensure the deployment pulls all required libraries.
    - Click Deploy Branch, or Enable Automatic Deployment.

## Local Deployment

The project can also be deployed locally. To do so, please follow these instructions:

1. For or clone this repository directly on GitHub, or using your IDE terminal with the following code:
    - `git clone https://github.com/Morgana-S/vinyl-online.git`

2. Create a virtual environment (optional, but recommended):
    - On Windows, the command for this is `python -m venv .venv`
    - On Linux/macOS, (assuming you have Python 3 and Pip installed via package manager) - `python3 -m venv .venv`

3. Activate the virtual environment:
    - On Windows: `.venv\scripts\activate`
    - On Linux/macOS: `source .venv/bin/activate`

4. Install Dependencies - Navigate to the project directory and install dependencies found in `requirements.txt`
    - Navigating out of the venv folder: `cd ..`
    - Navigation from your root directory: `cd <insert filepath here>/vinyl-online`
    - Installing dependencies: `pip install -r requirements.txt`

5. Creating your env.py file:
    - Create a file named env.py in your root directory for the project.
    - Add this to your .gitignore file to ensure your variables are kept secret.
    - Ensure the file imports the os library using the `import os`line at the top, and define variables for your:
        - `SECRET_KEY` - This will be your secret key for Django.
        - `DATABASE_URL` - The url for your database. This project uses a remote postgresql database.
        - `CLOUDINARY_URL` - The url for your cloudinary account.
        - `DISCOGS_USER_TOKEN` - The user token for your discogs account. This is needed to access the commands in the records app.
        - `DEFAULT_ARTIST_IMAGE` - Sets the default image used in your cloudinary account for new artists.
        - `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` - The email host for the project to send emails.
        - `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` - Your API keys and webhook endpoint secret for Stripe.
    - Each of the above variables can be defined by using the `os.environ.setdefault()`method. For example:
        - `os.environ.setdefault('DATABASE_URL', '<insert database url here>')`
        - If you are using Google Mail as your email host provider, you will need to sign in to your account with an app password. Information on how to do this can be found [here.](https://support.google.com/accounts/answer/185833?hl=en)

6. Run the Application:
    - To run the project with your machine as a host, you can then type the following into your terminal:
        - Windows: `python manage.py runserver`
        - Linux/macOS: `python3 manage.py runserver`
    - You will then be able to view the website by clicking the link to the address in the terminal or typing the following into your browser's URL address bar:
        - `http://127.0.0.1:8000`

# Credits & Technology

## Tools

- [RealFaviconGenerator](https://realfavicongenerator.net/) - Resizing images for use in the site favicon.

- [Cloudinary](https://cloudinary.com/) - Cloud based asset hosting for record/artist images.

- [VS Code](https://code.visualstudio.com/) - My IDE for the project.

- [Python](https://www.python.org/) - Main language utilised in application settings and backend development.

- [HTML5](https://developer.mozilla.org/en-US/docs/Glossary/HTML5) - Basic HTML page structure, enhanced with Django Template Language

- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - Custom page styling, when required outside of the classes provided by Bootstrap

- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Interactive functionality for pages, when required outside of the classes provided by Bootstrap

- [Heroku](https://www.heroku.com/) - Project deployment and site hosting

- [Git](https://git-scm.com/) - Version control system

- [GitHub](https://github.com/) - Project Repo hosting

- [Stripe](https://stripe.com/gb) - Payment processing

- [Licecap](https://www.cockos.com/licecap/) - Screen recording software for GIFs for feature images.

## Frameworks

- [Django](https://www.djangoproject.com/) - Python-based web framework that allows fast deployment of web applications.

- [Bootstrap](https://getbootstrap.com/) - JavaScript and CSS Framework that provides versatile classes for use in styling a website and providing interactivity.

## Libraries

### Third Party

- [django-allauth](https://docs.allauth.org/en/latest/) - Integrated authentication applications that assist with registration and management of user accounts.

- [dj-database-url](https://pypi.org/project/dj-database-url/) - Django utility for interfacing with databases.

- [cloudinary](https://pypi.org/project/cloudinary/) - Python/Cloudinary integration

- [django-colorfield](https://pypi.org/project/django-colorfield/) - Color field for models in django projects

- [django-summernote](https://pypi.org/project/django-summernote/) - Django-integrated text editor for django text fields

- [whitenoise](https://whitenoise.readthedocs.io/en/stable/django.html) - Allows deployment of static files to django projects when hosted on heroku via WSGI.

- [gunicorn](https://gunicorn.org/) - Python WSGI HTTP server for hosting on Heroku.

- [psycopg2](https://pypi.org/project/psycopg2/) - PostgreSQL adapter for use with Python

- [coverage.py](https://coverage.readthedocs.io/en/7.10.6/) - Test Execution Report Provider

- [django-phonenumber-field](https://django-phonenumber-field.readthedocs.io/en/latest/) - Library that interfaces with python-phonenumbers to validate and convert phone numbers.

- [stripe](https://pypi.org/project/stripe/) - Python library for Stripe's API

### Python

- [Decimal](https://docs.python.org/3/library/decimal.html) - Decimal module to fix floating point errors with floats

- [Pathlib](https://docs.python.org/3/library/pathlib.html) - Object-oriented filesystem paths

- [os](https://docs.python.org/3/library/os.html#module-os) - Misc Operating System interfaces

- [sys](https://docs.python.org/3/library/sys.html#module-sys) - System specific parameters and functions

- [unittest](https://docs.python.org/3/library/unittest.html) Library for performing unit testing.

- [json](https://docs.python.org/3/library/json.html) - JSON encoding and decoding

### Django

- [Django.contrib.admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/) - Django Admin Site

- [Django.urls path, include](https://docs.djangoproject.com/en/5.2/ref/urls/) - Django url functions for url routing

- [Django.views.generic RedirectView](https://docs.djangoproject.com/en/5.2/ref/class-based-views/base/#redirectview) - View for redirecting links to sitemap and robots.txt

- [Django.contrib.auth](https://docs.djangoproject.com/en/5.2/ref/contrib/auth/) - Base user model for authentication

- [Django.core.validators](https://docs.djangoproject.com/en/5.2/ref/validators/) Min/Max length validators, value validators

- [Django.db](https://docs.djangoproject.com/en/5.2/ref/databases/) - Models for db, views

- [Django.utils.safestring](https://docs.djangoproject.com/en/5.2/howto/custom-template-tags/#filters-and-auto-escaping) - String escapement

- [Django.utils.text slugify](https://docs.djangoproject.com/en/5.2/ref/utils/#django.utils.text.slugify) - Automatic slug generation for models

- [Django forms](https://docs.djangoproject.com/en/5.2/topics/forms/) - Form functionality for django projects

- [Django.contrib.auth.decorators](https://docs.djangoproject.com/en/4.2/_modules/django/contrib/auth/decorators/) - Decorations for @login_required

- [Django Messages](https://docs.djangoproject.com/en/5.2/ref/contrib/messages/) - Notification messages when an action has been completed e.g logout or login

- [Django shortcuts](https://docs.djangoproject.com/en/5.2/topics/http/shortcuts/) - Shortcuts for rendering templates, redirects, get_object_or_404s, etc.

- [Django Mail](https://docs.djangoproject.com/en/5.2/topics/email/) - Functionality for sending emails.

- [Django.urls reverse](https://docs.djangoproject.com/en/5.2/ref/urlresolvers/#reverse) - Creates absolute paths for a given view.

- [Django.template.loader render_to_string](https://docs.djangoproject.com/fr/4.2/topics/templates/#django.template.loader.render_to_string) - Renders a template to a string allowing generation of html content.

- [Django.utils.html strip_tags](https://docs.djangoproject.com/en/5.2/ref/utils/) - Strips tags from templates for plaintext emails

- [Django JSONResponse](https://docs.djangoproject.com/en/5.2/ref/request-response/#jsonresponse-objects) - Returns a response object as JSON, used for async views


## Visual Assets

- [SVG Repo](https://www.svgrepo.com/) - Record image used in website logo
- [Unsplash](https://unsplash.com/) - Stock photos used to illustrate personas in wireframes
- [FontAwesome](https://fontawesome.com/) - Icons for buttons
- [Discogs](https://www.discogs.com/) - Album and Vinyl art

## Content

- [Discogs](https://www.discogs.com/) - without Discogs and their [API](https://www.discogs.com/developers), obtaining the sheer amount of information about vinyl records present on this site would have been a much more arduous task. I have used Discogs API to simulate "warehouse stock" databases in this case; pulling from information from their API to simulate the inventory an e-commerce site would have.

- [Termsfeed Privacy Policy Generator](https://www.termsfeed.com/privacy-policy-generator/) - Privacy Policy generation.

- [xml-sitemaps.com](https://www.xml-sitemaps.com/) - Sitemap.xml generation.

## Special Thanks
- Thanks to [Code Institute](https://codeinstitute.net/) for tutorials and guidance in the development of this project.
