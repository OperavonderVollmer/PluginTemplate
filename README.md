# 🧩 Ophelia Plugin Template

An **abstract base class** defining the standardized interface for all plugins in the Ophelia suite.  

***This class cannot run by itself.***

---

## ⚙️ Overview

The `OpheliaTemplate` class serves as the foundation for all plugins used by the Ophelia system.  
It defines required metadata, enforces structure, and provides helper methods for user interaction, execution, and error handling.

All plugin metadata is accessible via the internal dictionary:

```python
self._meta = {
    "name": str,
    "prompt": str,
    "description": str,
    "needs_args": bool,
<<<<<<< HEAD
    "commands": list[str],
=======
    "modes": list[str],
>>>>>>> 6c77bdb93c75ccbe6784fb4f554a40c852d74b31
    "help_text": str,
    "dev_only": bool,
    "git_repo": str
}
```

## Parameters

| Name            | Type        | Description                                                                            |
| --------------- | ----------- | -------------------------------------------------------------------------------------- |
| **name**        | `str`       | The identifier of the plugin.                                                          |
| **prompt**      | `str`       | Optional string displayed to the user during `prep_execute`.                           |
| **description** | `str`       | Brief description of the plugin’s functionality.                                       |
| **needs_args**  | `bool`      | Indicates whether the plugin requires user input or arguments. Used in `prep_execute`. |
<<<<<<< HEAD
| **commands**    | `list[str]` | Optional list defining operational commands for the plugin.                            |
=======
| **modes**       | `list[str]` | Optional list defining operational modes for the plugin.                               |
>>>>>>> 6c77bdb93c75ccbe6784fb4f554a40c852d74b31
| **help_text**   | `str`       | Text shown when the user requests plugin-specific help.                                |
| **dev_only**    | `bool`      | Marks plugins intended only for developers or sensitive operations.                    |
| **git_repo**    | `str`       | The associated Git repository URL, if applicable.                                      |

## Methods

1. Prep Execute
   `prep_execute(self, input_callable: Callable = None, output_callable: Callable = None, *args, **kwargs) -> str | tuple[str, str] | None`

   Prepares the plugin for execution.
   Handles prompt display, user input collection, and mode validation.

      Behavior:

      - Outputs the defined prompt.
      - If the plugin requires arguments:
         - Returns a `str` if a single user input is expected.
         - Returns a `tuple (input, mode)` if operational modes are defined.
      - Returns `None` if:
         - No input is required,
         - The operation is cancelled (e.g., `Ctrl+C`), or
         - An error occurs.

2. Execute
   `execute(self, *args, **kwargs)`

   - Runs the plugin's primary logic.
   - Would typically run `prep_execute` followed by the plugins's main entry point, such as a `.run()` method.

3. Direct Execute
   `direct_execute(self, *args, **kwargs)`

   - Directly execute the plugin's primary logic without the need of `prep_execute` user interface.
   - Assumes prior preparation of parameters to be used.
   - Intended for automation or preconfigured workflows where arguments are already known.
