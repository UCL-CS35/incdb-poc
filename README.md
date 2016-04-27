### Deploying INcDb

Install Virtual Environment using pip:

	pip install virtualenv

Cloning the app into a folder named "incdb-poc"

	git clone https://github.com/UCL-CS35/incdb-poc.git incdb-poc

Create the "incdb" virtual environment

	mkvirtualenv incdb

Install required Python packages

	cd /path/to/incdb-poc
	workon incdb
	pip install -r requirements.txt

### Installing AFNI + Nipype (Merging)

Before proceeding, it is important to note that the AFNI toolkit is currently incompatible on Windows. In order to test the merging process, the easiest suggestion is to install a Virtual Machine software (such as VirutalBox), install a free Linux distribution and run Neurosynth within the system.

#### AFNI

The AFNI toolkit consists of various functions to read and manipulate brain imaging data (in this case, merging). To install the AFNI tool kit, follow the link below:

* <https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/download_links.html>

Under section B, download the package for the relevant operating system you are running the kit from, and follow this link:

* <https://afni.nimh.nih.gov/pub/dist/doc/htmldoc/background_install/install_instructs/index.html>

For complete installation instructions. It also to note that this process will require modifying your system’s shell (BASH or tcsh) in order to run the AFNI toolkit within Terminal. If you have completed this process and are able to run the command ‘afni’ within the Terminal, continue to the next section.

#### Nipype

Nipype serves as a Python interface for many of AFNI’s functions (since it is not natively written in Python) in order to easily integrate the toolkit within Flask. To install nipype, run:

	pip install nipype

To install the Nipype package. Nipype also requires additional dependencies to be installed as described in the link below under the ‘Dependencies’ section

* <http://nipy.org/nipype/users/install.html>

You can test your Nipype installation using the command :
	
	python -c "import nipype; nipype.test()"

### Setting Up INcDb

Run Celery Work

	celery worker -A app.initializers.mycelery -l info

Run Redis Server
	
	redis-server

To install redis-server from source on Ubuntu, follow the tutorial by Digital Ocean, <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-redis/>

Initialising the Database

	# Setup Neruoysnth Dataset
	# Create DB tables and populate with Terms from Neurosynth
	# Populate the roles and users tables	
	python manage.py init_db

### Running the App
	
	# Start the Flask development web server
	./runserver.sh    # will run "python manage.py runserver"

Point your web browser to http://http://127.0.0.1:5000/

You can make use of the following users:

* email `jeremy@incdb.com` with password `Password1` with Administrative Privileges.
* email `ong@incdb.com` with password `Password1`.
* email `johnson@incdb.com` with password `Password1`.
* email `rajind@incdb.com` with password `Password1`.

### Testing the app

    # Run all the automated tests in the tests/ directory
    ./runtests.sh         # will run "py.test -s tests/"

### Known Issues

> Out of Memory during Installation of Python Packages

As `matplotlib` and `nilearn` both require a large memory space during installation, the remote server might run out of memory. One way to overcome this issue is to add Swap on the server. Swap is created from the hard drive space and used by the operating system to store data for a non-permanent basis when it run out memory in the RAM to hold the data.

If you face the Out of Memory issue, follow the tutorial by Digital Ocean to add Swap to your remote server. <https://www.digitalocean.com/community/tutorials/how-to-add-swap-on-ubuntu-14-04>

> Trouble installing SciPy and NumPy

Try installing the dependencies of `python-scipy` and `python-numpy` using the following command:
	
	sudo apt-get build-dep python-numpy python-scipy

### Troubleshooting

* If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.

* If you have any other troubles with setting up INcDb, tell us on the [Discussion Forum](http://students.cs.ucl.ac.uk/2015/group35/support/).
