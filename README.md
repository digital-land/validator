## CSV validator

**Development status: Alpha**

This library provides a wrapper around [goodtables-py](https://github.com/frictionlessdata/goodtables-py) & [table schema](https://frictionlessdata.io/specs/table-schema) csv validation.

The main goals of this library

 - To collate standard error messages from goodtables and provide easy, human readable reference
 to column and row errors within csv files.
 
 - Provide additional custom checks to extend out of the box validation provided by goodtables.
 

The development of this library was driven by work on a prototype brownfield land csv validation web application. 

To make our lives easier we  bundled [a table schema]((validator/schema/brownfield-land-v2.json)) for the [Brownfield land data standard](https://www.gov.uk/government/publications/brownfield-land-registers-data-standard/publish-your-brownfield-land-data#publish-your-brownfield-land-data) 
in this code base. This is just a convenience and if development continues it's likely the schema can be hosted elsewhere. 

This library can be used programmatically and or from command line.

### Installation

Until/Unless this package in put into pypy, you can install as an editable dependency. If using pipenv add this
to your Pipfile in [packages] section:

    validator = {editable = true,git = "https://github.com/digital-land/validator.git"}
    
If you're using pip and a requirements file:

    -e git+https://github.com/digital-land/validator.git



### Command  line usage

The package has a command line entry point, which you can use to validate files. To see the help text enter the following
in a console.

    validate --help

The command line produces result output to the console. The format of the output defaults to a summary of validation
results. It can also product html or json output to standard output, so needs to be redirected in order to produce
an html or json file. 

Note that the Result that is used to create all the forms of output is also used in the 
[validation prototype web application](https://github.com/digital-land/brownfield-sites-validator) 

To run the validator against [version 2 of the brownfield register schema](validator/schema/brownfield-land-v2.json)

    validate --file /path/to/a-brownfield-register.csv
    
You can also validate against another schema:

    validate --file /path/to/a-brownfield-register.csv --schema /path/to/a-table-schema.json
    

All output of the script is sent to the console. The default is a plain text summary of the results.

To specify html or json output:

    validate --file /path/to/a-brownfield-register.csv --output html
   
or
    
    validate  --file /path/to/a-brownfield-register.csv --output json


Redirect output to create a file from the result:

     validate --file /path/to/a-brownfield-register.csv --output html > a-brownfield-register-validation-result.html
     

### Programmatic usage

     result = validate_file(file, schema)
     

 - `file` is the path to the file to validate
 - `schema` is a python dictionary representing the table schema (in other words call json.load on a table schema json file)
 
 - `result` is the wrapped up goodtables validation result with additional convenience methods for extracting error
 messages by column name or row number.



#### To run tests
    
    pytest
    
To run tests with linting

    pytest --flake8
    
    