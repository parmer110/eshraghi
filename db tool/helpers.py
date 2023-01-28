import os
import re
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

# Check if user was loged in, else redirect to login page


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Generate hash value from plain-text


def hash_in(plain):
    # if not plain: # Alternate: After implemention this will alter from.
    # return
    result = ""
    for s in str(plain):

        unicode = ord(s)
        quotient = unicode

        for i in range(4):
            reminder = quotient % 62
            digit = str(dec_to_62(reminder))
            result = digit + result
            quotient //= 62

    return "sxtw" + result

# Generate plain-text from hash value


def hash_out(hash):
    result = ""
    hash = str(hash)
    if hash[0: 4] == "sxtw" and len(hash) % 4 == 0:
        hash = hash[4:]
        for i in range(0, len(hash), 4):
            digit = hash[i: i + 4]
            result = chr(dec_from_62(digit)) + result
    else:
        return hash

    return result


# Convert decimal value of chr's ord to 62base digit
def dec_to_62(dec):
    # 1114111
    # try:
    # Data validation
    # assert (not dec.isdigit()), "helpers.dec_to_62: Must enter 10base digits"
    # assert (dec < 0 or dec > 61), "helpers.dec_to_62: Value must between 0 and 61"

    dec = int(dec)
    # Conversion
    if dec < 10:
        return chr(dec + 48)
    elif dec < 36:
        return chr(dec + 55)
    else:
        return chr(dec + 61)
#    except Exception as e:
#        print (e)


# Convert 62base digit to decimal value of chr's ord()
def dec_from_62(hash):
    # Assert len(hash) != 4, "Input string should be 4 characters length represents a plain digit"
    hash = str(hash)[:: -1]
    result = 0
    for i in range(0, 4):
        digit = hash[i: i + 1]
        if digit < 'A':
            result += (ord(digit) - 48) * 62 ** i
        elif digit < 'a':
            result += (ord(digit) - 55) * 62 ** i
        else:
            result += (ord(digit) - 61) * 62 ** i
    return result


def query(model, table, *argv):
    # Models:
    # add_c: Add column
    # add_r: Add row
    match model:
        case "add_c":
            query = f"ALTER TABLE {table} ADD"
            for arg in argv:
                if not arg:
                    continue
                query += f" \"{arg}\""
            return query + ";"
        case "add_r":
            query1 = f"INSERT INTO {table} ("
            query2 = f" VALUES ("
            for key, value in argv[0].items():
                query1 += f"\"{key[4 + len(table) + 1 : ]}\", "
                query2 += f"\"{value}\", "
            query1 = query1[: len(query1) - 2] + ")"
            query2 = query2[: len(query2) - 2] + ")"
            return query1 + query2 + ";"
        case _:
            return
