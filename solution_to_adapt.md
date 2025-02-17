# 🪐 Enter the Dimension of Cloud Computing! 🚀

In the previous unit, you have **packaged** 📦 the notebook of the _EHEC_ Data Science team

☁️ In this unit, you will learn how to dispatch work to a pool of **cloud resources** instead of using your local machine.

💪 As you can (in theory) now access a machine with the RAM-size of your choice, we'll consider that you don't need any "chunk-by-chunk" logic anymore!

🎯 Today, you will refactor the previous unit's codebase and:
- Fetch all your environment variables from a single `.env` file instead of updating `params.py`
- Load the raw data from Le Wagon BigQuery in one go in memory (no chunks)
- Cache a local CSV copy to avoid querying the data twice
- Process the data
- Upload the processed data to your own BigQuery table
- Download the processed data (in one go)
- Cache a local CSV copy to avoid querying the data twice
- Train your model on this processed data
- Store the model weights on your own Google Cloud Storage (GCS) bucket

Then, you'll provision a Virtual Machine (VM) to run this whole workflow on the VM !

Congratulations, you just grew from a **Data Scientist** into a full **ML Engineer**!
You can now sell your big GPU-laptop and buy a lightweight computer like real ML practitioners 😝

---

<br>

# 1️⃣ New lyxury package setup

<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>


## Project Structure

👉 From now on, you will start each new challenge with the solution of the previous challenge.

👉 Each new challenge will bring in an additional set of features.

Here are the main files of interest:
```bash
.
├── .env                            # ⚙️ Single source of all config variables
├── .envrc                          # 🎬 .env automatic loader (used by direnv)
├── Makefile                        # New commands "run_train", "run_process", etc..
├── README.md
├── requirements.txt
├── setup.py
├── luxury-project
│   ├── __init__.py
│   ├── interface
│   │   └── main_local.py           # 🚪 (OLD) entry point
│   │   └── main.py                 # 🚪 (NEW) entry point: No more chunks 😇 - Just process(), train()
│   ├── ml_logic
│       ├── data.py                 # (UPDATED) Loading and storing data from/to BigQuery !
│       ├── registry.py             # (UPDATED) Loading and storing model weights from/to Cloud Storage!
│       ├── ...
│   ├── params.py                   # Simply load all .env variables into python objects
│   └── utils.py
└── tests
```


#### ⚙️ `.env.sample`

This file is a _template_ designed to help you create a `.env` file for each challenge. The `.env.sample` file contains the variables required by the code and expected in the `.env` file. 🚨 Keep in mind that the `.env` file **should never be tracked with Git** to avoid exposing its content, so we have added it to your `.gitignore`.

#### 🚪 `main.py`

Bye bye `luxury.interface.main_local` module, you served us well ❤️

Long live `luxury.interface.main`, our new package entry point ⭐️ to:

- `preprocess`: preprocess the data and store `data_processed`
- `train`: train on processed data and store model weights
- `evaluate`: evaluate the performance of the latest trained model on new data
- `pred`: make a prediction on a `DataFrame` with a specific version of the trained model


🚨 One main change in the code of the package is that we chose to delegate some of its work to dedicated modules in order to limit the size of the `main.py` file. The main changes concern:

- The project configuration: the single source of truth is `.env`
  - `.envrc` tells `direnv` to load the `.env` as environment variables
  - `params.py` then loads all these variable in python, and should not be changed manually anymore

- `registry.py`: the code evolved to store the trained model either locally or - _spoiler alert_ - in the cloud
  - Notice the new env variable `MODEL_TARGET` (`local` or `gcs`)

- `data.py` has refactored 2 methods that we'll use heavily in `main.py`
  - `get_data_with_cache()` (get some data from BigQuery or a cached CSV if exists)
  - `load_data_to_bq()` (upload some data to BQ)



## Setup

#### Install `luxury-project` version `0.0.7`

**💻 Install the new package version**
```bash
make reinstall_package # always check what make does in the Makefile
```

**🧪 Check the package version**
```bash
pip list | grep taxifare
# luxury              0.0.7
```

