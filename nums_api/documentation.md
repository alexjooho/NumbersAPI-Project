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

If a valid keyword is provided, requests should return JSON:
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

If a valid keyword combination is provided, requests should return JSON:
```
http://numbersapi.com/api/dates/11

⇒ {
    "fact": {
        "number": 113
        "year":1970
        "fragment": "the day in 1970 that the first Earth Day is celebrated"
        "statement": "April 22nd is the day in 1970 that the first Earth Day is celebrated."
        "type": "dates"
        }
}
```

### Years
URL for Years fact about a number:

<code>http://numbersapi.com/api/years/<strong>year</strong></code>

<code><strong>year</code></strong> is
an integer for a year, or you can instead use
the keyword <code><strong>random</code></strong>, for which we will try to return a random available fact.

If a valid keyword is provided, requests should return JSON:
```
http://numbersapi.com/api/years/2011

⇒ {
    "fact": {
        "year": 2011
        "fragment": "the year that a magnitude 9 earthquake hit Japan"
        "statement": "2011 is the year that a magnitude 9 earthquake hit Japan."
        "type": "years"
        }
}
```

### Math
URL for Math fact about a number:

<code>http://numbersapi.com/api/math/<strong>number</strong></code>

<code><strong>number</code></strong> is
an integer for a number, or you can instead use
the keyword <code><strong>random</code></strong>, for which we will try to return a random available fact.

If a valid keyword is provided, requests should return JSON:
```
http://numbersapi.com/api/math/49

⇒ {
    "fact": {
        "number": 49
        "fragment": "the smallest number with the property that it and its neighbors are squareful"
        "statement": "49 is the smallest number with the property that it and its neighbors are squareful."
        "type": "math"
        }
}
```

## Table Schema

![db Table Schema](../nums_api/static/numbers-api-table-schema.png)
