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

For details see https://nbdev.fast.ai/api/merge.html#nbdev_merge.