#### Setup direnv & .env

Our goal is to be able to configure the behavior of our _package_ 📦 depending on the value of the variables defined in a `.env` project configuration file.

**💻 In order to do so, we will install the `direnv` shell extension.** Its job is to locate the nearest `.env` file in the parent directory structure of the project and load its content into the environment.

``` bash
# MacOS
brew install direnv

# Ubuntu (Linux or Windows WSL2)
sudo apt update
sudo apt install -y direnv
```
Once `direnv` is installed, we need to tell `zsh` to load `direnv` whenever the shell starts

``` bash
code ~/.zshrc
```

Add `direnv` to the end of your list of plugins in your `.zshrc`
When you're done, it should look something like this:

``` bash
plugins=(git gitfast ... direnv)
```

Start a new `zsh` window in order to load `direnv`

**💻 At this point, `direnv` is still not able to load anything, as there is no `.env` file, so let's create one:**

- Duplicate the `env.sample` file and rename the duplicate as `.env`
- Enable the project configuration with `direnv allow .` (the `.` stands for _current directory_)

🧪 Check that `direnv` is able to read the environment variables from the `.env` file:

```bash
echo $DATA_SIZE
# 1k --> Let's keep it small!
```

From now on, every time you need to update the behavior of the project:
1. Edit `.env`, save it
2. Then
```bash
direnv reload . # to reload your env variables 🚨🚨
```

**☝️ You *will* forget that. Prove us wrong 😝**

```bash
# Ok so, for this unit, alway keep data size values small (good practice for dev purposes)
DATA_SIZE=1k
CHUNK_SIZE=200
```

</details>

# 2️⃣ GCP Setup

<details>
<summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>

