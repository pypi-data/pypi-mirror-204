### New Code Utils

Basic components for the development of NewCode_

### Requirements

1. Install pip current

Quick start
-----------
``` bash

1. Add "newcode_utils" to your INSTALLED_APPS setting like this::
INSTALLED_APPS = [
        ...
        'newcode_utils',
    ]
```

### Components

* Admin
    * AuditAdmin
    * AuditStackedInline
    * AuditTabularInline
* Models
    * Audit
* Helpers
    * Utils
        * File departments of columbia
    * Utils permission rest

### Deploy pypi versions

* install requirements

``` bash
pip install -U twine wheel setuptools
```

* update repository

``` bash
python3.7 setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository pypi dist/newcode-utils-0.1.1*
```


