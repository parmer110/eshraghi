import re
import os

from cs50 import SQL
from tempfile import mkdtemp
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

from helpers import login_required, hash_in, hash_out, query

# Configure application
app = Flask(__name__, static_folder='static', template_folder='templates')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_COOKIE_NAME"]
# app.config["SESSION_COOKIE_NAME"] = "SESSION_" + re.sub("[^a-zA-Z0-9_]", "_", "Administration")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db_admin = SQL("sqlite:///administration.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def home():
    user = db_admin.execute(f"SELECT * FROM ? WHERE {hash_in('user id')} = ?", hash_in('user'), session["user_id"])
    return render_template("index.html", user=hash_out(user[0][hash_in('username')]))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        user = request.form.get("username")
        password = request.form.get("password")

        # Validation
        if not user:
            return render_template("login.html", popUp="True", target1="flashPopup", pop_up_text="Please enter username!")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", popUp="True", target2="flashPopup", pop_up_text="Please enter password!", hold=user)

        # Query database for username
        rows = db_admin.execute(f"SELECT * FROM ? WHERE {hash_in('username')} = ?;", hash_in("user"), hash_in(user))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not hash_in(password) == rows[0][hash_in("password")]:
            return render_template("login.html", popUp="True", target1="flashPopup", pop_up_text="User of password was not found!")

        # Remember which user has logged in
        session["user_id"] = rows[0][hash_in("user id")]
        session["selected"] = ""

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    elif request.method == "GET":
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def setting():
    try:
        # Generate tables name are in the databalse
        tbls_name = db_admin.execute("""SELECT name FROM sqlite_master WHERE type='table';""")

        # Cooshen table from tables menu
        selected = request.args.get("table")

        if selected:
            # Generate the table's columns header
            tbl_headers = db_admin.execute("SELECT name, type FROM PRAGMA_TABLE_INFO(?);", selected)
            rows = db_admin.execute("SELECT * FROM ?;", selected)
            session["selected"] = selected
        elif session["selected"] != "False" and session["selected"] != "None" and session["selected"]:
            selected = session["selected"]
            tbl_headers = db_admin.execute("SELECT name, type FROM PRAGMA_TABLE_INFO(?);", selected)
            rows = db_admin.execute("SELECT * FROM ?;", selected)
        else:
            tbl_headers = ""
            rows = ""

        # Decryption
        # While input elements submitted with POST
        if request.method == "POST":

            # Edit cells

            # Count of Elements catched Form changed values are returned with AJAX in ImmutableMultiDict
            if len(list(request.form.to_dict())) == 1:

                # Name attribute of the changed element analysis↓
                # Key of changed element dictionary
                key = (list(request.form.to_dict().keys())[0])

                # Value of changed element dictionary
                value = (list(request.form.to_dict().values())[0])

                # Table name, header and index of changed element
                u1 = 0
                u2 = 0
                u3 = 0
                u4 = 0
                u5 = 0
                for i in range(1, len(key), 1):
                    if key[i] == '_':
                        if u1 == 0:
                            u1 = i
                        elif u2 == 0:
                            u2 = i
                        elif u3 == 0:
                            u3 = i
                        elif u4 == 0:
                            u4 = i
                        elif u5 == 0:
                            u5 = i
                # Table name of changed element
                table = key[u1 + 1: u2]
                # Column name of changed element
                header = key[u2 + 1: u3]
                # Overal Index of changed element
                index_overal = key[u3 + 1: u4]
                # Index number of changed element
                index = key[u4 + 1: u5]
                # First header of changed element
                first_header = key[u5 + 1:]
                # Type of changed element
                type = key[0: 3]

                # The key name of hdr or edt or add checking
                match type:
                    # Edit Header
                    case "hdr":
                        # Max length value validation check.
                        if len(value) > 30:
                            flash("Error! Header title max length is 30 characters", "error")
                            return redirect("/settings")  # Because AJAX post fetching, Not working!
                        if hash_in(str(value)) in [d['name'] for d in tbl_headers]:
                            flash("Error! For new header, this name was exist.", "error")
                            return redirect("/settings")  # Because AJAX post fetching, Not working!
                        db_admin.execute("ALTER TABLE ? RENAME COLUMN ? TO ?;", table, header, hash_in(str(value)))
                    # Edit table cells value
                    case "edt":
                        db_admin.execute(f"UPDATE ? SET ? = ? WHERE {first_header} = ?;", table, header, hash_in(str(value)), index)
                    case _:
                        print("Exception! Not defined execution.")

            # Add column
            if "create" in request.form:
                data = hash_out(request.form.get("hidden"))
                type = data[0: 3]
                if type == "had":
                    # Table name
                    table = data[4:]
                    # Column specifications
                    # Column name
                    c_name = request.form.get("input")
                    if not c_name:
                        flash("Error! New column name not defind.")
                        return redirect(url_for("setting"))
                    if hash_in(c_name) in [d['name'] for d in tbl_headers]:
                        flash("Error! For new header, this name was exist.", "error")
                        return redirect(url_for("setting"))
                    # Column data-type
                    d_type = request.form.get("select")
                    if not d_type:
                        flash("Error! New column datatype not defined!")
                        return redirect(url_for("setting"))
                    # Column NOT NULL specification
                    entry = request.form.get("entry")
                    if not entry:
                        entry = None
                    # Column values should uniqe rule.
                    valid = request.form.get("valid")
                    # Default value specification.
                    default = request.form.get("default")
                    if default:
                        default = "DEFAULT " + str(default)
                    # Query execution.
                    db_admin.execute(query("add_c", table, hash_in(c_name), d_type, entry, valid, default))
                    return redirect(url_for('setting'))

            # Add row
            found = False
            row = request.form.to_dict()
            # Is row values?
            for key in row.keys():
                if "img_add_" + selected in key:
                    found = True
                    break
            if found:
                # Generate valid data dictionary to add
                i = 0
                vpdel = []  # Value-pairs should be delete
                for key in row:
                    if key[: 4 + len(selected)] != "add_" + selected:
                        vpdel.append(key)
                    else:
                        i += 1
                        if i == 1:
                            vpdel.append(key)
                for vp in vpdel:
                    del row[vp]
                row = {k: hash_in(v) for k, v in row.items()}
                # Take query
                if row:
                    q = query("add_r", selected, row)
                    # Execute query
                    db_admin.execute(q)
                # Render the page again
                return redirect(url_for("setting"))

            # Delete row
            found = False
            row = request.form.to_dict()
            # Is row values?
            for key in row.keys():
                if "imgdel_" + selected in key:
                    found = True
                    break
            if found:
                u1 = 0
                u2 = 0
                u3 = 0
                u4 = 0
                key = list(request.form.to_dict())[0]
                for i in range(1, len(key), 1):
                    if key[i] == "_":
                        if u1 == 0:
                            u1 = i
                        elif u2 == 0:
                            u2 = i
                        elif u3 == 0:
                            u3 = i
                        elif u4 == 0:
                            u4 = i
                # Table
                table = key[u1 + 1: u2]
                # First Header
                header = key[u2 + 1: u3]
                # Row Index
                index = key[u3 + 1: u4]
                # Query execution
                db_admin.execute(f"DELETE FROM ? WHERE {header} = ?;", table, index)
                return redirect(url_for("setting"))

            # Modal Message Box
            if request.form.get("mmb_delete"):
                match request.form.get("mmb_action"):
                    # Delete Columnew
                    case "hdrdlt":
                        table = request.form.get("mmb_table")
                        header = request.form.get("mmb_header")
                        db_admin.execute("ALTER TABLE ? DROP COLUMN ?;", table, header)
                        return redirect(url_for('setting'))
                    # Delete Table
                    case "tbldlt":
                        table = request.form.get("mmb_table")
                        db_admin.execute("DROP TABLE ?;", table)
                        session["selected"] = "False"
                        return redirect(url_for('setting'))
            # End of POST method↑↑

        # GET method↓↓
        # Create new table
        if "tblcreate" in request.args:
            table_name = hash_in(request.args.get("add_table"))
            if not table_name:
                flash("Error in table creation! Please enter Table name.", "error")
                return redirect(url_for("setting"))
            if table_name in [d['name'] for d in tbls_name]:
                flash("Error in table creation! This table name is exist! Please enter unique one.", "error")
                return redirect(url_for("setting"))
            db_admin.execute("CREATE TABLE IF NOT EXISTS ? (id INTEGER PRIMARY KEY);", table_name)
            session["selected"] = table_name
            return redirect(url_for("setting"))

        user = db_admin.execute(f"SELECT * FROM ? WHERE {hash_in('user id')} = ?", hash_in('user'), session["user_id"])
        return render_template("settings.html", tbls_name=tbls_name, selected=selected, tbl_headers=tbl_headers, rows=rows, hash_out=hash_out,
                               user=hash_out(user[0][hash_in('username')]))
    except:
        print("Settings error happens!")
        flash("Error:Settings error!       ••• Call \"parmer_110@yahoo.com\"")
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
