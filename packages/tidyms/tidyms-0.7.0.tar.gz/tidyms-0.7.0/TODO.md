TODO
====

- URGENT: fix warnings in pytest.
- URGENT: fix bug in annotation: MMI search uses peak area/ peak height. This has some problems in the search.
- The best way would be to perform an overlap-based search.
- 1: search by m/z; 2- filter by similarity ; 3 filter by qp rules.

Refactor annotation:

- convert annotation into a subpackage
- Remove usage of pandas
- Work with list of features created from a list of ROI
- To keep track of data, add an _index parameter to ROI and features.
- this allows to annotate features before computing descriptors and then
- remove non-annotated features.
- Define how the overlap based abundance should be computed. Maybe this has to be defined for each feature type.