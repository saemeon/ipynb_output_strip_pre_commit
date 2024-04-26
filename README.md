# Pre-commit hook to enforce empty notebook outputs and metadata.
## Using jupyter notebook pre-commit hook

The Jupyter Notebook pre-commit hook forces empty notebook cells and metadata on commits.
The nbconvert package is used to delete the notebook cells and metadata. Setting up nbconvert as a Git clean filter cleans the output cells and metadata only for the staging area, allowing outputs to be retained locally. However, outputs are still deleted when changes are pulled in.

To use the `ipynb-output-strip` and `check-ipynb-output-strip`
- add this to your requirements.txt:
  ```
  nbconvert
  gitpython
  nbdev
  ```
- add this to your .pre-commit-config.yaml:
  ```
  id: ipynb-output-strip
  ```
- add this to your .gitattributes
  ```
  *.ipynb filter=ipynb-output-strip
  ```
- add this to your .gitconfig
  ```
  [filter "ipynb-output-strip"]
      clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
  ```
Then, in order to include options from the .gitconfig file to the local git configuration options run the following command in the git repository root directory:
```
$ git config --local include.path ../.gitconfig
```
This command adds the following entry to your $GIT_DIR/config file, thus forcing it to include configuration options defined in the .gitconfig file:
```
[include]
	path = ../.gitconfig
```
Further, git breaks notebooks when resolving merge conflicts of notebooks. This problem can be solved by installing the `nbdev` package and changing the `.gitconfig` and `.gitattributes` in the following way:
- requirements.txt:
  ```
  nbconvert
  gitpython
  nbdev
  ```
- .gitattributes
  ```
  *.ipynb filter=ipynb-output-strip
  *.ipynb merge=nbdev-merge
  ```
- .gitconfig
  ```
  [filter "ipynb-output-strip"]
      clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
  [merge "nbdev-merge"]
      description = resolve conflicts with nbdev_fix
      driver = "nbdev_merge %O %A %B %P"
  ```

  Problems: 
Git projects ideally should not contain notebook outputs. How-to automatically clean notebook outputs before committing?
Merge conflicts of notebooks break the notebook s.t. they can no longer be opened. How-to adjust git merge to solve this problem (Details see https://nbdev.fast.ai/api/merge.html#nbdev_merge.)
Solution:

Set up local git repo to ...

automatically clean notebooks when "staging" (git add ...) a notebook, while still keeping the outputs in the working directory.
use a different git merge strategy to not break notebooks. 

The nbconvert package is used to delete the notebook cells and metadata. Setting up nbconvert as a Git clean filter cleans the output cells and metadata only for the staging area, allowing outputs to be retained locally. However, outputs are still deleted when changes are pulled in.

Step-by-step guide

1. Install (e.g. snb-pip install) the following packages in your virtual environment (and in your global python when using vscode GUI):

  nbconvert
  nbdev




2. Add a `.gitattributes` file in the root of your repo with the following content: 

  *.ipynb filter=ipynb-output-strip
  *.ipynb merge=nbdev-merge




3. Add a `.gitconfig` file in the root of your repo with the following content: 

  [filter "ipynb-output-strip"]
      clean = "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"
  [merge "nbdev-merge"]
      description = resolve conflicts with nbdev_fix
      driver = "nbdev_merge %O %A %B %P"




4. Run the following command in the git repository root to add the .gitconfig file to the local git configuration options:

 git config --local include.path ../.gitconfig



This command adds the following entry to your $GIT_DIR/config file, thus forcing it to include configuration options defined in the .gitconfig file:

[include]
    path = ../.gitconfig



 

For details see https://nbdev.fast.ai/api/merge.html#nbdev_merge.
