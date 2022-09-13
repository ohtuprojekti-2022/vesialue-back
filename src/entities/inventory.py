class Inventory():
    """ Class that represents a single inventory. """

    def __init__(self, name, email, phonenumber, coordinates, time, methods, attachments, other):
        """ Class constructor. Creates a new inventory.
        Attributes:
            _name: [String] The name of the submitter.
            _email: [String] The email of the submitter.
            _phonenumber: [String] The phonenumber of the submitter.
            _coordinates: [String] Coordinates of the inventory area.
            _time: [String] Time of the inventory.
            _methods: [String] Type of methods used in the inventory.
            _attachments: [boolean] True if there are attachments included.
            _other: [String] Other notes for the inventory.
        """

        self._name = name
        self._email = email
        self._phonenumber = phonenumber
        self._coordinates = coordinates
        self._time = time
        self._methods = methods
        self._attachments = attachments
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

    def get_coordinates(self):
        """ Gets the coordinates of the inventory."""

        return self._coordinates

    def get_time(self):
        """ Gets the time of the inventory."""

        return self._time

    def get_methods(self):
        """ Gets the methods of the inventory."""

        return self._methods

    def get_attachments(self):
        """ Gets the attachments of the inventory."""

        return self._attachments

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

    def set_coordinates(self, coordinates):
        """ Sets the coordinates.
        Args:
            coordinates: [String] The coordinates to be set.
        """

        self._coordinates = coordinates

    def set_time(self, time):
        """ Sets the time.
        Args:
            time: [String] The time to be set.
        """

        self._time = time

    def set_methods(self, methods):
        """ Sets the methods.
        Args:
            methods: [String] The methods to be set.
        """

        self._methods = methods

    def set_attachments(self, attachments):
        """ Sets the attachments.
        Args:
            attachments: [boolean] The attachments to be set.
        """

        self._attachments = attachments

    def set_other(self, other):
        """ Sets the other information.
        Args:
            other: [String] The other information to be set.
        """

        self._other = other
