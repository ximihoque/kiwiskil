---
type: Code Group
title: tests/fixtures
description: This group is a multi-language fixture corpus used by kiwiskil's indexer
  test suite to validate symbol extraction, component ID generation, and wiki-page
  mapping across five language parsers (Ruby, Rust, Go, Java, Python).
tags:
- tests
- fixtures
timestamp: '2026-06-21T20:09:33.562703+00:00'
resource: tests/fixtures
---
# tests/fixtures/
<!-- kiwiskil:deep -->

## Overview

This group is a multi-language fixture corpus used by kiwiskil's indexer test suite to validate symbol extraction, component ID generation, and wiki-page mapping across five language parsers (Ruby, Rust, Go, Java, Python). Each fixture implements the same structural patterns—a counter class with a bump/helper chain, a greeting function, and (in Python) an auth decorator—so parser output can be compared against known-good symbol tables without coupling tests to real production code. The Python auth fixture additionally exercises decorator wrapping and OAuth2 token rotation patterns that stress-test the indexer's ability to resolve inner functions and call-graph edges. Together these files form the ground truth for regression tests: if a parser change breaks extraction, these fixtures surface the breakage deterministically.

## Modules
| File | Purpose |
|------|---------|
| tests/fixtures/sample_ruby/widget.rb | Sample Ruby classes demonstrating parsing |
| tests/fixtures/sample_rust/widget.rs | Sample Rust widget struct and greeting functions |
| tests/fixtures/sample_go/server.go | Sample Go code with server struct and methods |
| tests/fixtures/sample_java/Widget.java | Sample Java widget class for testing extraction |
| tests/fixtures/sample_py/auth.py | Sample Python authentication module with validators |
## Key Symbols
| ID | Type | Description |
|----|------|-------------|
| `tests/fixtures/sample_go/server.go::Greet` | function | Return friendly greeting string for given name |
| `tests/fixtures/sample_go/server.go::Server` | class | HTTP server holder with listen address |
| `tests/fixtures/sample_go/server.go::Start` | function | Launch HTTP server greeting clients |
| `tests/fixtures/sample_java/Widget.java::Widget` | class | Widget counter—increments via bump method |
| `tests/fixtures/sample_java/Widget.java::Widget.bump` | method | Increment counter by n, return result |
| `tests/fixtures/sample_java/Widget.java::Widget.helper` | method | Internal helper for counter operations |
| `tests/fixtures/sample_py/auth.py::TokenValidator` | class | OAuth2 token validator and rotation handler |
| `tests/fixtures/sample_py/auth.py::TokenValidator.refresh` | method | Rotate OAuth2 refresh tokens via signing |
| `tests/fixtures/sample_py/auth.py::require_auth` | function | Route guard decorator enforcing authentication |
| `tests/fixtures/sample_py/auth.py::wrapper` | function | Inner decorator wrapper executing guarded function |
| `tests/fixtures/sample_ruby/widget.rb::Greeter` | class | Greeting helper class providing hello method |
| `tests/fixtures/sample_ruby/widget.rb::Greeter.hello` | method | Print greeting message for given name |
| `tests/fixtures/sample_ruby/widget.rb::Widget` | class | Widget counter class with bump increment |
| `tests/fixtures/sample_ruby/widget.rb::Widget.bump` | method | Increment counter by n via helper |
| `tests/fixtures/sample_ruby/widget.rb::top_level` | function | Top-level utility function |
| `tests/fixtures/sample_rust/widget.rs::Widget` | class | Widget struct counting things via bump |
| `tests/fixtures/sample_rust/widget.rs::Widget.bump` | method | Increment count by n, return result |
| `tests/fixtures/sample_rust/widget.rs::greet` | function | Greet given name via string construction |
| `tests/fixtures/sample_rust/widget.rs::Speak` | class | Speak trait or struct |
| `tests/fixtures/sample_rust/widget.rs::speak` | function | Speak function |
## Symbol Relationships
### `Greet`
- **Callers (1):** Start
- **Calls:** Println
- **Editing this affects:** Start
### `Start`
- **Callers (0):** none
- **Calls:** Greet, ListenAndServe
- **Editing this affects:** none
### `Widget.bump`
- **Callers (0):** none
- **Calls:** helper
- **Editing this affects:** none
### `TokenValidator.refresh`
- **Callers (0):** none
- **Calls:** sign_payload
- **Editing this affects:** none
### `require_auth`
- **Callers (0):** none
- **Calls:** func
- **Editing this affects:** none
### `wrapper`
- **Callers (0):** none
- **Calls:** func
- **Editing this affects:** none
### `Greeter.hello`
- **Callers (0):** none
- **Calls:** puts
- **Editing this affects:** none
### `Widget.bump`
- **Callers (0):** none
- **Calls:** helper
- **Editing this affects:** none
### `Widget.bump`
- **Callers (0):** none
- **Calls:** helper
- **Editing this affects:** none
### `greet`
- **Callers (0):** none
- **Calls:** from
- **Editing this affects:** none
## Data Flows
- Indexer parses fixture file → extracts symbol list → test asserts against expected component IDs (e.g. 'tests/fixtures/sample_py/auth.py::TokenValidator.refresh')
- Go fixture: HTTP request hits Start → Start calls Greet(name) → Greet returns greeting string → ListenAndServe delivers response — tests verify all three symbols are linked in the call graph
- Python fixture: require_auth decorates a route → at call time wrapper invokes func → tests assert wrapper's call edge to func is captured, not collapsed into require_auth
## Design Constraints
- Widget.bump in all languages delegates to a private helper method — the indexer must emit a call edge from bump to helper even though helper is not public; tests will fail if private symbols are filtered pre-graph-construction
- Python wrapper is a closure defined inside require_auth — it must be indexed as a distinct symbol (auth.py::wrapper) with its own call edge to func, not merged into its enclosing function's node
- TokenValidator.refresh calls sign_payload which is NOT defined in this file — the call edge must be recorded as an unresolved external reference, not silently dropped
- Go Server struct has no methods in this fixture; its Start function is a package-level function that receives Server as a value type — parsers that require method receivers will miss this relationship
- Rust Speak trait/struct and speak function are minimal stubs with no body logic — they exist solely to exercise trait-vs-struct disambiguation in the Rust parser, not to represent any real behavior
- Ruby top_level is a bare module-level function (no class), testing the indexer's handling of non-method callables; it must appear in the symbol list with no parent class component ID
## Relationships
- **Calls:** Greet, ListenAndServe, Println, from, func, helper, puts, sign_payload
- **Called by:** tests/fixtures/sample_go/server.go::Start
- **Imports from:** hashlib, import (, import java.util.ArrayList;, import java.util.List;, require 'json', require_relative 'helper', use std::fmt;, utils.crypto.sign_payload
## Entry Points
- `Server`
- `Start`
- `Widget`
- `TokenValidator`
- `require_auth`
- `wrapper`
- `Greeter`
- `Widget`
- `top_level`
- `Widget`
- `greet`
- `Speak`
- `speak`
