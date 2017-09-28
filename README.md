# locked

`locked` is offline password manager with command-line interface.

Actually `locked` can securely store any text data you want. It's organized
in a dictionary-like manner: each value is saved under a key and a subkey.

## Installation

First, clone this repository:

```
$ git clone git@github.com:piotrekio/locked.git
```

Then install the package:

```
$ cd locked
$ python setup.py install
```

## Usage

You start by initializing the storage:

```
$ locked init
Enter password: 
Confirm password:
```

By default the storage will be saved in the current directory under `storage.locked`.
This can be changed by the `--storage-path` option.

Now you can set some values:

```
$ locked set github username example
Enter password: 
$ locked set github password
Enter password: 
Enter value:
```

Once you have some data in the storage, you can list the keys:

```
$ locked get 
Enter password: 
github
```

Or you can see all the subkeys and their values in plain text:

```
$ locked get github
Enter password: 
username: example
password: my_password
```

Finally, you can copy a value to the clipboard, which will be cleared
after 30 seconds:

```
$ locked get github password
Enter password: 
Value copied to clipboard. I will be removed in 30 seconds...
```

The time after which the clipboard will be cleared is configurable:

```
$ locked get github password --clear 5
Enter password: 
Value copied to clipboard. I will be removed in 5 seconds...
```
