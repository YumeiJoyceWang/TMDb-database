## SQLite

Construct a TMDb database in SQLite. 

### Tasks

**a**. Create tables and import data
> i. Create two tables named movies and movie_cast with columns having the indicated data types:
- movies
  - id (integer)
  - title (text)
  - score (real)
- movie_cast
  - movie_id (integer)
  - cast_id (integer)
  - cast_name (text)
  - birthday (text)
  - popularity (real)

> ii.  Import the provided movies.csv file into the movies table and movie_cast.csv into the movie_cast table.

> iii. Vertical Database Partitioning. Create a new table cast_bio from the movie_cast table.
- cast_bio
  - cast_id (integer)
  - cast_name (text)
  - birthday (text)
  - popularity (real)

**b**.  Create indexes.
  - movie_index for the id column in movies table
  - cast_index for the cast_id column in movie_cast table
  - cast_bio_index for the cast_id column in cast_bio table

**c**. Calculate a proportion. Find the proportion of movies having both a score > 50 and the substring 'war' in the name.

**d**. Find the most prolific actors. List 5 cast members with the highest number of movie appearances that have a popularity > 10. Sort the results by the number of appearances in descending order, then by cast_name in alphabetical order.

**e**. Find the highest scoring movies with the smallest cast. List the 5 highest-scoring movies that have the fewest cast members. Sort the intermediate result by score in descending order, then by
number of cast members in ascending order, then by movie name in alphabetical order. 

**f**. Get high scoring actors. Find the top ten cast members who have the highest average movie scores.
  - Sort the output by average score in descending order, then by cast_name in alphabetical order.
  - First exclude movies with score <25 in the average score calculation.
  - Next exclude cast members who have appeared in two or fewer movies.

**g**. Creating views. Create a view called good_collaboration that lists pairs of actors who have had a good collaboration as defined here. Each row in the view describes one pair of actors who appeared in at least 3 movies together AND the average score of these movies is >= 40.
Find the best collaborators. Get the 5 cast members with the highest average scores from the good_collaboration view, and call this score the collaboration_score. This score is the average of the average_movie_score corresponding to each cast member, including actors in cast_member_id1 as well as cast_member_id2. 

**h**.  Import movie overview data from the movie_overview.csv into a new FTS table called movie_overview with the schema: 
- movie_overview
  - id (integer)
  - overview (text)

i. Count the number of movies whose overview field contains the word 'fight'. Matches are not case sensitive. Match full words, not word parts/sub-strings.
ii. Count the number of movies that contain the terms 'space' and 'program' in the overview field with no more than 5 intervening terms in between.