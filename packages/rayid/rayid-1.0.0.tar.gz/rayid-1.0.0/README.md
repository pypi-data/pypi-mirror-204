# RayID

**RayID** is a generated code that we use to track logs, posts or events. You can generate your own rayid, but we made your job easier!

In this instructure you will learn about how to use this package in your apps.

## Table of content

- [Languages](#languages)
- [Installation](#installation)
- [methods](#methods)
- [Development](#development)

## Languages

I created rayid for **JavaScript** too.

- [GitLab](https://gitlab.com/BlackIQ/rayid)
- [Npm](https://www.npmjs.com/package/rayid)

## Installation

How to install **RayID**? To install this package, use **pip** or **pipenv**.

```shell
$ pip3 install rayid
# Or
$ pipenv install rayid
```

## Config

So, import the package.

```python
from rayid import RayID

rayid = RayID("digit")
```

Now create your instance with what kind of rayid you want.

- digit: Numbers
- lower: Alphabet in lower case.
- upper: Alphabet in upper case.
- all: Combine of all types.

> No type means all combined togather.

```python
rayid = RayID("digit")
```

## Methods

Only one method! `gen(len)`.

### `gen(len)`

in **gen(len)** just say the length.

> There is no limit :)

```python
id = rayid.gen(25);
print(id); # 9514992619709220193874433
```

## Examples

Create common instances.

```python
all = RayID("all"); # All values
str = RayID("lower"); # Loercase generator
int = RayID("digit"); # Only int generator
```

Now use them:

```python
print(all.gen(10)); # Z*jVQ3c:+H
print(str.gen(10)); # ksixvpqohi
print(int.gen(10)); # 4748182066
```

All done!

---

## Development

If you want to develop the package, it is so simple. just follow steps below.

- Clone the project
- Start changing!

> Before you start: **Remember the base or code are stored in `rayid/rayid.py`**. You need to edit there.

### Cloning the project

To clone the project, you need to have git installed. Ok, now clone it same as command below.

```shell
$ git clone https:#github.com/BlackIQ/rayid
```

### Changing

To change package or anything, your need a testing environment to use linked package. Just change `rayid/rayid.py`.

#### Test

Your test app is linked. Change anything in package and test it in `test.py` file.
