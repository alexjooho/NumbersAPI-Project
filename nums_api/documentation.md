# Numbers API V2 Documentation

## Requesting Data from Numbers API

### Base Url
Requests for all data types will start with the following URL:

```
http://numbersapi.com/api
```

<br>

### Data Types Available
Numbers API has four different types of fact data available to you:
* Trivia
* Dates
* Years
* Math

### Trivia
URL for Trivia fact about a number:

<code>http://numbersapi.com/api/trivia/<strong>number</strong></code>

<code><strong>number</code></strong> is
an integer, or you can instead use
the keyword <code><strong>random</code></strong>, for which we will try to return a random available fact.

If a valid keyword is provided requests should return JSON:
```
http://numbersapi.com/api/trivia/11

⇒ {
    "fact": {
        "number": 11
        "fragment": "is the possible age of the youngest elected pope, Benedict IX"
        "statement": "11 is the possible age of the youngest elected pope, Benedict IX."
        "type": "trivia"
        }
}
```

### Dates
URL for Dates fact about a number:

<code>http://numbersapi.com/api/dates/<strong>month/day</strong></code>

<code><strong>month and day</code></strong>will be
integers, or you can instead use
the keyword <code><strong>random</code></strong>, for which we will try to return a random available fact.

If a valid keyword combination is provided requests should return JSON:
```
http://numbersapi.com/api/dates/11

⇒ {
    "fact": {
        "number":113
        "year":1970
        "fragment": "the day in 1970 that the first Earth Day is celebrated"
        "statement": "April 22nd is the day in 1970 that the first Earth Day is celebrated."
        "type": "dates"
        }
}
```





Just hit http://numbersapi.com/number/type to get a plain text response, where

type is one of **trivia, math, date, or year**. Defaults to trivia if omitted.
number is
an integer, or
the keyword random, for which we will try to return a random available fact, or
a day of year in the form month/day (eg. 2/29, 1/09, 04/1), if type is date
ranges of numbers

## Query Parameter Options

### JSON

            http://numbersapi.com/1..3,10
```
⇒ {
    "1": "1 is the number of dimensions of a line.",
    "2": "2 is the number of polynucleotide strands in a DNA double helix.",
    "3": "3 is the number of sets needed to be won to win the whole match in volleyball.",
    "10": "10 is the highest score possible in Olympics gymnastics competitions."
}
```

## Table Schema

![db Table Schema](../nums_api/static/numbers-api-table-schema.png)
