__Team Number:__ Team 4
__Team Name:__ Team Ralphie
__Weekly Team Meeting:__ Sunday at 6pm
__Planning Poker Results: Used scale 1-10
__Team Members in meeting:__ Nicole Sawtelle (Scrum Master), Kenji Ramcharansingh, Lucas Stackhouse, Nicholas Swisher
__Zoom Recording Link: https://youtu.be/W0FhYZ2-U9I

__User Stories__:
For a Moodle-type service:
As a user, I want to upload graphs & images so that I can share them with peers.
As an administrator, I want to introduce an anti-plagiarism tool.
As a user, I want data visualization on Moodle, so I have better understanding of my progress.
For an e-commerce service:
As a user, I want to compare the costs and reviews of products.
As a busy shopper, I want to check out just one item.
As an unsatisfied customer, I want to cancel my order.

__For a Moodle-type service:__
```
User Story Card
______________________________________________________________________________
As a 	: user
I want	: to upload graphs & images
So that : I can share them with peers.

Effort
Level	: 4

Acceptance Criteria
Given	: A signed-in user wants to upload graphs and images to Moodle to share with peers (ex: Piazza)
When 	: 	Going to a forum of peers AND creating a new post OR responding to an existing post
Then 	: 	New post is created with text box allowing user to include graphs/images OR user can comment on an existing post with text box allowing user to include graphs/images on the post
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As an	: administrator
I want	: to introduce an anti-plagiarism tool
So that : <reason for desired behavior / what you get from it> my students don't cheat

Effort
Level	: 7

Acceptance Criteria
Given	: 	An administrator is wanting to include a plagiarism checker on assignment submissions to discourage cheating
When 	: 	 When students upload a file/document to assignment submission page AND student 'submits' document
Then 	: 	Document is checked for plagiarism against existing websites (existing information on the web or additional student submissions stored in the database).
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: user
I want	: data visualization on Moodle
So that : I have better understanding of my progress

Effort
Level	: 4

Acceptance Criteria
Given	: 	 A signed-in user wants to have a visualization tool available on Moodle to monitor progress of the course
When 	: 	 A user accesses the homepage of Moodle
Then 	: 	 They are able to see a progress bar update with the tasks completed out of the actual assignments
When 	: 	 A signed-in user completes a task (quiz, homework assignment, test, etc)
Then 	: 	The data updates a counter on the homepage
____________________________________________________________________________

```

__For an e-commerce service:__

```
User Story Card
______________________________________________________________________________
As a 	: user
I want	: to compare the costs and reviews of products
So that : I can pick the highest quality, most cost effectice product

Effort
Level	: 5

Acceptance Criteria
Given	: 	A user has multiple products they are interested in and would like to easily compare the cost vs reviews of various products without having to switch between windows
When 	: 	 a user has selected products they are interested in
Then 	: 	they can select a 'compare view' screen to see the product displayed with the price, as well a handful of reviews. The user can also filter by 'helpful reivews' (which is selected by other purchasers).
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As a 	: busy shopper
I want	: to check out just one item
So that : I can continue browsing other media

Effort
Level	: 4

Acceptance Criteria
Given	: 	A customer has decided they want to make a purchase and only wants one item
When 	: 	A shopper has determined the sole product they want, a shopper can select a 'purchase now' button (as opposed to an 'add to cart')
Then 	: 	A shopper is redirected to a check-out page with the selected item and can immediately start entering their billing and shipping information.
____________________________________________________________________________

```

```
User Story Card
______________________________________________________________________________
As an	: unsatisfied customer
I want	: I want to cancel my order
So that : I no longer purchase from this company

Effort
Level	: 7

Acceptance Criteria
Given	: 	An unsatisfied customer has made a purchase and no longer wants the item from that company.
When 	: 	Navigating to purchase history OR from a purchase confirmation email AND 'cancel order' option has been selected (IF order has not yet shipped)
Then 	: 	the customer is redirected to a new page to confirm that they would like to cancel the order and an optional 'reason for cancelling order' text box is supplied to the customer.
When 	: 	IF order has already been shipped, it will not be possible to cancel order
Then 	: 	 the customer will have to wait for the item to be delivered to go through the returns process.
____________________________________________________________________________

```
