# How to Create a Pull Request

## 1. Create and Name a New Branch

First, you need a new branch for your changes. In your code editor, click on your current branch name (e.g., "main") in the bottom-left corner.

![Clicking the current branch name](howto/1.png)

From the menu that appears, select the option to create a new branch. Make sure you are branching off of `main`.

![Selecting 'Create new branch' from the menu](howto/2.png)

Now, give your branch a descriptive name. A good convention is `feature/` or `fix/` followed by a short description.
For example: `fix/play-button-bug`.

![Entering a descriptive branch name](howto/3.png)

![New branch created](howto/4.png)

---

## 2. Make Your Changes

With your new branch checked out, you can now safely make your code changes. Add, edit, and delete files as needed to implement your feature or fix.

![Screenshot of code being edited](howto/5.png)

---

## 3. Commit and Push Your Branch

Once you are happy with your changes, commit them with a clear message. After committing, push your new branch up to the remote repository (e.g., GitHub).

![Screenshot of committing and pushing changes in the source control panel](howto/6.png)

> **Note:** If Git prompts you about setting an "upstream" branch, just follow the instructions it provides in the terminal or your editor. This is usually a one-time command to link your local branch to the remote one.

---

## 4. Open the Pull Request on GitHub

Go to your repository's main page on GitHub. You should see a yellow banner appear for your recently pushed branch. Click the **"Compare & pull request"** button.

![Screenshot of the 'Compare & pull request' button on GitHub](howto/7.png)

---

## 5. Fill Out the Pull Request Form

Give your pull request a clear title and write a description of the changes you made. This helps your teammates understand what you did and why. When you're ready, click **"Create pull request."**

![Screenshot of the 'Open a pull request' form on GitHub](howto/8.png)

---

## 6. Done!

That's it! Your pull request is now open. Your team can review your changes, leave comments, and, once it's approved, merge your code into the `main` branch.

![Screenshot of a completed pull request on GitHub](howto/9.png)