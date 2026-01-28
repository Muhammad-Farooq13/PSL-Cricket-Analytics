name: Feature Request
description: Suggest an idea for this project
title: "[FEATURE] "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for your interest in improving this project!
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear and concise description of what you want to happen
      placeholder: "I want to be able to..."
    validations:
      required: true
  - type: textarea
    id: motivation
    attributes:
      label: Motivation and Context
      description: Why do you want this feature? What problem does it solve?
    validations:
      required: true
  - type: textarea
    id: implementation
    attributes:
      label: Possible Implementation
      description: How do you think this should be implemented?
    validations:
      required: false
