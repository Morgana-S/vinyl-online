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

## Adding Records

## Django Custom Commands for Adding Records using the Discogs API

## Form Verification

## Editing Records

## Deleting Records

## Artist Details

## Adding Artists

## Editing Artists

## Deleting Artists

## Shopping Basket

## Checkout

## Record Analytics

## Order Confirmation

## Account Registration and Login
![Account Registration](/documentation/images/feature-images/account-registration.gif)
Users are able to register accounts on the website using django all-auth. Users are then required to verify their email address as part of the account creation process.
Django Allauth's default templates have been replaced with custom ones that match the site's design.

## Account Profile

## Editing Profile Details

## Adding Delivery Addresses

## Viewing Order History

## Contacting Support

## Viewing Support Tickets

## Account Logout
![Account Logout](/documentation/images/feature-images/logout.gif)

Users can also sign out of their account at any time, allowing for them to navigate the site using public devices.

## Privacy Policy

## Newsletter Signup

## Robots.txt

## Sitemap.xml

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

# Testing, Bugs & Code Validation

For details of automated and manual tests, bugs, and code validation, please see the [TESTING.MD](/TESTING.md) document.

# Changes, and Considerations whilst the project was underway

# Potential Future Improvements

## Internationalization

At present, the site is very UK-Centric; it only takes UK phone numbers and only provides prices in GBP. A future improvement would be to expand on the delivery address system to allow for countries that are not the UK, pricing that is internationalized, etc.

## Newsletter Implementation

As of writing, there is a way to subscribe to the newsletter via the site, but no actual implementation of a newsletter. Further implementation could involve actually sending out monthly newsletters with discount codes, concert ticket giveaways, etc.


# Deployment

# Credits & Technology

## Tools

## Frameworks

- [Django](https://www.djangoproject.com/) - Python-based web framework that allows fast deployment of web applications.

- [Bootstrap](https://getbootstrap.com/) - JavaScript and CSS Framework that provides versatile classes for use in styling a website and providing interactivity.

## Libraries

### Third Party

### Python

### Django

### Summernote

### Cloudinary

### DjangoPhoneNumber

## Visual Assets

- [SVG Repo](https://www.svgrepo.com/) - Record image used in website logo
- [Unsplash](https://unsplash.com/) - Stock photos used to illustrate personas in wireframes
- [Discogs](https://www.discogs.com/) - Album and Vinyl art

## Content

- [Discogs](https://www.discogs.com/) - without Discogs and their [API](https://www.discogs.com/developers), obtaining the sheer amount of information about vinyl records present on this site would have been a much more arduous task. I have used Discogs API to simulate "warehouse stock" databases in this case; pulling from information from their API to simulate the inventory an e-commerce site would have.

## Special Thanks
- Thanks to [Code Institute](https://codeinstitute.net/) for tutorials and guidance in the development of this project.