**Google Cloud Platform** will allow you to allocate and use remote resources in the cloud. You can interact with it via:
- 🌐 [console.cloud.google.com](https://console.cloud.google.com)
- 💻 Command Line Tools
  - `gcloud`
  - `bq` (BigQuery - SQL)
  - `gsutils` (cloud storage - buckets)


### a) `gcloud` CLI

- Find the `gcloud` command that lists your own **GCP project ID**.
- 📝 Fill in the `GCP_PROJECT` variable in the `.env` project configuration with the ID of your GCP project
- 🧪 Run the tests with `make test_gcp_project`

<details>
  <summary markdown='span'><strong>💡 Hint </strong></summary>


  You can use the `-h` or the `--help` (more details) flags in order to get contextual help on the `gcloud` commands or sub-commands; use `gcloud billing -h` to get the `gcloud billing` sub-command's help, or `gcloud billing --help` for more detailed help.

  👉 Pressing `q` is usually the way to exit help mode if the command did not terminate itself (`Ctrl + C` also works)

  Also note that running `gcloud` without arguments lists all the available sub-commands by group.

</details>

### b) Cloud Storage (GCS) and the `gsutil` CLI

The second CLI tool that you will use often allows you to deal with files stored within **buckets** on Cloud Storage.

We'll use it to store large and unstructured data such as model weights :)

**💻 Create a bucket in your GCP account using `gsutil`**

- Make sure to create the bucket where you are located yourself (use `GCP_REGION` in the `.env`)
- Fill also the `BUCKET_NAME` variable with the name of your choice (must be globally unique and lower case! If you have an uppercase letter in your GitHub username, you'll need to make it lower case!)

e.g.
```bash
BUCKET_NAME = taxifare_<user.github_nickname>
```
- `direnv reload .` ;)

Tips: The CLI can interpolate `.env` variables by prefix them with a `$` sign (e.g. `$GCP_REGION`)
<details>
  <summary markdown='span'>🎁 Solution</summary>

```bash
# list buckets
gsutil ls

# make bucket
gsutil mb \
    -l $GCP_REGION \
    -p $GCP_PROJECT \
    gs://$BUCKET_NAME

# delete bucket
gsutil rm -r gs://$BUCKET_NAME
```
You can also use the [Cloud Storage console](https://console.cloud.google.com/storage/) to create a bucket or list the existing buckets and their content.

Do you see how much slower the GCP console (web interface) is compared to the command line?

</details>

**🧪 Run the tests with `make test_gcp_bucket`**

### c) BigQuery and the `bq` CLI

BiqQuery is a data warehouse, used to store structured data, that can be queried rapidly.

💡 To be more precise, BigQuery is an online massively-parallel **Analytical Database** (as opposed to **Transactional Database**)

- Data is stored by columns (as opposed to rows on PostgreSQL for instance)
- It's optimized for large transformations such as `group-by`, `join`, `where` etc.
- But it's not optimized for frequent row-by-row insert/delete

Ideally we should be using a managed PostgreSQL (e.g. [Google Cloud SQL](https://cloud.google.com/sql)) as its main production database on which its Django app is storing / reading hundred thousands of individual transactions per day!

Every night, (ideally) our project should launche a "database replication" job that applies the daily diffs of the "main" PostgresSQL into the "replica" BigQuery warehouse. Why?
- Because you don't want to run queries directly against your production-database! That could slow down your users.
- Because analysis is faster/cheaper on columnar databases.
- Because you also want to integrate other data in your warehouse to JOIN them (e.g marketing data from Google Ads, ...).

👉 Back to our business:

**💻 Let's create our own dataset where we'll store and query preprocessed data !**

- Using `bq` and the following env variables, create a new _dataset_ called `taxifare` on your own `GCP_PROJECT`

```bash
BQ_DATASET=taxifare
BQ_REGION=...
GCP_PROJECT=...
```

- Then add 3 new _tables_ `processed_1k`, `processed_200k`, `processed_all`

<details>
  <summary markdown='span'>💡 Hints</summary>

Although the `bq` command is part of the **Google Cloud SDK** , it does not seem to follow the same help pattern as the `gcloud` and `gsutil` commands.

Try running `bq` without arguments to list the available sub-commands.

What you are looking for is probably in the `mk` (make) section.
</details>

<details>
  <summary markdown='span'><strong>🎁 Solution </strong></summary>

``` bash
bq mk \
    --project_id $GCP_PROJECT \
    --data_location $BQ_REGION \
    $BQ_DATASET

bq mk --location=$GCP_REGION $BQ_DATASET.processed_1k
bq mk --location=$GCP_REGION $BQ_DATASET.processed_200k
bq mk --location=$GCP_REGION $BQ_DATASET.processed_all

bq show
bq show $BQ_DATASET
bq show $BQ_DATASET.processed_1k

```

</details>

**🧪 Run the tests with `make test_big_query`**


🎁 Look at `make reset_all_files` directive --> It resets all local files (csvs, models, ...) and data from bq tables and buckets, but preserves local folder structure, bq tables schema, and gsutil buckets.

Very useful to reset the state of your challenge if you are uncertain and you want to debug yourself!

👉 Run `make reset_all_files` safely now, it will remove files from unit 01 and make it clearer

👉 Run `make show_sources_all` to see that you're back from a blank state!


</details>

# 3️⃣ ⚙️ Train locally, with data on the cloud !

<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>

🎯 Your goal is to fill-up `luxury.interface.main` so that you can run all 4 routes _one by one_

```python
if __name__ == '__main__':
    # preprocess()
    # train()
    # evaluate()
    # pred()
```

To do so, you can either:

- 🥵 Uncomment the routes above, one after the other, and run `python -m luxury.interface.main` from your Terminal

- 😇 Smarter: use each of the following `make` commands that we created for you below

💡 Make sure to read each function docstring carefully
💡 Don't try to parallelize route completion. Fix them one after the other.
💡 You will also need to code the `load_data_to_bq()` function in `data.py`.
💡 Take time to read carefully the tracebacks, and add breakpoint() to your code or to the test itself (you are engineers now)!

**Preprocess**

💡 Feel free to refer back to `main_local.py` when needed! Some of the syntax can be re-used

```bash
# Call your preprocess()
make run_preprocess
# Then test this route, but with all combinations of states (.env, cached_csv or not)
make test_preprocess
```

**Train**

💡 Make sure to understand what happens when MODEL_TARGET = 'gcs' vs 'local'
💡 We advise you to set `verbose=0` on model training to shorten your logs!

```bash
make run_train
make test_train
```

**Evaluate**

Make sure to understand what happens when MODEL_TARGET = 'gcs' vs 'local'
```bash
make run_evaluate
make test_evaluate
```

**Pred**

This one is easy
```bash
make run_pred
make test_pred
```


🏁 Congrats for the heavy refactoring! You now have a very robust package that can be deployed in the cloud to be used with `DATA_SIZE='all'` 💪

</details>

# 4️⃣ Train in the Cloud with Virtual Machines


<details>
  <summary markdown='span'><strong>❓Instructions (expand me)</strong></summary>


## Enable the Compute Engine Service

In GCP, many services are not enabled by default. The service to activate in order to use _virtual machines_ is **Compute Engine**.

**❓How do you enable a GCP service?**

Find the `gcloud` command to enable a **service**.

<details>
  <summary markdown='span'>💡 Hints</summary>

[Enabling an API](https://cloud.google.com/endpoints/docs/openapi/enable-api#gcloud)
</details>

## Create your First Virtual Machine

The `luxury` package is ready to train on a machine in the cloud. Let's create our first *Virtual Machine* instance!

**❓Create a Virtual Machine**

Head over to the GCP console, specifically the [Compute Engine page](https://console.cloud.google.com/compute). The console will allow you to easily explore the available options. Make sure to create an **Ubuntu** instance (read the _how-to_ below and have a look at the _hint_ after it).

<details>
  <summary markdown='span'><strong> 🗺 How to configure your VM instance </strong></summary>


  Let's explore the options available. The top right of the interface gives you a monthly estimate of the cost for the selected parameters if the VM remains online all the time.

  The default options should be enough for what we want to do now, except for one: we want to choose the operating system that the VM instance will be running.

  Go to the **"Boot disk"** section, click on **"CHANGE"** at the bottom, change the **operating system** to **Ubuntu**, and select the latest **Ubuntu xx.xx LTS x86/64** (Long Term Support) version. (Do <u>not</u> pick a "Minimal" version: we would have to install too many tools manually.)

  Ubuntu is the [Linux distro](https://en.wikipedia.org/wiki/Linux_distribution) that will resemble the configuration on your machine the most, following the [Le Wagon setup](https://github.com/lewagon/data-setup). Whether you are on a Mac, using Windows WSL2 or on native Linux, selecting this option will allow you to play with a remote machine 
  using the commands you are already familiar with.
</details>

<details>
  <summary markdown='span'><strong>💡 Hint </strong></summary>

  In the future, when you know exactly what type of VM you want to create, you will be able to use the `gcloud compute instances` command if you want to do everything from the command line; for example:

  ``` bash
  INSTANCE=luxury-instance
  IMAGE_PROJECT=ubuntu-os-cloud
  IMAGE_FAMILY=ubuntu-2204-lts

  gcloud compute instances create $INSTANCE --image-project=$IMAGE_PROJECT --image-family=$IMAGE_FAMILY
  ```
</details>

**💻 Fill in the `INSTANCE` variable in the `.env` project configuration**


## Setup your VM

You have access to virtually unlimited computing power at your fingertips, ready to help with trainings or any other task you might think of.

**❓How do you connect to the VM?**

The GCP console allows you to connect to the VM instance through a web interface:

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-ssh.png" height="450" alt="gce vm ssh"></a><a href="https://wagon-public-datasets.s3.amazonaws.com/07-ML-Ops/02-Cloud-Training/GCE_SSH_in_browser.png"><img style="margin-left: 15px;" src="https://wagon-public-datasets.s3.amazonaws.com/07-ML-Ops/02-Cloud-Training/GCE_SSH_in_browser.png" height="450" alt="gce console ssh"></a>

You can disconnect by typing `exit` or closing the window.

A nice alternative is to connect to the virtual machine right from your command line 🤩

<a href="https://wagon-public-datasets.s3.amazonaws.com/07-ML-Ops/02-Cloud-Training/GCE_SSH_in_terminal.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/07-ML-Ops/02-Cloud-Training/GCE_SSH_in_terminal.png" height="450" alt="gce ssh"></a>

All you need to do is to `gcloud compute ssh` on a running instance and to run `exit` when you want to disconnect 🎉

``` bash
INSTANCE=luxury-instance

gcloud compute ssh $INSTANCE
```

<details>
  <summary markdown='span'><strong>💡 Error 22 </strong></summary>


  If you encounter a `port 22: Connection refused` error, just wait a little more for the VM instance to complete its startup.

  Just run `pwd` or `hostname` if you ever wonder on which machine you are running your commands.
</details>

**❓How do you setup the VM to run your python code?**


**💻 Connect to your VM instance and run the commands of the following sections**

<details>
  <summary markdown='span'><strong> ⚙️ <code>zsh</code> and <code>omz</code> (expand me)</strong></summary>

The **zsh** shell and its **Oh My Zsh** framework are the _CLI_ configuration you are already familiar with. When prompted, make sure to accept making `zsh` the default shell.

``` bash
sudo apt update
sudo apt install -y zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

👉 Now the _CLI_ of the remote machine starts to look a little more like the _CLI_ of your local machine
</details>

<details>
  <summary markdown='span'><strong> ⚙️ <code>pyenv</code> and <code>pyenv-virtualenv</code> (expand me)</strong></summary>

Clone the `pyenv` and `pyenv-virtualenv` repos on the VM:

``` bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
```

Open ~/.zshrc in a Terminal code editor:

``` bash
nano ~/.zshrc
```

Add `pyenv`, `ssh-agent` and `direnv` to the list of `zsh` plugins on the line with `plugins=(git)` in `~/.zshrc`: in the end, you should have `plugins=(git pyenv ssh-agent direnv)`. Then, exit and save (`Ctrl + X`, `Y`, `Enter`).

Make sure that the modifications were indeed saved:

``` bash
cat ~/.zshrc | grep "plugins="
```

Add the pyenv initialization script to your `~/.zprofile`:

``` bash
cat << EOF >> ~/.zprofile
export PYENV_ROOT="\$HOME/.pyenv"
export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init --path)"
EOF
```

👉 Now we are ready to install Python

</details>

<details>
  <summary markdown='span'><strong> ⚙️ <code>Python</code> (expand me)</strong></summary>

Add dependencies required to build Python:

``` bash
sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
python3-dev
```

ℹ️ If a window pops up to ask you which services to restart, just press *Enter*:

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-apt-services-restart.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-apt-services-restart.png" width="450" alt="gce apt services restart"></a>

Now we need to start a new user session so that the updates in `~/.zshrc` and `~/.zprofile` are taken into account. Run the command below 👇:

``` bash
zsh --login
```

Install the same python version that you use for the bootcamp, and create a `edhec` virtual env. This can take a while and look like it is stuck, but it is not:

``` bash
# e.g. with 3.10.6
pyenv install 3.10.6
pyenv global 3.10.6
pyenv virtualenv 3.10.6 luxury-env
pyenv global luxury-env
```

</details>

<details>
  <summary markdown='span'><strong> ⚙️ <code>git</code> authentication with GitHub (expand me)</strong></summary>

Copy your private key 🔑 to the _VM_ in order to allow it to access your GitHub account.

⚠️ Run this single command on your machine, not on the VM ⚠️

``` bash
INSTANCE=taxi-instance

# scp stands for secure copy (cp)
gcloud compute scp ~/.ssh/id_ed25519 $USER@$INSTANCE:~/.ssh/
```

⚠️ Then, resume running commands on the VM ⚠️

Register the key you just copied after starting `ssh-agent`:

``` bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Enter your *passphrase* if asked to.

👉 You are now able to interact with your **GitHub** account from the _virtual machine_
</details>

<details>
  <summary markdown='span'><strong> ⚙️ <em>Python</em> code authentication to GCP (expand me)</strong></summary>

The code of your package needs to be able to access your BigQuery data warehouse.

To do so, we will login to your account using the command below 👇

``` bash
gcloud auth application-default login
```

❗️ Note: In a full production environment we would create a service account applying the least privilege principle for the VM but this is the easiest approach for development.

Let's verify that your Python code can now access your GCP resources. First, install some packages:

``` bash
pip install -U pip
pip install google-cloud-storage
```

Then, [run Python code from the _CLI_](https://stackoverflow.com/questions/3987041/run-function-from-the-command-line). This should list your GCP buckets:

``` bash
python -c "from google.cloud import storage; \
    buckets = storage.Client().list_buckets(); \
    [print(b.name) for b in buckets]"
```

</details>

Your _VM_ is now fully operational with:
- A python virtualenv (taxifare-env) to run your code
- The credentials to connect to your _GitHub_ account
- The credentials to connect to your _GCP_ account

The only thing that is missing is the code of your project!

**🧪 Let's run a few tests inside your _VM Terminal_ before we install it:**

- Default shell is `/usr/bin/zsh`
    ```bash
    echo $SHELL
    ```
- Python version is `3.10.6`
    ```bash
    python --version
    ```
- Active GCP project is the same as `$GCP_PROJECT` in your `.env` file
    ```bash
    gcloud config list project
    ```

Your VM is now a data science beast 🔥

## Train in the Cloud

Let's run your first training in the cloud!

**❓How do you setup and run your project on the virtual machine?**

**💻 Clone your package, install its requirements**

<details>
  <summary markdown='span'><strong>💡 Hint </strong></summary>

You can copy your code to the VM by cloning your GitHub project with this syntax:

```bash
git clone git@github.com:<user.github_nickname>/data-train-in-the-cloud
```

Enter the directory of today's taxifare package (adapt the command):

``` bash
cd <path/to/the/package/model/dir>
```

Create directories to save the model and its parameters/metrics:

``` bash
make reset_local_files
```

Create a `.env` file with all required parameters to use your package:

``` bash
cp .env.sample .env
```

Fill in the content of the `.env` file (complete the missing values, change any values that are specific to your virtual machine):

``` bash
nano .env
```

Install `direnv` to load your `.env`:

``` bash
sudo apt update
sudo apt install -y direnv
```

ℹ️ If a window pops up to ask you which services to restart, just press *Enter*.

Reconnect (simulate a user reboot) so that `direnv` works:

``` bash
zsh --login
```

Allow your `.envrc`:

``` bash
direnv allow .
```

Install the luxury package (and all its dependencies)!

``` bash
pip install .
```

</details>

**🔥 Run the preprocessing and the training in the cloud 🔥**!

``` bash
make run_all
```

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-train-ssh.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-train-ssh.png" height="450" alt="gce train ssh"></a>

> `Project not set` error from GCP services? You can add a `GCLOUD_PROJECT` environment variable that should be the same as your `GCP_PROJECT`



**🏋🏽‍♂️ Go Big: re-run everything with `DATA_SIZE = 'all'` 🏋🏽‍♂️**!

**🏁 Switch OFF your VM to finish 🌒**

You can easily start and stop a VM instance from the GCP console, which allows you to see which instances are running.

<a href="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-start.png"><img src="https://wagon-public-datasets.s3.amazonaws.com/data-science-images/DE/gce-vm-start.png" height="450" alt="gce vm start"></a>

<details>
  <summary markdown='span'><strong>💡 Hint </strong></summary>

A faster way to start and stop your virtual machine is to use the command line. The commands still take some time to complete, but you do not have to navigate through the GCP console interface.

Have a look at the `gcloud compute instances` command in order to start, stop, or list your instances:

``` bash
INSTANCE=taxi-instance

gcloud compute instances stop $INSTANCE
gcloud compute instances list
gcloud compute instances start $INSTANCE
```
</details>

🚨 Computing power does not grow on trees 🌳, do not forget to switch the VM **off** whenever you stop using it! 💸

</details>

<br>


🏁 Remember: Switch OFF your VM with `gcloud compute instances stop $INSTANCE`
