About
=====
* This is a modified version of pip that integrates in-toto verification.
* It assumes that there is an outer package, containing the payload package and the files necessary for toto-verification. 
* If there is a failure during the toto-verification process, the installation is halted.

pip-toto installation
=====================
* First install in-toto as outlined in https://github.com/in-toto/in-toto/tree/develop/demo#download-and-setup-in-toto-on-nix-linux-os-x-  


```shell
# After installing in-toto, get pip-toto
git clone https://github.com/team-ferret/pip-toto.git

# Change into project root directory
cd pip-toto

# Install with pip in "develop mode"
# (we strongly recommend using Virtual Environments)
# http://docs.python-guide.org/en/latest/dev/virtualenvs/
pip install -e .

```

pip-toto options
===================
* The following options are now valid when using pip install
	* --toto-verify (layout) (layout-keys) 
		* EXAMPLE: pip install MyDemoProject3 --toto-verify root.layout alice.pub
	* --toto-default: (Assumes a default layout of "root.layout" and layout-key of "alice.pub")
		* EXAMPLE: pip install MyDemoProject3 --toto-default


Sample packages pip installable with pip-toto options
========================================================
* MyDemoProject3 (this installation should succeed if the pip-toto options are used)
* MyMaliciousProject (this installation should fail if the pip-toto options are used)
