# Sending Notifications to Your Smartphone for Specific Keywords in Emails
The project involves creating a program that reads gmail and sends notifications to your smartphone using slack when a specific keyword appears.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Issue](https://img.shields.io/github/issues/kw9212/project_2023)](https://github.com/kw9212/project_2023.git)
![](https://github.com/kw9212/project_2023/actions/workflows/build.yml/badge.svg)
[![codecov](https://codecov.io/github/kw9212/project_2023/branch/main/graph/badge.svg?token=05c337ef-226f-41c3-b136-0fe9842b5192)](https://app.codecov.io/gh/kw9212/project_2023)

# Overview
This idea came from the challenge of having to sort through many emails every day to find the important ones. Gmail already has a labeling function that classifies emails based on specific email addresses as filters. This project aims to create a function that sends notifications based on keywords using slack and smartphones. There is also potential to expand this project to find information in other ways besides just keywords.

## Installation

Install the library using pip:

```bash
pip install project_progress
```

## Usage

To use the Project Progress Tracking System:

1. Configure your email and Slack settings in the `emails.json` file.
2. Import the library into your Python script:

    ```python
    from project_progress import send_email, send_slack_notification
    ```

3. Use the `send_email` and `send_slack_notification` functions to send notifications:

    ```python
    send_email(subject="Task Update", message="The task is now complete.")
    send_slack_notification(text="The task is now complete.")
    ```

For more detailed usage instructions and available options, please refer to the [documentation](./documentation.md).
