## CSV validator

**Development status: Alpha**

This library provides a wrapper around [goodtables-py](https://github.com/frictionlessdata/goodtables-py) & [table schema](https://frictionlessdata.io/specs/table-schema) csv validation.

The main goals of this library

 - To collate standard error messages from goodtables and provide easy, human readable reference
 to column and row errors within csv files.
 
 - Provide additional custom checks to extend out of the box validation provided by goodtables.
 

The development of this library was driven by work on a prototype brownfield land csv validation web application. 

To make our lives easier we  bundled a table schema for the [Brownfield land data standard](https://www.gov.uk/government/publications/brownfield-land-registers-data-standard/publish-your-brownfield-land-data#publish-your-brownfield-land-data) 
in this code base. This is just a convenience and if development continues it's likely the schema can be hosted elsewhere. 


This library can be used programmatically and or from command line.

### Command line usage
    -- example usage coming soon

The command line produces result output to the console. The format of the output defaults to a summary of validation
results. It can also product html or json output to standard output, so needs to be redirected in order to produce
an html or json file.

### Programmatic usage
    -- again, coming soon


#### To run tests
    
    pytest
    
To run tests with linting

    pytest --flake8
    
    