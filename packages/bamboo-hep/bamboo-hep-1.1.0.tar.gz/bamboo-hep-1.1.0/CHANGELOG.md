# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2023-04-21

### Added
- Support of [SOFIE](https://root.cern/doc/v626/release-notes.html#sofie-code-generation-for-fast-inference-of-deep-learning-models)
- Check that `VariableBinning` edges are strictly increasing
- Helpers to evaluate CMS b-tagging scale factors using [correctionlib](https://cms-nanoaod.github.io/correctionlib/)

### Changed
- Make it possible to declare several calculators for on-the-fly variations of a given collection.
  This changes the public attribute of the variations proxy (e.g. `tree._Jet.calcProd`) to an iterable
  (`tree._Jet.calcProds`).
- Pass jet parton flavour to CMSJMECalculators, for pure-flavour JEC variations.
  Requires v0.2.0 of the calculators.

### Fixed
- Fix forwarding of analysis module CLI list-type arguments to workers

## [1.0.1] - 2021-02-28

### Fixed
- Fix cut flow reports with `recursive=True` argument
- Fix in SLURM batch backend: `NODE_FAIL` status should be interpreted as a failed job 
- Fix running `bambooRun` with `--onlyprepare`

## [1.0.0] - 2021-12-13

This is the first stable release of bamboo, after quite some time of active
development and use in several analyses.
Having releases and meaningful version numbers should make it easier
to keep track of changes between versions, and to coordinate development.
