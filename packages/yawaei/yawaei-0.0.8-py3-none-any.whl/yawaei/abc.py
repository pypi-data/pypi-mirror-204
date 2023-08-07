from abc import ABC, abstractmethod

class Intranet(ABC):
    """Interface of the communication between model and intranet

    :param token: Must be set before anything
    :type token: str
    """

    @abstractmethod
    async def get_current_scholar_year(self):
        """Get current Scolar year from the intranet
        """
        ...
    
    @abstractmethod
    async def get_students(self, promotions: str):
        """Get list of students of the given promotions

        :param promotions: Promotions code (Defined in constants.py)
        :type promotion: str
        :returns: Students or None in case of error
        :rtype: typing.Optional[list[str]]
        """
        ...

    @abstractmethod
    async def register_students(self, event: str, students: list[str]):
        """Register students to given event

        :param event: Epitech intranet url (format: 'event-xxxxxx')
        :type event: str
        :param students: Students to register.
        :type students: list[str]
        :returns: None on failure, the list of students registered on success
        :rtype: typing.Optional(list[str])
        """
        ...

    @abstractmethod
    async def create_event(self, activity: str, date: str, hour: str):
        """Create event at a given date for a given activity

        :param activity: Activity url under which to create event
        :type activity: str
        :param date: Date of the event to create (format 'YYYY-MM-DD')
        :type date: str
        :param hour: hour of the start of the event to create (format 'HH-MM-SS')
        :type hour: str
        :returns: A code of the created event
        :rtype: str
        """
        ...

    @abstractmethod
    async def get_events(self, activity: str, *, date: str = None, hour: str = None):
        """Get All events for a given activity
        
        :param activity: Activity url
        :type activity: str
        :param date: date of event to get (format: YYYY-MM-DD)
        :type date: typing.Optional(str)
        :param hour: hour of event to get (format: 00:00)
        :returns: Events code of the activity
        :rtype: list
        """
        ...

    @abstractmethod
    async def get_registered_students(self, event: str):
        """Get All students registered to the given event
        
        :param event: Event url
        :type event: str
        :returns: Registered students
        :rtye: list[dict]
        """
        ...

    @abstractmethod
    async def get_activities(self, year: str, codeModule: str, codeInstance: str):
        """Get Activities in a module given a code and an instance

        :param year: accademic year
        :type year: str
        :param codeModule: Code of the module
        :type codeModule: str
        :param codeInstance: Year instance (eg: LYN-0-1)
        :type codeInstance: str
        """
        ...
    
    @abstractmethod
    async def get_modules(self, year: str):
        """Get All modules for a year

        :param year: Accademic year
        :type year: str
        """
        ...
    
    @abstractmethod
    async def get_module(self, year: str, code: str, instance: str):
        """Get one module

        :param year: Accademic year
        :type year: str
        :param code: module code
        :type code: str
        :param instance: module instance
        :type instance: str
        """
        ...