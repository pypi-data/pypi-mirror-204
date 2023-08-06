# EntX-Py - Encrypt and Decrypt your python files!

EntXpy allows you to encrypt and decrypt your python files with the EntX library, with encrypted files requiring a password to run/decrypt. All encrypted files have the extension .entxpy.

## The FileClient object
To perform operations on a file, you must initialise a FileClient object, with the file path and the password you wish to use.

```
from entxpy import FileClient

path = "path to .py / .entxpy file"
password = "your password"

my_client = FileClient(password, path)
```

## Encrypting a .py file
```
from entxpy import FileClient

path = "path to .py/ file"
password = "your password"

my_client = FileClient(password, path)

my_client.pack()
```

## Decrypting a .entxpy file
```
from entxpy import FileClient

path = "path to entxpy file"
password = "your password"

my_client = FileClient(password, path)

my_client.unpack()
```

## Running a .py / .entxpy file
```
from entxpy import FileClient

path = "path to .py / .entxpy file"
password = "your password"

my_client = FileClient(password, path)

my_client.run()
```

## Exceptions:

### entxpy.errors.InvalidPath
Raised when the path provided does not lead to a valid file

### entxpy.errors.InvalidOperation
Raised when an operation is being performed on an incorrect file, i.e running FileClient.unpack() on a .py file.