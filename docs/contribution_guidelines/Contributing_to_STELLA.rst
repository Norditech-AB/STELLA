Contributing to STELLA
======================

Thank you for considering contributing to the STELLA project. Your contributions play a vital role in the continued growth and improvement of STELLA. We have a specific workflow involving two important branches that help us maintain the project's integrity and stability.

Important Branches
------------------

The STELLA repository contains two primary, protected branches:

1. **Main branch**: This is the stable branch that represents the production version of the project. It contains the latest released version of STELLA.

2. **Dev branch**: This is the development branch where active development occurs. It is always ahead of the main branch and contains new features and bug fixes that are not yet part of a stable release.

Contributing Workflow
---------------------

To contribute to STELLA, follow these steps:

1. **Branching**: Always create your feature or bugfix branch from the `dev` branch, as it reflects the most recent developments.

2. **Making Changes**:

   a. First, ensure you have the latest version of the `dev` branch:

   .. code-block:: shell

      git checkout dev
      git pull origin dev

   b. Create a new branch from `dev` where you will make your changes:

   .. code-block:: shell

      git checkout -b feature/your-feature-name

   .. note::

      for bug fixes, use the prefix `fix/` instead of `feature/`.

   Make sure to give your branch a meaningful name related to the feature or fix you are working on.

3. **Committing**: Commit your changes using clear, descriptive commit messages. Push your changes to the repository on GitHub.

.. code-block:: shell

   git add .
   git commit -m "Add a clear, descriptive message about your changes"
   git push origin feature/your-feature-name

4. **Creating a Pull Request (PR)**:

   a. Go to the `STELLA` repository on GitHub, and you will likely see a prompt to create a pull request from your new branch. If not, navigate to the 'Pull requests' tab and hit 'New pull request'.

   b. Set the base branch to `dev` and compare with your feature branch.

   c. Give your pull request a clear title and description of the changes you have made.

5. **Review Process**: Once you have created the pull request, it will be reviewed by the repository maintainers. Be receptive to feedback and make requested changes if necessary. If your pull request is deemed a serious and valid contribution, it will be approved and merged into the `dev` branch. Otherwise, you will receive comments and guidance.

6. **Merging to Main**: Periodically, the maintainers will merge changes from the `dev` branch into the `main` branch, marking a new stable release of STELLA.

By following these guidelines, you help ensure that STELLA remains a high-quality, stable project for everyone to use. We appreciate your contributions and look forward to seeing your great work!