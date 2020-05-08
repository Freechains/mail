# Freechains: Using an E-Mail Client

It's possible to use an e-mail client, such as Thunderbird, to interface with
Freechains.

We expect that all content sent to chain `/mail` uses these instructions.

You will need the following set of tools:

- Thunderbird: to read & write e-mails
- `send.py`: an SMTP server to intercept sends and redirect to a chain
- `recv.py`: a script to read a chain to a mailbox.

## Setup

- Thunderbird:
    - open Thunderbird
    - cancel account creation initial popup
    - click on `Set up an account: -> Movemail`
        - Identity
            - `Your Name: name`
            - `Email Address: name@localhost`
            - the `name` you choose is irrelevant
        - `Outgoing Serter: localhost`
        - `Account Name: Freechains`
    - right click on `Freechains` account
        - `Settings -> Outgoing Server (SMTP) -> Default -> Edit`
            - `Port: 2525`
    - configure `Inbox` to threaded display mode

- Local mailbox:

```
$ sudo touch /var/mail/<username>
$ sudo chown <username> /var/mail/<username>
$ sudo chmod 600 /var/mail/<username>
```

- `recv.py`:
    - edit the file and set variable `USER` to the same as `<username>` above

## Usage

First, start the SMTP server:

```
$ ./send.py
Type your private key to sign all messages: <...>
```

To receive e-mails, execute `recv.py` periodically:

```
$ ./recv
```

To send e-mails, always set `To` as `/mail@localhost`.
