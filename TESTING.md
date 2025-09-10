# Testing and Code Validation

## General Approach

During the writing of functions and models, a red-green-refactor approach was taken to ensure that functions and models were suitable for use. After the website was made feature-complete for now, automated testing began of both JavaScript files and Django Views, Models, and Forms. Below I have documented my approach to each test.

## Automated Testing

### Jest and JavaScript/jQuery Testing

Jest was used to test each JavaScript and jQuery function utilised throughout the site. These tests remain in the source code for greater detail, but the results of each page can be found here.

![base.js Testing](/documentation/images/automated-testing/base-js-testing.png)

![artist_detail.js Testing](/documentation/images/automated-testing/artist-detail-js-testing.png)

![checkout.js Testing](/documentation/images/automated-testing/checkout-js-testing.png)

![record_detail.js Testing](/documentation/images/automated-testing/record-detail-js-testing.png)

![user_profile.js Testing](/documentation/images/automated-testing/user-profile-js-testing.png)

![view_basket.js Testing](/documentation/images/automated-testing/view-basket-js-testing.png)

### Django Testing

Automated testing of Django components was done using the in-built django testing library,
unittest. While testing, an sqlite test database was created and used to create mock data for tests. This allowed me to focus on the behaviour of the tested components without worrying about creating or destroying data in my production database.

I used the coverage.py library to provide a detailed coverage report for each app, a summary of which can be seen below.

![coverage.py Report](/documentation/images/automated-testing/coverage-report.png)

## Manual Testing

All testing was carried out on the latest deployed version of the project on Heroku. The following tests were carried out:

### Browser Compatability

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Browser - Basic Functionality | Website was opened with Microsoft Edge, Google Chrome, and Mozilla Firefox. Website functionality was tested with the tests below. | Website loads correctly on all browsers. | Working as intended. |
| Device - Basic Functionality | Website was opened using a desktop PC, Google Pixel 7 Mobile device, iPhone, and iPad. Website functionality was tested with the tests below. | Website loads correctly on all devices. | Working as intended. |

### Responsiveness Testing Images

For responsive image testing, please see the [RESPONSIVENESS.md](/RESPONSIVENESS.md) file.

### Navigation

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Unauthorised User Navigation Bar Use | Clicking all links on the navigation bar as an anonymous user. | All navigation links work and navigate to the correct page. | Working as intended.  |
| Authorised User Navigation Bar Use | Log the user in, and click all links on the navigation bar. | All navigation links work and navigate to the correct pages. | Working as intended. |
| Unauthorised User Link Navigation | Go through the pages available to anonymous users and click every button or link to ensure they navigate correctly. | All navigation links work and navigate to the correct locations. | Working as intended. |
| Authorised User Link Navigation | Log the user in, go through all pages accessible to the user and ensure they lead to the correct locations. | Working as intended | 
| Footer Links - Unauthorised Users | Clicking the links in the footer as a guest user take the user through to the appropriate pages. Contact Us, Terms and Conditions, Return Policy, Github Link, and Privacy Policy should also open in a new page.  | Working as intended. |
| Footer Links - Authorised users | Clicking the links in the footer a signed in user takes the user through to the appropriate pages. Contact Us, Terms and Conditions, Return Policy, Github Link, and Privacy Policy should also open in a new page.  | Working as intended. |
| Search - Async | Typing the name of a known artist, a known record, and a hidden record into the search bar at the top of the page. | The known artist, known record should appear in the search results. Clicking the known artist's result or a record should take you to the record/artist detail page. The hidden record should not appear. | Working as intended. |
| Search - View | Typing the name of a known artist, a known record, and a hidden record into the search bar at the top of the page, then pressing the search button. | The known artist, known record should appear in the search results. Clicking the result for the known artist/record should take the user to the appropriate detail page. The hidden record should not appear. | Working as intended. |
| Index Page - Links | Click each of the three carousel links, every record link and the featured "View New Releases" and "View All Pop" links on the index page. | All links take the user to the appropriate location. | Working as intended. |
| All Records - Links | Click all of the records on each of the all records pages. | Takes the user to the record detail page for that record. | Working as intended. |
| Latest Releases Links | Similar to the All Records test above, click all links on latest releases page. | Takes the user to the record detail page for that record. | Working as intended. |
| Browse by Genre - Links | Similar to above - click all records on a browse by genre page. | Takes the user to the record detail page for that record. | Working as intended. |
| Authorised User - Profile Navigation Links | Clicking on the change password, edit/create profile personal info, add/edit delivery addresses, an item in the order history, an item in the support tickets table, the view full order history, view all support tickets, and add new support ticket buttons. | All pages take the user to the intended location. | Working as intended. |



