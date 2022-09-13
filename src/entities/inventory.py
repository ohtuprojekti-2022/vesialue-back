class Inventory():
    """ Class that represents a single inventory. """

    def __init__(self, name, email, phonenumber, other):
        """ Class constructor. Creates a new inventory.
        Attributes:
            _name: [String] The name of the submitter.
            _email: [String] The email of the submitter.
            _phonenumber: [String] The phonenumber of the submitter.
            _other: [String] Other notes for the inventory.
        """

        self._name = name
        self._email = email
        self._phonenumber = phonenumber
        self._other = other

    def get_name(self):
        """ Gets the name of the inventory."""

        return self._name

    def get_email(self):
        """ Gets the email of the inventory."""

        return self._email

    def get_phonenumber(self):
        """ Gets the phonenumber of the inventory."""

        return self._phonenumber

    def get_other(self):
        """ Gets the other information of the inventory."""

        return self._other

    def set_name(self, name):
        """ Sets the name.
        Args:
            name: [String] The name to be set.
        """

        self._name = name

    def set_email(self, email):
        """ Sets the email.
        Args:
            email: [String] The email to be set.
        """

        self._email = email

    def set_phonenumber(self, phonenumber):
        """ Sets the phonenumber.
        Args:
            phonenumber: [String] The phonenumber to be set.
        """

        self._phonenumber = phonenumber

    def set_other(self, other):
        """ Sets the other information.
        Args:
            other: [String] The otherinformation to be set.
        """

        self._other = other
