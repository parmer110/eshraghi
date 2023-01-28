# Database Tool
#### Video Demo:  <URL HERE>
#### Description:
Abstract:
This software Healps implemention database table (Column and major values) With data encryption helps more and easily starting this as a base for programming helper.

TODO
* What will your software do? What features will it have? How will it be executed?
    <!-- - Database table creation and data entry afairs -->

    - Decrypted assigning table name, headers and cells.
    - UI abilities for add or delete columns and row.
    - Have alert for deleting table and column.
    - Auto submit (AJAX) some value changes, ne need page refreses.

    - Will executed in web browser. (This is a web application)


* What new skills will you need to acquire? What topics  will you need to research?
    - JavaScript
    - AJAX.
    - SQlite date fields.


* In the world of software, most everything takes longer to implement than you expect. And so it’s not uncommon to accomplish less in a fixed amount of time than you hope. What might you consider to be a good outcome for your project? A better outcome? The best outcome?


## Details:
0. The system files:
    * Root:
        - administration.db: The project database file.
        - app.py: The controler of project.
        - helper.py: some using functions:
            + login_required(): Detect is user loged in to application, thus let working.
            + hash_in(): Coding the input value in 62 base number.
            + hash_out(): Decode a hashed value to plain text.
            + query(): Generat the query string needed in db.execute()
        - README.md: Hi!
        - requirements.txt: the libraries are used in this project.
    * static:
        - Icons: are small pictures.
        - style.css: styling web pages.
        - PersonalPic3.jpg is using in the page title.
    * templates:
        - index.html: The home page.
        - loyout.html: The layout of my view pages.
        - login: Using for get username and password from user and define validation with database query.
        - settings.html: Main view of this project. Working on tables.

1. Define menus of the web application
    * initialize app.py, helper.py with login prototypes.
    * layout.html, index.html, login.html
2. Personel registrants
    * Create initial enterprise admin who has full access
3. I reached an idea for generate an interactive structure.
4. Create database tables.
    * Create enterprise admin user
5. Create pop up flash message.
6. Hold username and password in the field, when wrong input.
7. The question: [Clear web variables in refresh](https://stackoverflow.com/q/74994762/17473587).
8. Create index home page:

9. Create settings page:
    * Initialize
        - Setting definition
        - User groups definition
        - Programaticaly developement definition.
        - Crate table
        - submit form in case of choose an select item and remain
        - Cach table columns header
    * Create table
        - Working with Jinja if and increment variable
        - Load each choosen table values in a table
        - More search, learning and practice Bootstrap.
        - popup menus with form in popup flash upside setting logo (picture)
        - Input text for each column in nested table_setting form.
        - Page should contains single form to return values when each button submission.
        - Change mouse curser on setting logo to pointer.
        - Made each table cell be editable
            + Handle editable and label format
            + submit each changed value with POST method to the server with Javascript function. (Form: frm_secondary)
        - Analyse edited cells:
            + Updating headers, body and insert new row.
        - Add column feature
        - Javascript code ensuring user not saved changes.
        - Styling selected headers of cells using Bootstrap classes.
        - Structure logical name values for the Name attribute of the type text elements.
        - Analysis the above value, extract sub-values needed.
        - Definition the table's password fields in case of "password" in the column's title.
        - Finding password field set as if "password" string in column header. (No case sensitive.)
        - I need finding a technique which made program convert all sequence of characters to a number in base sixty two [a-zA-Z0-9] for ciber sequrity and avoid run-time errors which there is sense on _ character in input text name attributes. Will be write functions in helper.py
            + Learning assert command for error exception.
            + There is no limits for name attribute length.
            + hash_in() and hash_out() functions are generated. (convert 1114112 ord character codes to above 62 ones. it same sixty-two base number whitch all unicode will represented with 62 alphnumerics).
        - Many errors visited almost ("deprecationwarning: 'session_cookie_name' is deprecated and will be removed in flask 2.3. use 'session_cookie_name' in 'app.config' instead."), found setting: app.config["SESSION_COOKIE_NAME"] in the session configuration, thus I'm not sure, unknown the exact meaning.
            + Add try/ except block for setting function.
        - Update the requirements.txt.
        - Max length of the input text elements are setted with html attributes and data validation in app.py.
        - Not resolved BUG founds: The redirect and render_template functions not executing in the settings route while calling with the fetch AJAX which is in the first JavaScript function.
        - Create new table, Delete existing ones developement.
        - Created Message box in modal, with CSS specifications and front-end controling with Javascript in "Detete table" and "Delete column" using.
        - Using session variables for record situations between functions.
        - Implement flash message with Javascript.
        - Showing previous edition value on hover the cell. (headers and regular cells)
        - Tooltip hints in hover for showing initial data values after edition.
    * Create Table
    * Delete Table
        - Has modal message box control.
    * Create column
        - Adding new column with specifications.
    * Delete column
        - Delete column ability. (Assumed no relation and primary key)
        - Has modal message box control.
        - Encounter [Checking value is in a list of dictionary values in Jinja](https://stackoverflow.com/q/75150849/17473587)
    * Add row
        - Using query generator helper function, generate from dictionary of row input elements.
    * Delete rows
        - Remove of singlet, rows. Here the where Develepoment Idea:
            + Undelete feature by using a temporary table helper or using session to record deletion data history.
            + Many rows deletion with a checkbox in first data table column.
    * Edit table rows cell
        - Using AJAX data fetch in POST method.
    * Encryption-Dectiption implemention.
    * All previous data from system (Tables) and create new table-values which gets encryption-decryption for new values. There are advantages in wide of characters accessible and safety in cyber-sequrity.
        - The table names "user" is created for initialize and hoding owner user.
        - The second table which name is personnel was created.
    * Headers edition get locked for our initial base table which is "user"
    * Test and debuging.
    * Creating some descriptions in the home page, about this project.
    * Take safe the user table agains the owner user accessing problem. This table have assumed as using for system.
10. Working null values because of encryption method which is append an static value "sxtw" acronym of "Sexty Two" in the starting the string and each null value, here be represented with "sxtw" !

11. Descriptions are presented page:

    Database tables related with there type of varied. (Table name, columns name, values) As you know, there were 1,114,112 character codes in UNICODE system. We have provided ability for you using all 1114112 characters in this case. (No mather of using and sequene of using. e.g. You can create a table, witch name is space!)

    The program's database needs and contain main table which name is "user". users are not able to change most of it's specifications.

    This application is architectd case sensitive.

12. Table management:

    Click "Settings" link in above↑
    Note that the default username and password are same "admin" for owner as enterprise admin

13. Create Table:

    Enter table name
    Click on "Create" button

    Note that the table name can be null! but duplicated in database is forbided. Here we get mean to the Null value. We respect it!

14. Delete Table:

    Choose intended table name from drop-down menu
    Press "Delete" button

15. Create Column:

    Click on circled plus icon on right-side end of the table headers
    In the appeared menu, input desired column name in appropritated input box
    Choose the value type from the below drop-down menu
    Some optional items are there and has obvious meaning

16. Delete Column:

    Near right side each column header is there an setting icon
    Hear the datatype is visible. Choose the red "Delete" button.
    In the modal message box, choose the Delete button

17. Add empty row

    Add the end bottom of the table, there were an empty row. Pressing the rectangle plus icon in reft side, will register values.

18. Delete current row:

    At right end side of each row there were a cirtular negative icon. Note That pressing this key will remove respected row permanently and cant be undone

19. Edit desired values:

    Inpute velues in cells will auto register to the database after clicking outside of the cell, or pressing enter.