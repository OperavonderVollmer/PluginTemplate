# Ophelia's Plugin Template

Abstract Class to be used by plugins under the Ophelia script family.
**Does not run by itself.**

## Parameters

1. Name
2. Prompt
   - Used under [prep_execute](https://github.com/OperavonderVollmer/PluginTemplate/blob/main/README.md#L24) method to print the line.
3. Description
4. Needs Args
   - An optional bool indicating the plugins need of arguments, used in [prep_execute](https://github.com/OperavonderVollmer/PluginTemplate/blob/main/README.md#L24) method
5. Modes
   - An optional list dictating the plugins different modes
6. Help Text
7. Dev Bool
   - A bool indicating access level. Used for sensitive transactions
8. Git Repo

Attributes are accessible under the meta dictionary.

## Methods
prep_execute
    - Method that runs prior to execute. Works as both user input interface and notification of the script's operations. 
    - Returns a string if a single user input is required.
    - Returns a tuple of (input, mode) if the plugin defines operational modes.
    - Returns None if no input is needed, cancelled, or an error occurs.

execute
    - Runs the scripts main function. 
    - Would typically run [prep_execute](https://github.com/OperavonderVollmer/PluginTemplate/blob/main/README.md#L24) followed by the specific script's **.run** method.

direct_execute
    - Directly execute the scripts main function without the need of[prep_execute's](https://github.com/OperavonderVollmer/PluginTemplate/blob/main/README.md#L24) user interface.
    - Assumes prior preparation of parameters to be used. 