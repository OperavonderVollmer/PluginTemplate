from abc import ABC, abstractmethod
from OperaPowerRelay import opr
from typing import Callable

class ophelia_plugin(ABC):
    """
    Abstract base class for plugins, standardizing the interface.

    Parameters
    ----------
    name : str
        The name of the plugin.
    prompt : str, optional
        The prompt to display to the user.
    description : str, optional
        A description of the plugin.
    needs_args : bool, optional
        Whether the plugin requires arguments.
    command_map : list, optional
        A dictionary of operational commands. Key = command, value = function.
    help_text : str, optional
        Additional help text for the plugin.
    access_level : int, optional
        A flag indicating the plugin's access level.
    git_repo : str, optional
        The GitHub repository URL for the plugin.

    Attributes
    ----------
    _meta : dict
        A dictionary containing metadata about the plugin.

    Methods
    -------
    prep_execute
        Orchestrates plugin execution by preparing user interaction and handling input/output.
    execute
        Executes the plugin.
    direct_execute
        Executes the plugin directly without user interaction.
    clean_up
        Performs cleanup tasks after executing the plugin.

    
    """
    def __init__(
            self, 
            name:               str, 
            prompt:             str = "", 
            description:        str = "", 
            needs_args:         bool = False, 
            command_map:        dict = None,    
            help_text:          str = "", 
            access_level:       int = 0,
            git_repo:           str = "",
        ):

        self._meta: dict = {
            "name":             name, 
            "prompt":           prompt, 
            "description":      description,
            "needs_args":       needs_args, 
            "command_map":      command_map or {}, 
            "help_text":        help_text, 
            "access_level":     access_level,
            "git_rep":          git_repo,
        }
    


    def prep_execute(self, input_callable: Callable = None, output_callable: Callable = None, *args, **kwargs) -> str | tuple[str, str] | None:  # type: ignore
        """
        Orchestrates plugin execution by preparing user interaction and handling input/output.

        This method determines whether the plugin requires arguments and manages both automated 
        (callable-based) and interactive (user-prompted) input collection. It optionally supports 
        output redirection through a provided callable.

        Parameters
        ----------
        input_callable : Callable, optional
            A function used to retrieve input programmatically. If provided, it is called with *args and **kwargs.
        output_callable : Callable, optional
            A function used to display or process the prompt output programmatically.
        *args : tuple
            Positional arguments passed to `input_callable`, if used.
        **kwargs : dict
            Keyword arguments passed to `input_callable`, if used.

        Returns
        -------
        str | tuple[str, str] | None
            - Returns a string if a single user input is required.
            - Returns a tuple of (input, mode) if the plugin defines operational modes.
            - Returns None if no input is needed, cancelled, or an error occurs.

        Behavior
        --------
        - Displays the plugin prompt either through `output_callable` or `opr.print_from`.
        - If the plugin requires arguments, retrieves user input via `input_callable` or interactively.
        - Detects operational modes embedded in the user input when applicable.
        - Gracefully handles interruptions (Ctrl+C) and input errors.

        """
        if output_callable:
            output_callable(self._meta["prompt"])
        elif self._meta["prompt"] and not self._meta["needs_args"]:
            opr.print_from(name=self._meta["name"], message=self._meta["prompt"], do_print=True)


        if self._meta["needs_args"]:

            if input_callable: return input_callable(*args, **kwargs)
            
            else:
                try:
                    user_input: str = ""
                    while True:
                        if self._meta["prompt"]: print(self._meta["prompt"])
                        user_input = opr.input_from(name=self._meta["name"], message="Input (Ctrl+C to cancel)", do_print=True)
                        
                        if self._meta["command_map"]:
                            for mode in self._meta["command_map"].keys():
                                if mode in user_input:
                                    find = user_input.replace(mode, "").strip()
                                    user_input = [find, mode]
                                    break
                            else: 
                                opr.print_from(name=self._meta["name"], message="Mode not found. Query cancelled", do_print=True)
                                return None

                        break

                    return user_input
                except KeyboardInterrupt:
                    return None
                except EOFError: # Helps against accidental returns
                    pass
                except Exception as e:
                    opr.error_pretty(exc=e, name=self._meta["name"], message=f"Error in input function\n{e}", level="ERROR")
                    pass

        return None

    def run_command(self, command: str, *args, **kwargs):

        """
        Executes a command associated with the plugin, if applicable.

        Parameters
        ----------
        command : str
            The command to be executed.

        *args : tuple
            Positional arguments passed to the command function, if applicable.

        **kwargs : dict
            Keyword arguments passed to the command function, if applicable.

        Returns
        -------
        any
            The result of the command function, if applicable. Otherwise, None.
        """

        if command in self._meta["command_map"]:
            return self._meta["command_map"][command](*args, **kwargs)

        return None


    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Performs the main execution logic for the plugin.
        """
        pass

    @abstractmethod
    def direct_execute(self, *args, **kwargs):
        """
        Directly executes plugin logic without user interaction. Used for automation and testing.
        """
        pass

    @abstractmethod
    def clean_up(self, *args, **kwargs):
        """
        Performs cleanup tasks after executing the plugin.
        """
        pass