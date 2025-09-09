# Testing and Code Validation

## General Approach

During the writing of functions and models, a red-green-refactor approach was taken to ensure that functions and models were suitable for use. After the website was made feature-complete for now, automated testing began of both JavaScript files and Django Views, Models, and Forms. Below I have documented my approach to each test.

## Automated Testing

### Jest and JavaScript/jQuery Testing

Jest was used to test each JavaScript and jQuery function utilised throughout the site. These tests remain in the source code for greater detail, but the results of each page can be found here.
![base.js Testing](/documentation/images/automated-testing/base-js-testing.png)
![artist_detail.js Testing](/documentation/images/automated-testing/artist-detail-js-testing.png)
![checkout.js Testing](/documentation/images/automated-testing/checkout-js-testing.png)

## Manual Testing

## Peer Reviewed Testing

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


## Code Validation