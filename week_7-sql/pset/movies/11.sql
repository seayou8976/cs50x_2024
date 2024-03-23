SELECT title
  FROM movies
  JOIN stars
    ON movies.id = stars.movie_id
  JOIN ratings
    ON movies.id = ratings.movie_id
 WHERE stars.person_id IN
       (SELECT id
          FROM people
         WHERE name = 'Chadwick Boseman')
 ORDER BY ratings.rating DESC LIMIT 5;
