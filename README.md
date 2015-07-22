khayyam
=======

Jalali Date and Time types and algorithms for Python2 and Python3.


### To Do

  * Constructors act as converter: `JalaliDate(date)`
  * Create TehranDatetime object
  * Add two methods: d.next(SATURDAY) & d.previous(WEDNESDAY)
  * Use compiled regex if matters in performance
  * Readme:
    * Formatting & parsing
    * Conversions
    * Operators
  * Doc
    * Introduction
      * Formatting & parsing
      * Operators
      * Conversions
    * Review all object's documentation
    * Parsing, post processors priority
    * Compatibility
    * Naming conventions
    
  * Cython
    * setup.py pure python fallback switch
    * Distribute pre compiled binaries from some platforms
  * Alphabetical number format

### Change Log

  * 2.3.0-alpha (2015-07-22)
    * Constants are moved to formatting packages except MINYEAR, MAXYEAR ans weekdays. 
    

  * 2.2.1-alpha (2015-07-21)
    * Doc: Reading package's version automatically from khayyam/__init__.py in `sphinx/conf.py`
    * Doc: Installation: (PYPI, Development version)
    * Doc: Testing
    * Doc: Contribution

  * 2.2.0-alpha (2015-07-21)
    * Generating API Documentation  

  * 2.1.0-alpha (2015-07-20)
    * Adding ascii weekdayname in `JalaliDatetime` and `JalaliDate` representation(__repr__). 

  * 2.0.0-alpha (2015-07-19) Incompatible with < 2.0.0
    * JalaliDate: method `localformat` renamed to `localdateformat`.
    * JalaliDatetime: method `localformat` renamed to `localdatetimeformat`.
    * JalaliDatetime: method `localshortformat_ascii` renamed to `localshortformatascii`.
    * JalaliDatetime: method `localdatetimeformat_ascii` renamed to `localdatetimeformatascii`.
    * JalaliDatetime: method `ampm_ascii` renamed to `ampmascii`.
    * JalaliDatetime: Migrating to New Formatter/Parser Engine
    * TehTz: renamed to TehranTimezone
    * Comparison and Timezones
    * Comparison with `datetime.date` & `datetime.datetime`
    * Fixing timezone bug
    
  * 1.1.0 (2015-07-17)
    * JalaliDate: New Formatter/Parser & full unittests.
    