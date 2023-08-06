v3.6.0 (2023-04-24)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add `VBINMOSC` and `VBICMOSC` keys that encode the total number of and current mosaic repeat in VBI data. (`#35 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/35>`__)


v3.5.0 (2023-04-10)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Added `NSPECLNS` and `SPECLN<sl>` keys to support inclusion of spectral line information. (`#34 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/34>`__)


v3.4.0 (2023-03-15)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add CRYO-NIRSP keys for tracking number of map scans. (`#32 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/32>`__)
- Change units for some VISP specific keywords. (`#33 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/33>`__)


v3.3.0 (2023-02-15)
===================

Bug Fixes to the Python API
---------------------------

- Proposal and experiment ID groups do not get copied from the raw headers. (`#30 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/30>`__)


Documentation
-------------

- Update FITS L0 schema to SPEC-0122 revision H. (`#31 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/31>`__)


v3.2.1 (2023-02-02)
===================

Bug Fixes to the Python API
---------------------------

- Made expansions conditional on keywords that determine their range existing. (`#29 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/29>`__)


v3.2.0 (2023-02-01)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Revert DL-NIRSP keywords to not required. (`#28 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/28>`__)


v3.1.0 (2023-02-01)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add contributing proposal and experiment id keywords. (`#24 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/24>`__)
- Conform with SPEC-0122 revision G. (`#26 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/26>`__)
- Set required DL-NIRSP keywords. (`#27 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/27>`__)


New Feature in the Python API
-----------------------------

- Refactor how FITS keywords are integer-expanded. (`#25 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/25>`__)


v3.0.0 (2022-10-26)
===================

Bug Fixes to the Python API
---------------------------

- VELOSYS keyword type changed from bool to float. (`#23 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/23>`__)

Misc
----

- Prevent compression header keywords from being moved around during header refactoring. (`#23 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/23>`__)

v2.1.2 (2022-09-14)
===================

Bugfix
---------------------------

- Fix the type of some reprocessing keywords.


v2.1.1 (2022-09-12)
===================

Bugfix
------

- Relaxing requiredness of headers added in v2.1.0


v2.1.0 (2022-09-12)
===================

Features
--------

- Adding new keywords to support the addition of reprocessing metadata to the FITS headers.


v2.0.0 (2022-04-26)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Updated Spec122 and Spec214 schemas to be consistent with SPEC-122 Rev F. (`#21 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/21>`__)


New Feature in the Python API
-----------------------------

- Change the return values of all specification loading functions to be
  ``frozendict``.
  This means that the specifications once constructed are (largely) immutable and
  therefore can be cached. Caching the specfications massively speeds up
  subsequent calls to the specification construction functions. (`#22 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/22>`__)


v1.5.0 (2022-02-10)
===================

Documentation
-------------

- Add a documenation build for the yaml files containing the specifications and other information about the data products. (`#18 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/18>`__)
