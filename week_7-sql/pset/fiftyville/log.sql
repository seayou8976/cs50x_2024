-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get the schema of all the tables, copy/paste for reference later
.schema

-- Just to get a feel for what the table looks like
SELECT *
  FROM crime_scene_reports;

-- Narrow it down to find the transcript we need
SELECT *
  FROM crime_scene_reports
 WHERE year = 2023
   AND month = 7
   AND day = 28
   AND street = "Humphrey Street";

-- Find the three witness statements that mention the Bakery
SELECT *
  FROM interviews
 WHERE year = 2023
   AND month = 7
   AND day = 28
   AND transcript
  LIKE "%bakery%";

-- Check security logs from bakery between 10:15AM - 10:25AM
SELECT *
  FROM bakery_security_logs
 WHERE year = 2023
   AND month = 7
   AND day = 28
   AND hour = 10
   AND minute BETWEEN 15 AND 25;

-- Check ATM transaction logs
SELECT *
  FROM atm_transactions
 WHERE year = 2023
   AND month = 7
   AND day = 28
   AND atm_location
  LIKE "%Leggett%"
   AND transaction_type = "withdraw";

-- Find phone calls on 7/28/2023 less than 60 seconds
SELECT *
  FROM phone_calls
 WHERE year = 2023
   AND month = 7
   AND day = 28
   AND duration < 60;

-- First - find the destination city for earliest flight out of Fiftyville on 7/29/2023. That's the easiest
SELECT city
  FROM airports
 WHERE id IN
       (SELECT destination_airport_id
          FROM flights
         WHERE year = 2023
           AND month = 7
           AND day = 29
         ORDER BY hour, minute LIMIT 1);

-- Find the thief
SELECT name FROM people
 WHERE people.passport_number IN
       (SELECT passport_number
          FROM passengers
         WHERE flight_id = 36)
   AND people.phone_number IN
       (SELECT caller
          FROM phone_calls
         WHERE year = 2023
           AND month = 7
           AND day = 28
           AND duration < 60)
   AND people.license_plate IN
       (SELECT license_plate
          FROM bakery_security_logs
         WHERE year = 2023
           AND month = 7
           AND day = 28
           AND hour = 10
           AND minute BETWEEN 15 AND 25)
   AND people.id IN
       (SELECT person_id
          FROM bank_accounts
         WHERE account_number IN
               (SELECT account_number
                  FROM atm_transactions
                 WHERE year = 2023
                   AND month = 7
                   AND day = 28
                   AND atm_location
                  LIKE "%Leggett%"
                   AND transaction_type = "withdraw"));

-- Find the accomplice
SELECT name
  FROM people
 WHERE people.phone_number IN
       (SELECT receiver
          FROM phone_calls
         WHERE year = 2023
           AND month = 7
           AND day = 28
           AND duration < 60
           AND caller IN
               (SELECT phone_number
                  FROM people
                 WHERE name = "Bruce"));