### User Authentication and Authorisation

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Signing up | Anonymous user navigates to the sign up page, provides account credentials, and clicks the sign up button. | User account is created, they receive an email that contains a link for them to click to verify their account. | Working as intended. |
| Logging In | Anonymous user navigates to the log in page and signs into account using details. | User logs in successfully, is informed they have signed in successfully, and are directed back to the index page. | Working as intended. |
| Logging Out | Authorised user navigates to the sign out page link in the navbar, confirms they wish to sign out. | User is signed out, informed of this, and directed to the index page. | Working as intended.
| Anonymous User - Accessing Profile Features | While signed out, the user attempts to access the profile page via the URL bar. The user also attempts to access creating/editing their profile, delivery addresses, viewing order history, or viewing support tickets. | User is directed to log in first. | Working as intended. |
| Anonymous User - Accessing Staff Features | While signed out, the user attempts to access the analytics, Add Record/Edit Record, Add Artist/Edit Artist, Delete Record/Artist functions. | User is directed to log in. | Working as intended. |
| Authorised User - Accessing Staff Features | While signed in as a non-staff user, the user attempts to access the analytics, Add/Edit record functions, Add/Edit Artist functions, Delete Record/Artist functions. | User is directed to the relevant page - often the artist/record detail or index page - and advised that section of the site is accessible only to members of staff. | Working as intended. |

### CRUD Functionality, Forms and Input

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Adding / Editing User Personal Info | As an authorised user, navigate to the profile page and click to add or edit personal info. The form is then filled out with personal info details. | Form updates with new user details. | Working as intended.
| Adding a Delivery address | As an authorised user, navigate to the profile page and click the add new address button. Fill out the address details and submit the form. | A new address appears on the profile page. | Working as intended.
| Adding a Delivery address - invalid form | As above, but leaving details such as the address line 1 and postcode, which are required fields, unfilled. | Form will not submit until required fields are filled. | Working as intended. |
| Editing a Delivery Address | As an authorised user, navigate to the profile page and click on an existing address's edit button. Fill out the new address details and submit the form. | The existing address has its details edited. | Working as intended. |
| Editing an address - invalid form | As above, but removing required details such as label, address line 1, and postcode. | Form will not submit until required fields are filled. | Working as intended.
| Deleting a Delivery address | As an authorised user, navigate to the profile page and click on an existing address's delete button. | A delete confirmation modal should appear, which when confirmed, deletes the address. | Working as intended. |
| Reviews as an unauthorised user - eligibility | As an unauthorised user, navigate to any record page and attempt to leave a review. | As unauthorised users are unable to leave reviews, they should not be able to see the button to leave a review. Attempting to navigate via url asks the user to log in. The user sees a message that incentivizes them to log in to leave a review. | Working as intended - however, no message currently present. Message has been added to reflect this - not a bug, just an overlooked feature. | 
| Reviews as an authorised user - eligibility | As an authorised user, navigate to any record page and attempt to leave a review - notably, without having a confirmed delivered copy of the record. | As with the unauthorised user, the user is not eligible to leave a review and should not be able to leave one. | Working as intended - logged in users are directed to the record detail page with the message about purchasing the record to provide a review. | 
| Reviews as an authorised user - IS eligible | As an authorised user, attempt to make a review for a record they are eligible to review. | Record review goes through - viewable only to user as has not been approved. | Working as intended. | 
| Eligible Review marked approved - visible to all users | The above review is marked as approved on the admin panel. | Review is now visible to all users. | Working as intended. |
| Deleting a review - anonymous user | Attempt to delete a review while not signed in by triggering the request via the URL bar. | Returned to the record detail page. | Working as intended. |
| Deleting a review - authorised user, not their review | As above, but as a signed in user. | Returned to the record detail page. | Working as intended. |
| Deleting a review - authorised user, is their review | As above, but as the author of the review. | Confirm deletion modal appears, when confirmed, review is deleted. | Working as intended. |
| Adding a record | As a staff user, go to add a record and fill out the form with correct details. | New record is created. | Working as intended. |
| Adding a record - invalid form | As a staff user, go to add a record that is missing details. | Form does not submit. | Working as intended. |
| Adding a record - no images | As above, but without adding images | Form does submit - images can be added after the fact. | Working as intended. |
| Adding a record - uploading images | As above, but add images when completing the form normally. | Images are present on the page, front cover image is designated properly. | Working as intended. |
| Editing a record | As a staff user, edit the details of an existing record using the form. | New changes are visible on the record. | Working as intended. |
| Editing a record - invalid form | As a staff user, edit the details of an existing record, removing details that are mandatory. | Form does not submit. | Working as intended. | 
| Editing a record - remove all images | As a staff user, complete the record form but delete existing images | Record images are deleted. | Working as intended. | 
| Editing a record - uploading images | As above, but add images when completing the form normally. | Images are present on the page, front cover image is designated properly. | Working as intended. |
| Deleting a record | As a staff user, try to delete a record using the button on the record detail page. | After the confirmation modal, the record is deleted. | Working as intended. |
| Adding an artist | As a staff user, go to add an artist and fill out the form with details. | New artist is created. | Working as intended. |
| Adding an artist - invalid form | As above, but leave out obligatory details, such as artist name. | Form will not submit. | Working as intended. |
| Adding an artist - no image | As above, but do not submit an image. Fill out remainder of required details. | Artist is submitted with default image. | Working as intended. |
| Editing an artist | Edit an artist's existing details using the form. | Artist details are changed. | Working as intended. |
| Editing an artist - invalid form | As above, but leaving the artist's name as blank. | Form does not submit. | Working as intended.
| Editing an artist - adding an image | As above, but form filled out correctly, submitting a new image | Artist's image changes | Working as intended. |
| Deleting an artist | As a staff user, click the delete button on the artist detail page. | After confirmation modal, artist is deleted, user is directed to index page. | Working as intended. |
| Signing up for newsletter - anonymous user | Go to the newsletter page and provide details to sign up. | Providing the newsletter sign up page with details creates a new newsletter subscriber, and a confirmation of this is sent if a real email is used. | Working as intended. |
|Signing up for a newsletter - authorised user | As above - go to newsletter page and sign up. | As above - if the user as personal info set in their profile, the newsletter automatically populates from this. | Working as intended. | 


