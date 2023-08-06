Add this text to the README when the code changes have been completed


## What is the difference between a command and an operation?
A command is closer to a function, it is the definition of a transform step.  An operation is an invocation of a command with concrete arguments.

The UI reads the list of Commands, along with their argspecs and presents them in the UI.  Using them to build a list of operations.

Commands include a python function to actually perform the transformation, a python function to emit the equivalent python code, and argspecs describing the expected arguments for the Command.

---
Previously invocations of commands and commands, and commands themselves were called Command (with extra explanatory endings).  @zainhoda helped the disambiguation in a pairing session.  Most of the changes have been made to frontend react widget... they need to be carried through to the backend python code.
