"""
Test Cases for Account Model
"""
import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# =======================================================================
# Test: A dictionary is returned via .to_dict()
# Author: Ken Harvey
# Date: 2025-2-3
# Description: Ensure `to_dict()` correctly converts an account to a dictionary format.
# =======================================================================
def dictionary_version_of_account_is_a_dictionary():
    """Test that a dictionary is returned using .to_dict()

    We avoid ORM interaction by testing the Account object without
    uploading and downloading the object or its dictionary counterpart.
    """

    account_dict = Account(name="Ken H", email="kenh@xyz.com", role="user").to_dict()
    assert isinstance(account_dict, dict)

# =======================================================================
# Test: .to_dict() creates a dictionary with all of the fields that the Account object had
# Author: Ken Harvey
# Date: 2025-2-3
# Description: Verify that all expected fields are included in the dictionary.
# =======================================================================
def dictionary_version_of_account_has_all_account_fields():
    """Test that .to_dict() returns a dictionary with all the Account fields

    We avoid ORM interaction by testing the Account object without
    uploading and downloading the object or its dictionary counterpart.
    """

    account_dict = Account(name="Ken H", email="kenh@xyz.com", role="user").to_dict()
    list_of_dict_keys = list(account_dict.keys())
    for key in list_of_dict_keys:
        assert hasattr(account_dict, key)

# TODO 2: Test Invalid Email Input
# - Check that invalid emails (e.g., "not-an-email") raise a validation error.
# - Ensure accounts without an email cannot be created.

# ===========================
# Test: Test Invalid Email Input
# Author: Hardy Fenam
# Date: 2025-02-04
# Description: Ensure accounts without an email cannot be created.
# ===========================

def test_invalid_email_input():
    """Test that accounts without an email cannot be created"""
    account = Account(name="John Doe", email="", role="user")

    #attempt to create an account without email
    with pytest.raises(DataValidationError):
        account.validate_email()  #invalid email should raise an error

# TODO 3: Test Missing Required Fields
# - Ensure that creating an `Account()` without required fields raises an error.
# - Validate that missing fields trigger the correct exception.

# ===========================
# Test: Test Missing Required Fields
# Author: Michael Soffer
# Date: 2025-02-04
# Description: Validate that missing fields trigger the correct exception.
# ===========================

def test_missing_required_fields():
    """Test missing required fields for an account"""
    
    # Helper function for checking required fields
    def create_account_manual_check(name=None, email=None, role=None):
        account = Account(name=name, email=email, role=role)
        
        # Manually check for missing fields and raise validation error manually
        if not account.name or not account.email or not account.role:
            raise DataValidationError

    # Missing name
    with pytest.raises(DataValidationError):
        create_account_manual_check(email="missingname@example.com", role="user")

    # Missing email
    with pytest.raises(DataValidationError):
        create_account_manual_check(name="Missing Email", role="user")

    # Missing role
    with pytest.raises(DataValidationError):
        create_account_manual_check(name="Missing Role", email="missingrole@example.com")
    

# TODO 4: Test Positive Deposit
# - Ensure `deposit()` correctly increases the account balance.
# - Verify that depositing a positive amount updates the balance correctly.

# ===========================
# Test: Positive Deposit
# Author: Tanner Donovan
# Date: 2/5/2025
# Description: Tests positive deposit
# ===========================

def test_positive_deposit():
    """Test depositing a positive amount"""
    account = Account(name="Tanner", email="tannertdonovan@gmail.com", balance=25)
    account.deposit(75)

    assert account.balance == 100

# TODO 5: Test Deposit with Zero/Negative Values
# - Ensure `deposit()` raises an error for zero or negative amounts.
# - Verify that balance remains unchanged after an invalid deposit attempt.

# ===========================
# Test: Deposit with Zero/Negative Values Values
# Author: Kevin Ramos
# Date: 2025-02-03
# Description: Ensure that deposit rases a DataValidationError for a zero or negative deposit ensuring the balance remains unchanged.
# ===========================

def test_deposit_zero_negative():
    """Test deposit zero or negative to raise data validation error and leaves balance unchanged."""
    account = Account(name = "Kevin Ramos", email = "ramosk10@example.com", role = "user")
    account.balance = 100

    balance = account.balance
    
    # Test depositing 0
    with pytest.raises(DataValidationError):
        account.deposit(0)
    assert account.balance == balance, "Balance should be unchanged after depositing zero"

    # Test depositing a negative value
    with pytest.raises(DataValidationError):
        account.deposit(-1)
    assert account.balance == balance, "Balance stays the same after depositing negative amount"

# TODO 6: Test Valid Withdrawal
# - Ensure `withdraw()` correctly decreases the account balance.
# - Verify that withdrawals within available balance succeed.

# TODO 7: Test Withdrawal with Insufficient Funds
# - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
# - Verify that the balance remains unchanged after a failed withdrawal.

# ===========================
# Test: Test Withdrawal with Insufficient Funds
# Author: Adam Hamou
# Date: 2025-02-06
# Description: Ensure that the balance remains unchanged after a failed withdrawal.
# ===========================

def test_withdrawal_insufficient_funds():
    """Test withdrawal with insufficient funds"""
    account = Account(name="Adam", email="hamoua2@example.com", balance=100)
    balance = account.balance

    # Attempt to withdraw more than the available balance
    with pytest.raises(DataValidationError):
        account.withdraw(200)   # Withdrawal amount exceeds balance
    
    # Verify that the balance remains unchanged
    assert account.balance == balance, "Balance should remain unchanged after a failed withdrawal"


# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.

# ===========================
# Test: Test Password Hashing
# Author: Jayson Kirchand-Patel
# Date: 2025-02-03
# Description: Ensures passwords are stored as hashed values
# ===========================

def test_password_hashing():
    '''Test storing passwords as hashed values'''
    test_password = "password"
    account = Account()

    # Set password and verify it's not being stored as plaintext
    account.set_password(test_password)
    assert account.password_hash != test_password

    # Ensure password is successfully stored as hashed value
    assert account.check_password(test_password)

# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.

# ===========================
# Test: Test Deleting an Account
# Author: John Zaleschuk
# Date: 2025-02-04
# Description: Ensure that 'delete()' removes an account from the database.
# ===========================

def test_deleting_an_account():
    """Test deleting an account"""
    # Add a test account to database
    account = Account(name="John Test", email="johntest@test.com", role="user")
    db.session.add(account)
    db.session.commit()
    
    # Verify the account is in the database
    tempaccount = Account.query.filter_by(email="johntest@test.com")
    assert tempaccount is not None
    
    # Delete the account
    tempaccount.delete()
    
    # Check again for the account
    tempaccount = Account.query.filter_by(email="johntest@test.com")
    assert tempaccount is None


