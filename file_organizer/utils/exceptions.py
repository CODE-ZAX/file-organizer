"""
Custom exceptions for the file organizer
"""


class FileOrganizerError(Exception):
    """Base exception for file organizer errors"""
    pass


class ConfigurationError(FileOrganizerError):
    """Exception raised for configuration-related errors"""
    pass


class OrganizationError(FileOrganizerError):
    """Exception raised for file organization errors"""
    pass


class SchedulerError(FileOrganizerError):
    """Exception raised for scheduler-related errors"""
    pass


class ThemeError(FileOrganizerError):
    """Exception raised for theme-related errors"""
    pass


class ValidationError(FileOrganizerError):
    """Exception raised for validation errors"""
    pass
