# Numbers API V2 Documentation

## URL Structure

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
