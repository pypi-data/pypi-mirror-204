# Data Science Common (dsc)
> UNDER CONSTRUCTION: 
> A simple Python library for facilitating analysis.  

![build status](https://github.com/kelleyrw/data_science_common/actions/workflows/release.yml/badge.svg)

When performing data analysis and other data intensive tasks, one often finds many examples where they use same code 
or workflow repeatedly.  The next obvious step is to write resuable piece.  This project is an attempt to collect 
all of these reusable pieces on a central place and to facilitate collaboration.

This library contains methods to help with:
 * String manipulation
 * Date manipulation
 * Data analysis
 * Database connections and queries
 * Cloud computing 

This is an experimental library and will possibly be broken into smaller pieces in the future.

## Installation

```sh
pip install data-science-common
```

## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
```

## Release History

* 0.1.7
  * refactored code layout and updated build to pyproject.toml paradigm 
* 0.1.6
  * updating documentation and deployment infrastructure
* 0.1.5
  * CHANGE: added package `dsc.util.date` 
  * CHANGE: added package `dsc.util.db`
  * CHANGE: added package `dsc.util.error`
  * CHANGE: added package `dsc.util.obj`
  * CHANGE: added package `dsc.util.pd`
  * CHANGE: added package `dsc.util.str`
* 0.1.4
  * CHANGE: adding CI/CD 
* 0.1
    * Initial release 

## Meta

Ryan Kelley – kelleyrw@gmail.com

Distributed under the Apache License, Version 2.0. See ``LICENSE`` for more information.

[https://github.com/kelleyrw](https://github.com/kelleyrw)

## Contributing

1. Fork it (<https://github.com/kelleyrw/data_science_common/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki

### requirements for development

* black
* isort
* pandoc