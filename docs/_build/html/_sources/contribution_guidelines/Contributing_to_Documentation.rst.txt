Contributing to Documentation
=============================

Introduction
------------
Contributions to the documentation are vital to ensuring that the information remains up-to-date, accurate, and helpful for users and developers. This section provides guidelines for contributing to our project's documentation.

Getting Started
---------------
Before you start, ensure you're familiar with our documentation structure and standards. Familiarize yourself with reStructuredText (`.rst`) format, as it is the primary format used in our documentation.

Writing Guidelines
------------------
1. **Clarity and Conciseness**: Write in a clear and concise manner. Avoid jargon and complex language to ensure the documentation is accessible to users of all levels.

2. **Consistency**: Follow the existing format, style, and tone of the documentation. This includes adhering to the structure of headings, code blocks, and naming conventions.

3. **Accuracy**: Ensure all technical details are correct. Double-check command examples, URLs, and configuration settings.

4. **Relevance**: Only include information that is relevant to the topic at hand. Avoid unnecessary details that may confuse the reader.

5. **Code Examples**: Where applicable, include code examples. Ensure these examples are tested and functional.

Git Workflow Guidelines
------------------------

1. **Create a Branch from `gh-pages`**:
   - Start by creating a new branch from the `gh-pages` branch. This ensures that you are working with the latest version of the documentation.
   - Use a descriptive name for your branch that reflects the changes you are making.

2. **Write Documentation in reStructuredText Format**:
   - Write your documentation using reStructuredText (`.rst`) format. Ensure it follows our writing guidelines mentioned earlier.

3. **Test Your Changes**:
   - After writing or updating the documentation, test your changes locally by following these steps:

   For Windows:
       1. Run `cleanup.bat` to clean up any previous builds.
       2. Navigate to the `docs` directory with `cd docs`.
       3. Build the documentation using `make html`.
       4. Copy the built HTML files to the root directory using `xcopy _build\\html\\* ..\\ /E /I`.
       5. Open the `index.html` file in a web browser to view the changes.

   For Mac/Unix:
       1. Run `./cleanup.sh` to clean up any previous builds.
       2. Navigate to the `docs` directory.
       3. Build the documentation using `make html`.
       4. Copy the built HTML files to the root directory using `$ cp -r _build/html/* ../`.
       5. Open the `index.html` file in a web browser to view the changes.

   - Ensure that all changes render correctly and that there are no formatting errors.

4. **Create a Pull Request**:
   - Once you have tested your changes, commit them to your branch. Push the branch to the repository and create a pull request against the `gh-pages` branch.
   - In your pull request description, provide a clear and comprehensive summary of the changes you have made.

Review Process
--------------
All documentation contributions undergo a review process. When you submit a change, it will be reviewed by a member of our team. Feedback or requests for changes should be addressed to allow updates to the documentation.

Submission
----------
Submit your documentation changes via a pull request to the appropriate repository. Ensure you provide a clear and descriptive commit message that outlines the changes and the reasons for them.

Questions and Assistance
------------------------
If you have questions or need help while contributing to the documentation, please reach out to our team through [discord?].