### Checkout and E-Commerce Process

| Test | Method | Desired Results | Actual Results |
| --- | --- | --- | --- |
| Checkout flow - anonymous user | Test the general checkout flow - add an item to basket, go to view basket, go to checkout, input address and personal details, use test card number. | Checkout completes and user is taken to an order confirmation page. If a real email is used in the process, an email confirmation is sent. | Working as intended. |
| Checkout flow - authorised user | As above, but as a logged in user. New address details are used, rather than a saved address. | Checkout completes and user is taken to an order confirmation page. Order shows up in the user's order history. If a real email is used in the process, an email confirmation is sent. | Working as intended. |
| Async basket updates | Add an item to the basket from the record detail page. | The basket count badge updates without refreshing the page. | Working as intended. |
| Basket functionality - empty basket | Navigate to the empty basket | Basket is empty and a random array of 5 records are suggested to the user. | Working as intended. |
| Basket functionality - has items | As above, navigate to the basket with items in it. | Items are displayed in a table in the basket. Order total costs are shown below the table. | Working as intended. |
| Basket functionality - changing amounts to valid number | In the basket, adjust the number of records to a different number. | Page refreshes with updated totals and prices. | Working as intended. |
| Basket functionality - changing amounts to invalid number | In the basket, adjust the number of records to 99. | Basket item should refresh to contain a max of 9 of the record. |  Working as intended. | 
| Basket functionality - changing amounts to not a number | In the basket, adjust the number of records to 'two' | Basket item should refresh to contain 1 record. | Working as intended. |
| Basket functionality - removing a record | Click the "remove all" button next to a record row. | All instances of that record are removed from the basket. | Working as intended. | 
| Checkout - authorised user - prefilled details | As an authorised user, have an existing user profile with filled details, then attempt to navigate to the checkout with the intent to purchase a record. | The contact info is prepopulated based on the user's personal details. | Working as intended. |
| Checkout - authorised user - selecting a delivery address | As above, have at least one delivery address to select from, then, when navigating to checkout, select that delivery address. Complete the checkout with the intent for that address to be the delivery address. | Delivery address is correctly shown in the order. | Working as intended. |
| Checkout - authorised user - new address | As above, but select to fill out a new address. | Delivery address is correctly shown in the order. | Working as intended. |
| Checkout - authorised user - saving new address | As above, but check to save the new address on checkout completion. | New delivery address is saved on profile. | Working as intended. |
| Record Detail - selecting an invalid amount or string to add to basket | Change the quantity on a record detail page to an invalid number, such as 999, or 'two' | User is prompted to select a valid number between 1 - 9. | Working as intended. |

