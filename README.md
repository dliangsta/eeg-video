# Installs

Here are the instructions to get Rekall set up on Nero.
You can create your own environment, or start from the environment in
`/share/pi/cleemess/envs/rekall`, but you'll need to run some install commands
either way (`conda` doesn't correctly save Javascript installs).

If you want to start from scratch, start in the next section.
Otherwise, skip down to Javascript installs.

## Starting from scratch

When you create a new environment, create it with Python 3.7 and anaconda:

```
conda create -p [PATH] python=3.7 anaconda
source activate [PATH]
```

Once you have the environment activated, install the following Conda packages
(note that some packages require mirrors):

```
conda install nodejs -c https://nero-mirror.stanford.edu/conda/conda-forge
conda install nb_conda
```

Install the following `pip` packages:

```
pip install pytest-runner
pip install rekallpy
pip install vgridpy
pip install vgrid_jupyter
```

Next, follow the instructions in the next section.

## Javascript installs

Run these commands from within your conda environment, *from this folder* (the
Javascript packages will be installed locally).

```
npm install --save @wcrichto/rekall
npm install --save react react-dom mobx mobx-react
npm install --save @wcrichto/vgrid
jupyter nbextension enable --py --sys-prefix vgrid_jupyter
```

# Running the Jupyter notebooks

To run the Jupyter notebooks, you need two servers running:
* HTTP server to serve videos
* Jupyter notebook server

Anecdotally, the [NPM http-server](https://www.npmjs.com/package/http-server)
works best.

## HTTP server

To run the HTTP server, activate your Conda environment and run the
following (from this directory):

```
npm install http-server -g
srun run_http_server.sh
```

You can also run the `run_http_server.sh` script (without srun) in a `tmux`
session should work too.

Pay attention to the output of the script; mine looks something like this:
```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.1.86.251	nero-login-1

# Entries added by HostAliases.
127.0.0.1	nero-login-1.stanford.edu
Starting up http-server, serving ./
Available on:
  http://127.0.0.1:8080
  http://10.1.86.251:8080
Hit CTRL-C to stop the server
```

Notice the line `10.1.86.251 nero-login-1` -- you'll need this IP address.

From your host machine, SSH into Nero with port forwarding:

```
ssh -L8080:10.1.86.251:8080 [USERNAME]@nero.compute.stanford.edu
```

*Except replacing the IP address with the one from the output of your script.*

Next get the Jupyter server running (similar process).

## Jupyter server

Run the following:

```
srun run_jupyter_server.sh
```

Again, you can also run the script directly in a `tmux` environment without
`srun`.

Again, pay attention to the output of the script; mine looks something like
this:
```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.1.86.251	nero-login-1

# Entries added by HostAliases.
127.0.0.1	nero-login-1.stanford.edu
[I 08:23:42.630 NotebookApp] [nb_conda_kernels] enabled, 19 kernels found
[I 08:23:43.727 NotebookApp] JupyterLab extension loaded from /share/pi/cleemess/envs/rekall/lib/python3.7/site-packages/jupyterlab
[I 08:23:43.727 NotebookApp] JupyterLab application directory is /share/pi/cleemess/envs/rekall/share/jupyter/lab
[I 08:23:43.732 NotebookApp] [nb_conda] enabled
[I 08:23:43.732 NotebookApp] Serving notebooks from local directory: /
[I 08:23:43.732 NotebookApp] The Jupyter Notebook is running at:
[I 08:23:43.733 NotebookApp] http://(nero-login-1.stanford.edu or 127.0.0.1):8888/?token=0e697c4ad80c9e3face1cb2cd22efa2f28209dff9f4722f0
[I 08:23:43.733 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 08:23:43.739 NotebookApp] No web browser found: could not locate runnable browser.
[C 08:23:43.739 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/danfu/.local/share/jupyter/runtime/nbserver-249435-open.html
    Or copy and paste one of these URLs:
        http://(nero-login-1.stanford.edu or 127.0.0.1):8888/?token=0e697c4ad80c9e3face1cb2cd22efa2f28209dff9f4722f0
```

Again, notice the line `10.1.86.251 nero-login-1` -- you'll need this IP
address.
Also pay attention to the port your Jupyter notebook is running on (second port
number in the port forwarding command).

Again, from your host machine, SSH into Nero with port forwarding:

```
ssh -L8888:10.1.86.251:8888 [USERNAME]@nero.compute.stanford.edu
```

Then navigate to `localhost:8888` on your host machine and take a look at the
Jupyter notebooks!
