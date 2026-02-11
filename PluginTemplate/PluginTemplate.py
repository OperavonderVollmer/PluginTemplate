from abc import ABC, abstractmethod
from OperaPowerRelay import opr
from typing import Callable
import os, sys
root = os.path.dirname(os.path.abspath(__file__))
if root not in sys.path:
    sys.path.insert(0, root)
import DSL
import socket, json, struct

class ophelia_plugin(ABC):
    """
    Abstract base class for plugins, standardizing the interface.

    Parameters
    ----------
    name : str
        The name of the plugin.
    description : str
        A description of the plugin.
    prompt : str, optional
        The prompt to display to the user.
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
    input_scheme
        Returns the input scheme for the plugin.

    
    """
    def __init__(
            self, 
            name:               str, 
            description:        str, 
            prompt:             str = "", 
            needs_args:         bool = False, 
            type_of_input:      str = "console",
            command_map:        dict = None,    
            quick_commands:     dict = None,
            help_text:          str = "", 
            access_level:       int = 0,
            git_repo:           str = "",
        ):

        self._meta: dict = {
            "name":             name, 
            "description":      description,
            "prompt":           prompt,  
            "needs_args":       needs_args,
            "type_of_input":    type_of_input,
            "command_map":      command_map or {}, 
            "quick_commands":   quick_commands or {},
            "help_text":        help_text, 
            "access_level":     access_level,
            "git_repo":         git_repo,
        }
    

    def input_scheme(self, root: DSL.JS_Container = None, form: bool = None, serialize: bool = False, effects: dict = {}, presets: dict = {}):
        """
        Returns the input scheme for the plugin.

        Parameters
        ----------
        serialize : bool, optional
            Whether to serialize the input scheme.

        Returns
        -------
        dict
            The input scheme for the plugin.
        """

        scheme = DSL.JS_Page(
            title= self._meta["name"],
            description= self._meta["description"],
            prompt= self._meta["prompt"],
            form= form or self._meta["needs_args"],
            root= root or DSL.JS_Div(
                id= "root",
                children= [
                    DSL.JS_Label(
                        id= f"{self._meta['name']}_no_children",
                        text= "No children",
                    )
                ]
            ),        
            effects= effects,
            presets= presets,
        )
        return scheme.serialize() if serialize else scheme


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

    def run_command(self, command: str=None, *args, **kwargs):

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
        commands = list(self._meta["command_map"].keys())

        opr.list_choices(choices=commands, title=f"Available commands for {self._meta['name']}")

        # If no command is pre-specified, ask user to select one
        if command is None:
            raw = opr.input_from(
                name=self._meta["name"],
                message=f"Select command (1 - {len(commands)}) or enter to cancel",
            )

            # Validate input
            try:
                choice = int(raw.strip())
                if not 1 <= choice <= len(commands) or raw == "":
                    raise ValueError
                command = commands[choice - 1]
            except ValueError as e:
                opr.print_from(self._meta["name"], message=f"{self._meta['name']} command cancelled")
                return None


        # Execute command if valid
        func = self._meta["command_map"].get(command)
        if func is None:
            opr.error_pretty(
                exc=None,
                name=self._meta["name"],
                message=f"Unknown command: {command}",
                level="INFO"
            )
            return None

        return func(*args, **kwargs)


    def execute(self, *args, **kwargs):
        """
        Performs the main execution logic for the plugin.
        """
        return self.run_command(*args, **kwargs)


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




class ophelia_envelope(ABC):

    def __init__(
            self,
            page_title: str,
            page_data: DSL.JS_Page,       
        ):
        self.page_title = page_title
        self.page_data = page_data

    def export(self) -> dict:
        return {
            "page_title": self.page_title,
            "data": self.page_data.serialize(),
        }


class ophelia_input():


    types = [
        "console",
        "browser",
        ]
    
    HUD_HOST = "127.0.0.1"
    HUD_PORT = 6990
    DEFAULT_BROWSER_PROMPT = DSL.JS_Page(
            title= "Input Required",
            description = "",
            prompt = "",
            form = True,
            root= DSL.JS_Div(
                id = "new-input-div",
                children=[
                    DSL.JS_TextBox(
                        id = "generic_input",
                        label = "Input",
                        hint = "Input Required",
                        type = "text",
                        ),
                    ]
                )
            )

    @classmethod
    def get_types(cls) -> list:
        return cls.types
    
    @classmethod
    def console_input(cls, **kwargs):
        """
        
        Retrieves user input from the console. 

        Parameters
        ----------
        prompt : str (default: None)
            The prompt message to display to the user.
        opr : bool (default: True)
            Whether to use opr.input_from (True) or input (False).


        Returns
        -------
        str
            The user's input.

        """


        answer = None
        if kwargs.get("prompt", None):
            
            if kwargs.get("opr", True):
                answer = opr.input_from(name=kwargs.get("name", "Input"), message=kwargs["prompt"])
            else:
                answer = input(kwargs["prompt"] + ": ")
        else:
            answer = input("Input: ")
        return answer

    @classmethod
    def browser_input(cls, **kwargs):

        """
        Retrieves user input from a web browser prompt.

        Parameters
        ----------
        prompt : DSL.JS_Page (default: None)
            The prompt message to display to the user.

        Returns
        -------
        dict
            Dictionary containing the user's input. The keys depend on the IDs defined in the DSL.JS_Page prompt.

        """

        answer = {}
        prompt = kwargs.get("prompt", cls.DEFAULT_BROWSER_PROMPT
        )
    

        payload_json = json.dumps(prompt.serialize())
        payload_bytes = payload_json.encode("utf-8")
        payload_size = len(payload_bytes)


        for attempt in range(1, 4):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5*60)  # 5 minutes timeout
                    sock.connect((cls.HUD_HOST, cls.HUD_PORT))
                    size_packed = struct.pack("!I", payload_size)
                    sock.sendall(size_packed + payload_bytes)

                    answer_bytes = sock.recv(8192)
                    answer_json = answer_bytes.decode("utf-8")
                    answer = json.loads(answer_json)
                    break
                
            except (ConnectionRefusedError, ConnectionResetError) as e:
                opr.error_pretty(
                    exc=e,
                    name="Plugin Input",
                    message=f"Connection with HUD failed. Attempt: {attempt}/3. Is the HUD running? - {e}",
                )
            except socket.gaierror as e:
                opr.error_pretty(
                    exc=e,
                    name="Plugin Input",
                    message=f"Invalid HUD host address. Attempt: {attempt}/3 - {e}",
                )
            except socket.timeout as e:
                opr.error_pretty(
                    exc=e,
                    name="Plugin Input",
                    message=f"Timed out, probably AFK. Breaking...",
                )
                break
            except Exception as e:
                opr.error_pretty(
                    exc=e,
                    name="Plugin Input",
                    message=f"An unexpected error occurred during HUD communication. Attempt: {attempt}/3 - {e}",
                )

        return answer

    @classmethod
    def input(cls, input_type: str = "console", **kwargs):
        """
        Parameters
        ----------

        type : str
            The type of input to request.

        **kwargs : dict
            Additional keyword arguments specific to the input type.

        Kwargs Scheme
        ------

        For "console" type:
            - prompt : str
                The prompt message to display to the user.
            - opr : bool
                Whether to use opr.input_from (True) or input (False).

        For "browser" type:
            - prompt : DSL.JS_Page
                A page to display to the user.

        """

        match input_type:
            case "console":
                return cls.console_input(**kwargs)
            case "browser":
                return cls.browser_input(**kwargs)
            case _:
                raise ValueError(f"Unhandled input type: {input_type}")

            
