# Tests
#### TODO
`jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec`
`sun|mon|tue|wed|thu|fri|sat`
## Table of contents
* [Keyword: 'every'](#keyword-every)
   * [Test: day[s]](#test-days)
      * [Expression](#expression)
      * [Test case](#test-case)
   * [Test: hour[s]](#test-hours)
      * [Expression](#expression-1)
      * [Test case](#test-case-1)
   * [Test: hr[s]](#test-hrs)
      * [Expression](#expression-2)
      * [Test case](#test-case-2)
   * [Test: minute[s]](#test-minutes)
      * [Expression](#expression-3)
      * [Test case](#test-case-3)
   * [Test: second[s]](#test-seconds)
      * [Expression](#expression-4)
      * [Test case](#test-case-4)
* [Keyword 'in'](#keyword-in)
   * [Test: day[s]](#test-days-1)
      * [Expression](#expression-5)
      * [Test case](#test-case-5)
   * [Test: hour[s]](#test-hours-1)
      * [Expression](#expression-6)
      * [Test case](#test-case-6)
   * [Test: hr[s]](#test-hrs-1)
      * [Expression](#expression-7)
      * [Test case](#test-case-7)
   * [Test: minute[s]](#test-minutes-1)
      * [Expression](#expression-8)
      * [Test case](#test-case-8)
   * [Test: second[s]](#test-seconds-1)
      * [Expression](#expression-9)
      * [Test case](#test-case-9)
## Keyword: 'every'
All tests pass: https://regex101.com/r/kfPCGu/3
### Test: day[s]
#### Expression
`.*every\s(\d+)\sdays*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\sdays*`
#### Test case
<pre>
case: every ... in ...
should: match '5' and '15'
every 5 days 3 hours 15 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 3 hours 15 days 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 5 days in 6 hours 2 days
every 15 days in 10 days

case: in ... every ...
should: match '5' and '15'
in 10 days 6 hours 30 minutes 23 seconds every 5 days 30 minutes 13 seconds starting at 12:00
in 10 days 6 hours 30 minutes 23 seconds every 3 hours 15 days 30 minutes 13 seconds starting at 12:00
in 6 hours 2 days every 3 hours 5 days
in 10 days every 15 days

case: at ... in ... every ...
should: match '5' and '15'
at 12:00 in 10 days 6 hours 30 minutes 23 seconds every 5 days 3 hours 30 minutes 13 seconds
at 12:00 in 10 days 6 hours 30 minutes 23 seconds every 15 days 3 hours 30 minutes 13 seconds
at 12:00 in 10 days every 5 days
at 12:00 in 20 hours 10 days every 1 hour 15 days

case: at ... every ... in ...
should: match '5' and '15'
at 12:00 every 3 hours 5 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 3 hours 15 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 5 days 3 hours 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds
at 12:00 every 15 days 3 hours 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'every' keyword is not supplied a 'days' value
every 3 hours in 10 days
every 3 hours 30 minutes 13 seconds in 10 days
every 3 hours 30 minutes 13 seconds in 3 hours 30 minutes 3 days

case: in ... every ...
should: not match because the 'every' keyword is not supplied a 'days' value
in 10 days 30 minutes every 3 hours 45 minutes
in 6 hours 30 days 2 minutes every 12 hours
in 3 hours 30 minutes 13 seconds every 3 hours 30 minutes 13 seconds
</pre>
### Test: hour[s]
#### Expression
`.*every\s(\d+)\shours*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\shours*`
#### Test case
<pre>
case: every ... in ...
should: match '5' and '15'
every 5 days 5 hours 15 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 15 hours 15 days 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 5 days 5 hours in 6 hours 2 days
every 15 days 15 hours in 10 days 12 hours 30 seconds

case: in ... every ...
should: match '5' and '15'
in 10 days 6 hours 30 minutes 23 seconds every 5 days 30 minutes 15 hours 13 seconds starting at 12:00
in 10 days 6 hours 30 minutes 23 seconds every 5 hours 15 days 30 minutes 13 seconds starting at 12:00
in 6 hours 2 days every 15 hours 5 days
in 10 days every 15 days 5 hours

case: at ... in ... every ...
should: match '5' and '15'
at 12:00 in 10 days 6 hours 30 minutes 23 seconds every 5 days 5 hours 30 minutes 13 seconds
at 12:00 in 10 days 6 hours 30 minutes 23 seconds every 15 days 15 hours 30 minutes 13 seconds
at 12:00 in 10 days every 5 hours 15 days 3 hrs 5 minutes
at 12:00 in 20 hours 10 days every 15 hours 15 days

case: at ... every ... in ...
should: match '5' and '15'
at 12:00 every 5 hours 5 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 15 hours 15 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 5 days 15 hours 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds
at 12:00 every 15 days 15 hours 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'every' keyword is not supplied an 'hours' value
every 3 days 15 minutes in 10 days 15 hours
every 3 hrs 30 minutes 13 seconds in 10 days 5 hours
every 3 days 30 minutes 13 seconds in 3 hours 30 minutes 3 days

case: in ... every ...
should: not match because the 'every' keyword is not supplied an 'hours' value
in 10 hours 2 hrs 30 minutes every 3 days 45 minutes
in 6 hours 30 days 2 minutes every 12 days 4 hrs 15 minutes
in 3 hours 30 minutes 13 seconds every 3 days 30 minutes 13 seconds
</pre>
### Test: hr[s]
#### Expression
`.*every\s(\d+)\shrs*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\shrs*`
#### Test case
<pre>
case: every ... in ...
should: match '5' and '15'
every 5 days 5 hrs 15 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 15 hrs 15 days 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 5 days 5 hrs in 6 hours 2 days
every 15 days 15 hrs in 10 days 12 hours 30 seconds

case: in ... every ...
should: match '5' and '15'
in 10 days 6 hours 30 minutes 23 seconds every 5 days 30 minutes 15 hrs 13 seconds starting at 12:00
in 10 days 6 hours 30 minutes 23 seconds every 5 hrs 15 days 30 minutes 13 seconds starting at 12:00
in 6 hours 2 days every 15 hrs 5 days
in 10 days every 15 days 5 hrs

case: at ... in ... every ...
should: match '5' and '15'
at 12:00 in 10 days 6 hours 30 minutes 23 seconds every 5 days 5 hrs 30 minutes 13 seconds
at 12:00 in 10 days 6 hours 30 minutes 23 seconds every 15 days 15 hrs 30 minutes 13 seconds
at 12:00 in 10 days every 5 hours 15 days 5 hrs 5 minutes
at 12:00 in 20 hours 10 days every 15 hrs 15 days

case: at ... every ... in ...
should: match '5' and '15'
at 12:00 every 5 hrs 5 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 15 hrs 15 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 5 days 15 hrs 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds
at 12:00 every 15 days 15 hrs 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'every' keyword is not supplied an 'hrs' value
every 3 days 15 minutes in 10 days 15 hrs
every 3 hours 30 minutes 13 seconds in 10 days 5 hrs
every 3 days 30 minutes 13 seconds in 3 hrs 30 minutes 3 days

case: in ... every ...
should: not match because the 'every' keyword is not supplied an 'hrs' value
in 10 hrs 2 hrs 30 minutes every 3 days 45 minutes 5 hours
in 6 hrs 30 days 2 minutes every 12 days 4 hours 15 minutes
in 3 hrs 30 minutes 13 seconds every 3 days 2 hours 30 minutes 13 seconds
</pre>
### Test: minute[s]
#### Expression
`.*every\s(\d+)\sminutes*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\sminutes*`
#### Test case
<pre>
case: every ... in ...
should: match '30' and '15'
every 5 days 5 hrs 15 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 15 hrs 15 days 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 5 days 5 hrs 30 minutes 12 seconds in 6 hours 2 days
every 15 days 15 hrs 15 minutes 10 seconds in 10 days 12 hours 30 seconds

case: in ... every ...
should: match '30' and '15'
in 10 days 6 hours 12 minutes 23 seconds every 5 days 30 minutes 15 hrs 13 seconds starting at 12:00
in 10 days 6 hours 12 minutes 23 seconds every 5 hrs 15 days 30 minutes 13 seconds starting at 12:00
in 6 hours 2 days 3 minutes every 15 hrs 5 days 30 minute
in 10 days 9 minutes every 15 days 5 hrs 15 minute 10 seconds

case: at ... in ... every ...
should: match '30' and '15'
at 12:00 in 10 days 6 hours 12 minutes 23 seconds every 5 days 5 hrs 30 minutes 13 seconds
at 12:00 in 10 days 6 hours 12 minutes 23 seconds every 15 days 15 hrs 30 minutes 13 seconds
at 12:00 in 10 days 5 minutes every 5 hours 15 days 5 hrs 15 minutes 2 seconds
at 12:00 in 20 hours 10 days 10 minutes every 15 hrs 30 minutes 15 days 5 seconds

case: at ... every ... in ...
should: match '30' and '15'
at 12:00 every 5 hrs 5 days 15 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 15 hrs 15 days 30 minutes 13 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 5 days 15 hrs 15 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds
at 12:00 every 15 days 15 hrs 30 minutes 13 seconds in 10 days 6 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'every' keyword is not supplied an 'minutes' value
every 3 days in 10 days 15 hrs 90 minutes
every 3 hours 13 seconds in 10 days 5 hrs 68 minutes
every 3 days 13 seconds in 3 hrs 30 minutes 3 days

case: in ... every ...
should: not match because the 'every' keyword is not supplied an 'minutes' value
in 10 hrs 2 hrs 30 minutes every 3 days 5 hours
in 6 hrs 30 days 2 minutes every 12 days 4 hours
in 3 hrs 30 minutes 13 seconds every 3 days 2 hours 13 seconds
</pre>
### Test: second[s]
#### Expression
`.*every\s(\d+)\sseconds*.*?(?=in\s\d+)|.*every(?!<=in\s)(?:(?!in\s).)*(?:\s)(\d+)\sseconds*`
#### Test case
<pre>
case: every ... in ...
should: match '30' and '15'
every 5 days 5 hrs 15 minutes 15 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 15 hrs 15 days 30 minutes 15 seconds in 10 days 6 hours 30 minutes 23 seconds starting at 12:00
every 5 days 5 hrs 30 minutes 30 seconds in 6 hours 2 days 80 seconds
every 15 days 15 hrs 15 minutes 15 seconds in 10 days 12 hours 30 seconds

case: in ... every ...
should: match '30' and '15'
in 10 days 6 hours 12 minutes 23 seconds every 5 days 30 minutes 15 hrs 15 seconds starting at 12:00
in 10 days 6 hours 12 minutes 23 seconds every 5 hrs 15 days 30 minutes 15 seconds starting at 12:00
in 6 hours 2 days 3 minutes every 15 hrs 5 days 30 minute 30 seconds
in 10 days 9 minutes every 15 days 5 hrs 15 minute 15 seconds

case: at ... in ... every ...
should: match '30' and '15'
at 12:00 in 10 days 6 hours 12 minutes 23 seconds every 5 days 5 hrs 30 minutes 30 seconds
at 12:00 in 10 days 6 hours 12 minutes 23 seconds every 15 days 15 hrs 30 minutes 15 seconds
at 12:00 in 10 days 5 minutes 8 seconds every 5 hours 15 days 5 hrs 15 minutes 15 seconds
at 12:00 in 20 hours 10 days 10 minutes 4 seconds every 15 hrs 30 minutes 15 days 30 seconds

case: at ... every ... in ...
should: match '30' and '15'
at 12:00 every 5 hrs 5 days 15 minutes 15 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 15 hrs 15 days 30 minutes 15 seconds in 6 hours 10 days 30 minutes 23 seconds
at 12:00 every 5 days 15 hrs 15 minutes 30 seconds in 10 days 6 hours 30 minutes 23 seconds
at 12:00 every 15 days 15 hrs 30 minutes 30 seconds in 10 days 6 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'every' keyword is not supplied an 'seconds' value
every 3 days in 10 days 15 hrs 90 minutes 13 seconds
every 3 hours in 10 days 5 hrs 68 minutes 13 seconds
every 3 days in 3 hrs 30 minutes 3 days 13 seconds

case: in ... every ...
should: not match because the 'every' keyword is not supplied an 'seconds' value
in 10 hrs 2 hrs 30 minutes 13 seconds every 3 days 5 hours
in 6 hrs 30 days 2 minutes 13 seconds every 12 days 4 hours
in 3 hrs 30 minutes 13 seconds every 3 days 2 hours
</pre>
## Keyword 'in'
### Test: day[s]
#### Expression
#`.*in\s(\d+)\sdays*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\sdays*`
#### Test case
<pre>
case: every ... in ...
should: match '20'
every 5 days 3 hours 15 minutes 13 seconds in 20 days 6 hours 30 minutes 23 seconds starting at 12:00
every 3 hours 15 days 30 minutes 13 seconds in 20 days 6 hours 30 minutes 23 seconds starting at 12:00
every 5 days in 6 hours 20 days
every 15 days in 20 days

case: in ... every ...
should: match '20'
in 20 days 6 hours 30 minutes 23 seconds every 5 days 30 minutes 13 seconds starting at 12:00
in 20 days 6 hours 30 minutes 23 seconds every 3 hours 15 days 30 minutes 13 seconds starting at 12:00
in 6 hours 20 days every 3 hours 5 days
in 20 days every 15 days

case: at ... in ... every ...
should: match '20'
at 12:00 in 5 hours 20 days 30 minutes 23 seconds every 5 days 3 hours 30 minutes 13 seconds
at 12:00 in 20 days 6 hours 30 minutes 23 seconds every 15 days 3 hours 30 minutes 13 seconds
at 12:00 in 20 days every 5 days
at 12:00 in 20 hours 20 days every 1 hour 15 days

case: at ... every ... in ...
should: match '20'
at 12:00 every 3 hours 5 days 30 minutes 13 seconds in 6 hours 20 days 30 minutes 23 seconds
at 12:00 every 3 hours 15 days 30 minutes 13 seconds in 6 hours 20 days 30 minutes 23 seconds
at 12:00 every 5 days 3 hours 30 minutes 13 seconds in 20 days 6 hours 30 minutes 23 seconds
at 12:00 every 15 days 3 hours 30 minutes 13 seconds in 20 days 6 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'in' keyword is not supplied a 'days' value
every 15 days 3 hours in 12 hours 15 minutes
every 2 days 3 hours 30 minutes 13 seconds in 10 hours 15 minutes
every 3 hours 5 days 30 minutes 13 seconds in 3 hours 30 minutes

case: in ... every ...
should: not match because the 'every' keyword is not supplied a 'days' value
in 30 minutes every 5 days 3 hours 45 minutes
in 6 hours 2 minutes every 10 days 12 hours
in 3 hours 30 minutes 13 seconds every 2 days 3 hours 30 minutes 13 seconds
</pre>
### Test: hour[s]
#### Expression
`.*in\s(\d+)\shours*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\shours*`
#### Test case
<pre>
case: every ... in ...
should: match '20'
every 5 days 3 hours 15 minutes 13 seconds in 20 days 20 hours 23 seconds starting at 12:00
every 3 hours 15 days 30 minutes 13 seconds in 20 days 20 hours 30 minutes starting at 12:00
every 5 days in 20 hours 20 days
every 15 days 10 hours in 20 days 20 hours

case: in ... every ...
should: match '10'
in 1 day 10 hours 30 minutes 23 seconds every 5 days 30 hours starting at 12:00
in 10 hours 30 minutes 23 seconds every 3 hours 15 days 13 seconds starting at 12:00
in 10 hours 20 days every 3 hours 5 days
in 20 days 10 hours every 15 days 5 hours

case: at ... in ... every ...
should: match '20'
at 12:00 in 20 hours 20 days 30 minutes 23 seconds every 5 days 3 hours 30 minutes 13 seconds
at 12:00 in 20 days 20 hours 30 minutes 23 seconds every 15 days 3 hours 30 minutes 13 seconds
at 12:00 in 20 days 20 hours every 5 days 9 hours
at 12:00 in 20 hours 20 days every 1 hour 15 days

case: at ... every ... in ...
should: match '20'
at 12:00 every 3 hours 5 days 30 minutes 13 seconds in 20 hours 20 days 30 minutes 23 seconds
at 12:00 every 3 hours 15 days 30 minutes 13 seconds in 20 hours 20 days 30 minutes 23 seconds
at 12:00 every 5 days 3 hours 30 minutes 13 seconds in 20 days 20 hours 30 minutes 23 seconds
at 12:00 every 15 days 3 hours 30 minutes 13 seconds in 20 days 20 hours 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'in' keyword is not supplied a 'hours' value
every 15 days 3 hours in 12 days 15 minutes
every 2 days 3 hours 30 minutes 13 seconds in 10 days 15 minutes
every 3 hours 5 days 30 minutes 13 seconds in 3 days 30 minutes

case: in ... every ...
should: not match because the 'every' keyword is not supplied a 'hours' value
in 30 minutes every 5 days 3 hours 45 minutes
in 6 days 2 minutes every 10 days 12 hours
in 3 days 30 minutes 13 seconds every 2 days 3 hours 30 minutes 13 seconds
</pre>
### Test: hr[s]
#### Expression
`.*in\s(\d+)\shrs*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\shrs*`
#### Test case
<pre>
case: every ... in ...
should: match '20'
every 5 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 23 seconds starting at 12:00
every 3 hrs 15 days 30 minutes 13 seconds in 20 days 20 hrs 30 minutes starting at 12:00
every 5 days in 20 hrs 20 days
every 15 days 10 hrs in 20 days 20 hrs

case: in ... every ...
should: match '10'
in 1 day 10 hrs 30 minutes 23 seconds every 5 days 30 hrs starting at 12:00
in 10 hrs 30 minutes 23 seconds every 3 hrs 15 days 13 seconds starting at 12:00
in 10 hrs 20 days every 3 hrs 5 days
in 20 days 10 hrs every 15 days 5 hrs

case: at ... in ... every ...
should: match '20'
at 12:00 in 20 hrs 20 days 30 minutes 23 seconds every 5 days 3 hrs 30 minutes 13 seconds
at 12:00 in 20 days 20 hrs 30 minutes 23 seconds every 15 days 3 hrs 30 minutes 13 seconds
at 12:00 in 20 days 20 hrs every 5 days 9 hrs
at 12:00 in 20 hrs 20 days every 1 hrs 15 days

case: at ... every ... in ...
should: match '20'
at 12:00 every 3 hrs 5 days 30 minutes 13 seconds in 20 hrs 20 days 30 minutes 23 seconds
at 12:00 every 3 hrs 15 days 30 minutes 13 seconds in 20 hrs 20 days 30 minutes 23 seconds
at 12:00 every 5 days 3 hrs 30 minutes 13 seconds in 20 days 20 hrs 30 minutes 23 seconds
at 12:00 every 15 days 3 hrs 30 minutes 13 seconds in 20 days 20 hrs 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'in' keyword is not supplied a 'hrs' value
every 15 days 3 hrs in 12 days 15 minutes
every 2 days 3 hrs 30 minutes 13 seconds in 10 days 15 minutes
every 3 hrs 5 days 30 minutes 13 seconds in 3 days 30 minutes

case: in ... every ...
should: not match because the 'every' keyword is not supplied a 'hrs' value
in 30 minutes every 5 days 3 hrs 45 minutes
in 6 days 2 minutes every 10 days 12 hrs
in 3 days 30 minutes 13 seconds every 2 days 3 hrs 30 minutes 13 seconds
</pre>
### Test: minute[s]
#### Expression
`.*in\s(\d+)\sminutes*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every\s).)*(?:\s)(\d+)\sminutes*`
#### Test case
<pre>
case: every ... in ...
should: match '30'
every 5 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 30 minutes 23 seconds starting at 12:00
every 3 hrs 15 days 15 minutes 13 seconds in 20 days 20 hrs 30 minutes starting at 12:00
every 5 days 15 minutes in 20 hrs 20 days 30 minutes
every 15 days 15 minutes  10 hrs in 30 minutes 20 days 20 hrs

case: in ... every ...
should: match '30'
in 1 day 10 hrs 30 minutes 23 seconds every 5 days 15 minutes starting at 12:00
in 10 hrs 30 minutes 23 seconds every 3 hrs 15 days 15 minutes starting at 12:00
in 10 hrs 20 days 30 minutes every 3 hrs 5 days 15 minutes
in 20 days 10 hrs 30 minutes every 15 days 5 hrs 15 minutes

case: at ... in ... every ...
should: match '30'
at 12:00 in 20 hrs 20 days 30 minutes 23 seconds every 5 days 3 hrs 30 minutes 13 seconds
at 12:00 in 20 days 20 hrs 30 minutes 23 seconds every 15 days 3 hrs 30 minutes 13 seconds
at 12:00 in 20 days 20 hrs 30 minutes every 5 days 9 hrs 15 minutes
at 12:00 in 20 hrs 30 minutes 20 days every 1 hrs 15 days 15 minutes

case: at ... every ... in ...
should: match '30'
at 12:00 every 3 hrs 5 days 15 minutes 13 seconds in 20 hrs 20 days 30 minutes 23 seconds
at 12:00 every 3 hrs 15 days 15 minutes 13 seconds in 20 hrs 20 days 30 minutes 23 seconds
at 12:00 every 5 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 30 minutes 23 seconds
at 12:00 every 15 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 30 minutes 23 seconds

case: every ... in ...
should: not match because the 'in' keyword is not supplied a 'minutes' value
every 15 days 3 hrs 15 minutes in 12 days
every 2 days 3 hrs 15 minutes 13 seconds in 10 days
every 3 hrs 5 days 15 minutes 13 seconds in 3 days

case: in ... every ...
should: not match because the 'every' keyword is not supplied a 'minutes' value
in every 5 days 3 hrs 30 minutes
in 6 days every 10 days 12 hrs 30 minutes
in 3 days 13 seconds every 2 days 3 hrs 30 minutes 13 seconds
</pre>
### Test: second[s]
#### Expression
`.*in\s(\d+)\sseconds*.*?(?=every\s\d+)|.*in(?!<=every|u)(?:(?!every).)*(?:\s)(\d+)\sseconds*`
#### Test case
<pre>
case: every ... in ...
should: match '30'
every 5 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 30 minutes 30 seconds starting at 12:00
every 3 hrs 15 days 15 minutes 13 seconds in 20 days 20 hrs 30 seconds starting at 12:00
every 5 days 15 minutes in 20 hrs 20 days 30 minutes 30 seconds
every 15 days 15 minutes 10 hrs in 30 minutes 20 days 20 hrs 30 seconds

case: in ... every ...
should: match '30'
in 1 day 10 hrs 30 minutes 30 seconds every 5 days 15 seconds starting at 12:00
in 10 hrs 30 minutes 30 seconds every 3 hrs 15 days 15 seconds starting at 12:00
in 10 hrs 20 days 30 seconds every 3 hrs 5 days 15 seconds
in 20 days 10 hrs 30 seconds every 15 days 5 hrs 15 seconds

case: at ... in ... every ...
should: match '30'
at 12:00 in 20 hrs 20 days 30 minutes 30 seconds every 5 days 3 hrs 30 minutes 13 seconds
at 12:00 in 20 days 20 hrs 30 minutes 30 seconds every 15 days 3 hrs 30 minutes 13 seconds
at 12:00 in 20 days 20 hrs 30 seconds every 5 days 9 hrs 15 seconds
at 12:00 in 20 hrs 30 seconds 20 days every 1 hrs 15 days 15 seconds

case: at ... every ... in ...
should: match '30'
at 12:00 every 3 hrs 5 days 15 minutes 13 seconds in 20 hrs 20 days 30 minutes 30 seconds
at 12:00 every 3 hrs 15 days 15 minutes 13 seconds in 20 hrs 20 days 30 minutes 30 seconds
at 12:00 every 5 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 30 minutes 30 seconds
at 12:00 every 15 days 3 hrs 15 minutes 13 seconds in 20 days 20 hrs 30 minutes 30 seconds

case: every ... in ...
should: not match because the 'in' keyword is not supplied a 'seconds' value
every 15 days 3 hrs 15 seconds in 12 days
every 2 days 3 hrs 15 minutes 13 seconds in 10 days
every 3 hrs 5 days 15 minutes 13 seconds in 3 days

case: in ... every ...
should: not match because the 'every' keyword is not supplied a 'seconds' value
in every 5 days 3 hrs 30 seconds
in 6 days every 10 days 12 hrs 30 seconds
in 3 days 13 hours every 2 days 3 hrs 30 minutes 13 seconds
</pre>