### Admin Functionality

| Test |  Desired Results | Actual Results |
| --- | --- | --- |
| Models | All models are registered and appear in the admin panel. | Working as intended. |
| Filter and Sorting | All models are able to be filtered and sorted by relevant fields. | Working as intended. |
| CRUD functionality | It is possible to create, read, update and delete instances of models from the admin panel. | Working as intended. | 
| Search functionality | It is possible to search the fields for each model by various factors, such as record title or artist. | Working as intended. |

## Peer Reviewed Testing

- The website was also tested by four different users on a variety of devices, from mobile phones to desktop PCs. Their feedback about the site can be found in the section below.
- I also asked one of the three users to carry out the tests found in the sections above, on three seperate devices; iphone, iPad, and desktop PC. The user reported functionality in line with my results, or, where I have made changes, they reported results that changes were working as intended.

## Feedback

- Users found the website simple to navigate, and were happy with functionality both as an anonymous user and authorised user. The ability to pre-save information for delivery and contact info was lauded as a desirable feature. Users were able to make accounts and log in without any issues.
- One of the users expressed that the site was very "dark" - as a result of the choice of a black background for the majority of the site. Given that the aesthetic is inspired by 'rock and roll' themes, this was intentional, but might not necessarily be a universal appeal and may be something to consider for future projects.
- Users expressed a desire for more variety in records on the site; as the website functions as a proof of concept and adding more record models is scalable, I consider this to be an easily fixed feature should a similar design be used in a true production environment.
- The representatives of each persona in the initial design process felt like their concerns were listened to and addressed - the audiophile, however, wishes that it were addressed in a slightly different way, with utilisation of more info per record as well as collapsible sections with further info. Lack of record information has been addressed in the future improvements section on the readme alongside the limitations of pulling info from the Discogs API.

## Bugs

- Stripe Payment Intents: When checking out, a second payment intent is created after the first one succeeds. This account seems to be for the same transaction and permanently awaits account details.
    - Cause: Unknown at present. I've tried examining my asynchronous code for awaiting for payment intents to succeed but it's nothing obvious there. Could possibly be related to how the view creates a new payment intent when the checkout page loads, which is done to ensure the payment intent matches with the order correctly.
    - Fix: None at present; as this does not actually affect the order itself, it's an annoying but relatively harmless bug.

- All Records Pagination: Paginator does not call pages correctly.
    - Cause: the page_number was calling the incorrectly named GET object ('page') instead of ('record_page')
    - Fix: Amended GET object, now works as intended.

- Creating New Records: Image formset was not saving correctly.
    - Cause: instead of calling the formset.instance, I was calling formset.record - minor typo
    - Fix: Now correctly call formset.instance - working as intended.

- Review Contexts: Anonymous users encountering a server error due to the is_reviewable and has_reviewed booleans.
    - Cause: Booleans were not being set for anonymous users.
    - Fix: Set is_reviewable and has_reviewed to false for anonymous users.

- Async Search: Singular instance of partial search results not showing in the results bar.
    - Cause: Unknown; unable to replicate. May have possibly been network issues on user side.
    - Fix: None for now.

- Clear Address Fields: During automated testing, the clear address fields function failed to run.
    - Cause: Renaming the ids for the fields were not updated in the function.
    - Fix: Fields updated in function.

- Async Search: No response returned if a query isn't provided.
    - Cause: return JsonResponse was in query block.
    - Fix: Move JsonResponse out of query block so it always returns something.


## Code Validation

For Code Validation Screenshots, please see [VALIDATION.md](/VALIDATION.MD).

## Lighthouse Reports

For Lighthouse Report Screenshots, please see [LIGHTHOUSE.md](/LIGHTHOUSE.md).