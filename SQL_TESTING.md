# Overview
This document outlines the database design and test strategy using for a MongoDB based sentiment analysis application that collects and processes media data (Youtube, Reddit, and IGDB). It includes the structure of each collection, data access functions, and frontend test coverage to ensure database interactions are functional. Given that this is based in MongoDB the schema is flexible and these are expectations rather than constraints as constraints are not not enforced. The same goes for dependancies, collections in MongoDB do not have relationships   
---

## Collection: `youtube_comments`
**Description**
Stores sentiment-analyzed comments from YouTube videos. 

**Fields:**
| Name           | Type               | Desc                                                | Expectations ("Constraints")                     |
|----------------|--------------------|-----------------------------------------------------|--------------------------------------------------|
| `_id`          | `ObjectID`         | `Gives each document a unique identifier`           | `Auto generated ObjectID`                        | 
| `Video_id`     | `String`           | `Youtube identifying string for each video`         | `Expected`                                       |
| `Comment`      | `String`           | `Text content of the YouTube comment`               | `Expected`                                       |
| `sentiment`    | `String`           | `Sentiment result`                                  | `(Positive / Negative)`                          | 
| `timestamp`    | `ISODate`          | `Date and time of comment`                          | `Should be valid ISO Date`                       |

**Tests:**

`insert`:  Insert a comment and verify all fields are correctly stored. 

`read`: Fetch by video_id and validate the retrieved data and validate contents.

## Collection `reddit_posts`
**Description**
Stores sentiment-analyzed Reddit posts/comments 

**Fields**
| Name           | Type               | Desc                                                | Expectations ("Constraints")                     |
|----------------|--------------------|-----------------------------------------------------|--------------------------------------------------|
| `_id`          | `ObjectID`         | `Gives each document a unique identifier`           | `Auto generated ObjectID`                        | 
| `post_id`      | `String`           | `ID of associated reddit post/comment`              | `Expected`                                       |
| `content`      | `String`           | `Text of post or comment`                           | `Expected`                                       |
| `sentiment`    | `String`           | `Sentiment result`                                  | `(Positive / Negative)`                          | 
| `timestamp`    | `ISODate`          | `Date and time of comment`                          | `Should be valid ISO Date`                       |

**Tests:** 

`insert`: Insert reddit data and ensure proper structure.

`read`: Query by post_id and verify content/sentiment. Check timestamp format and value correctness. 

## Collection `igdb_data`
**Description**
Stores information collected from igdb regarding games 

**Fields**
| Name                | Type               | Desc                                                | Expectations ("Constraints")                     |
|---------------------|--------------------|-----------------------------------------------------|--------------------------------------------------|
| `_id`               | `ObjectID`         | `Gives each document a unique identifier`           | `Auto generated ObjectID`                        | 
| `id`                | `Int`              | `ID used on igdb to identify games`                 | `Expected`                                       |
| `cover`             | `Object`           | `Object containing an Int id and an image url`      | `Expected`                                       |
| `first_release_date`| `ISODate`          | `ISO Date of games first release`                   | `Expected valid ISODate`                         | 
| `genres`            | `Array`            | `Array of objects containing genre id and desc`     | `Expected >= 1`                                  |
| `companies`         | `Array`            | `Array of objects containing company info`          | `Expected >= 1`                                  |
| `name`              | `String`           | `Name of Game`                                      | `Expected`                                       |
| `platforms`         | `Array`            | `Array of objects containing platform info`         | `Expected >= 1`                                  |
| `summary`           | `String`           | `Summary of the game`                               | `Expected`                                       |
| `updated_at`        | `ISODate`          | `ISO Date of entry update`                          | `Expected valid ISODate`                         | 
| `websites`          | `Array`            | Array og objects containing associated sites`       | `Expected >=1`                                   |

**Tests:**

`insert`: Insert igdb data and ensure proper fields are occupied with corrosponding data.

`read`: Query by name and verify all data is accessable and valid (most will be displayed on the games page) 

## Data Access Methods
**Add_youtube_comment(video_id, comment, sentiment, timestamp)**

`Description:` adds a new comment to the youtube_comments collection 

`Parameters:` video_id – string, comment – string, sentiment – string, timestamp – date/time 

`Returns:` insterted_id 

**Tests:**
| Desc                              | Requirements                           | Structure                                                                                                                 | Actual Result                       | Test Result             |
|-----------------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------|
| `insert empty params (4)`         | `Youtube api keys/Mongo login keys`    | - Connect to youtube api<br>- Get comment from generator<br>- Connect to Mongo node<br>- Insert with one field empty      | `Should throw Error`                | `Pass/Fail`             | 
| `insert with invalid types (4)`   | `Youtube api keys/Mongo login keys`    | - Connect to youtube api<br>- Get comment from generator<br>- Connect to Mongo node<br>- Insert with one field invalid    | `Should throw Error`                | `Pass/Fail`             | 
| `insert with valid params`        | `Youtube api keys/Mongo login keys`    | - Connect to youtube api<br>- Get comment from generator<br>- Connect to Mongo node<br>- Insert with all fields filled    | `Should return an inserted id`      | `Pass/Fail`             | 

**Add_reddit_post(post_id, connect, sentiment, timestamp)**

`Description:` Adds a new reddit post/comment

`Parameters:` post_id – string, content – string, sentiment – string, timestamp – data/time 

`Returns:` inserted_id 

**Tests:**
| Desc                              | Requirements                           | Structure                                                                                                                 | Actual Result                       | Test Result             |
|-----------------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------|
| `insert empty params (4)`         | `Reddit api keys/Mongo login keys`     | - Connect to reddit api<br>- Get comment from generator<br>- Connect to Mongo node<br>- Insert with one field empty       | `Should throw Error`                | `Pass/Fail`             | 
| `insert with invalid types (4)`   | `Reddit api keys/Mongo login keys`     | - Connect to reddit api<br>- Get comment from generator<br>- Connect to Mongo node<br>- Insert with one field invalid     | `Should throw Error`                | `Pass/Fail`             | 
| `insert with valid params`        | `Reddit api keys/Mongo login keys`     | - Connect to reddit api<br>- Get comment from generator<br>- Connect to Mongo node<br>- Insert with all fields filled     | `Should return an inserted id`      | `Pass/Fail`             | 

**add_game(game_name)**

`Description:` Queries igdb and creates a document in igdb_data containg game data

`Parameters:` game_name - String

`Returns:` inserted_id

**Tests:**
| Desc                              | Requirements                           | Structure                                                                                                                 | Actual Result                       | Test Result             |
|-----------------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------|
| `insert empty param`              | `igdb api keys/Mongo login keys`       | - Connect to igdb api<br>- Get query data from igdb<br>- Connect to Mongo node<br>- Insert with one of each field empty   | `Should throw Error`                | `Pass/Fail`             | 
| `insert with invalid type`        | `igdb api keys/Mongo login keys`       | - Connect to igdb api<br>- Get query data from igdb<br>- Connect to Mongo node<br>- Insert with one of each field invalid | `Should throw Error`                | `Pass/Fail`             | 
| `insert with valid params`       | `igdb api keys/Mongo login keys`        | - Connect to igdb api<br>- Get query data form igdb<br>- Connect to Mongo node<br>- Insert with all fields valid          | `Should return an inserted id`      | `Pass/Fail`             | 





