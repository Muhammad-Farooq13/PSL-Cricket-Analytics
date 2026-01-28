name: Bug Report
description: Create a report to help us improve
title: "[BUG] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill out the form below.
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what the bug is
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Run command...
        2. Input data...
        3. See error...
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should happen instead?
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: |
        Please include:
        - Python version
        - OS (Windows/Linux/Mac)
        - Error message/traceback
    validations:
      required: true
