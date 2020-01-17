## Brownfield land CSV validator
[![build](https://travis-ci.org/digital-land/validator.svg?branch=master)](https://travis-ci.org/digital-land/validator)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/digital-land/validator/blob/master/LICENSE)

**Development status: Alpha**

This library provides a wrapper around [goodtables-py](https://github.com/frictionlessdata/goodtables-py) & [table schema](https://frictionlessdata.io/specs/table-schema) csv validation.

The main goals of this library

 - To collate standard error messages from goodtables and provide easy, human readable reference
 to column and row errors within csv files.
 
 - Provide additional custom checks to extend out of the box validation provided by goodtables.
 

The development of this library was driven by work on a prototype brownfield land csv validation web application. 

To make our lives easier we  bundled [a table schema](validator/schema/brownfield-land-v2.json) for the [Brownfield land data standard](https://www.gov.uk/government/publications/brownfield-land-registers-data-standard/publish-your-brownfield-land-data#publish-your-brownfield-land-data) 
in this code base. This is just a convenience and if development continues it's likely the schema can be hosted elsewhere. 

This library can be used programmatically and or from command line.

### Installation

Until/Unless this package in put into pypy, you can install as an editable dependency. If using pipenv add this
to your Pipfile in [packages] section:

    validator = {editable = true,git = "https://github.com/digital-land/validator.git"}

If you're using pip add the following to your requirements file:

    -e git+https://github.com/digital-land/validator.git#egg=Validator

#### Dependencies

* libmagic (install with Homebrew on OS X)

### Command  line usage

The package has a command line entry point, which you can use to validate files. To see the help text enter the following
in a console.

    validate --help

The command line prints result output to the console. The format of the output defaults to a summary of validation
results. It can also output an html or json version of the result, also to the console. Therefore if you want to save the html or json you should redirect the output to a file.

Note that the result object that is used to create all the forms of output is also used in the 
[validation prototype web application](https://github.com/digital-land/brownfield-sites-validator) so it's easy to create similar html in both use cases.

To run the validator against [version 2 of the brownfield register schema](validator/schema/brownfield-land-v2.json)

    validate --file /path/to/a-brownfield-register.csv
    
You can also validate against another schema:

    validate --file /path/to/a-brownfield-register.csv --schema /path/to/a-table-schema.json
    

All output of the script is sent as json to the console.

Redirect output to create a file from the result:

     validate --file /path/to/a-brownfield-register.csv > result.json
     

### Programmatic usage

     from validator.validator import validate_file

     result = validate_file(file, schema)
     

 - `file` is the path to the file to validate
 - `schema` is a python dictionary representing the table schema (in other words call json.load on a table schema json file)
 
 - `result` is the wrapped up goodtables validation result with additional convenience methods for extracting error
 messages by column name or row number.



#### To run tests
    
    pytest
    
To run tests with linting

    pytest --flake8
    
 
#### TODO

- report on detected character encoding not being UTF-8
- Remove harmonisation code
- Warn rather than error new fields which are missing
- Warn rather than error unexpected fields
- Support other schemas than brownfield sites
- Handle multiple files and data packages
