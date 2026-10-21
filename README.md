This repository builds upon the original work by [PMeira](https://github.com/PMeira) at [AltDSS-Schema](https://github.com/dss-extensions/AltDSS-Schema), which aimed to define a structured JSON-based schema for DSS circuit representation. The schema has been packaged in this repository with slight modifications, enabling users to add the package as a dependency for downstream applications. This repository is actively maintained by [Tarek Elgindy](https://github.com/tarekelgindy)

When both total load loss and individual winding resistances are supplied,
transformer and transformer-code serializers emit `%LoadLoss` before `%Rs`.
Explicit winding resistances take precedence because OpenDSS resets the first
two winding resistances when it processes `%LoadLoss`.

Run serialization regression tests with `python -m pytest tests`.
