AGM
===
**AGM** (Active Grammar-based modeling) is a modern core for **perception-aware robotic architectures**. It relies on a visual language named AGGL (Active Graph Grammar Language) that is used describe the possible changes that robots can make to their world models and the behavior that they should adopt if such changes are desired.
In conjunction with an AI planner, AGGL descriptions are used by AGM to reason about what to do depending on the current objectives and world model. In the context of AGM, a _behavior_ is the resulting phenomena of the coordinated interaction between the main modules of the architecture. These modules eventually propose world model changes to the executive, entering in a loop in which AGM activates some modules and --after a modeling or performing some action-- these modules propose model changes.

**AGGL** (Active Graph Grammar Language) is a powerful (yet easy to understand) visual language visual language that is used describe the possible changes that robots can make to their world models and the behavior that they should adopt if such changes are desired. The description of these changes, expressed as graph-grammar rules, can be used for several purposes:
* Generating plans to perceive the world
* Generating plans to modify the world or the relationship between the robot and the world
* Verifying world model modifications

## Installation:
### Download
Despite we haven't made a release yet, the repository is quite stable and is unlikely to be broken. You can download a repository snapshot [using this link](https://github.com/ljmanso/AGM/archive/master.zip) or clone the repository using a git client (url: git://github.com/ljmanso/AGM.git).
### Install
In addition the regular C++ requirements for the library, you will need to install some dependencies for the editor. Some of them are mandatory (PySide, pyparsing) and others are optional, depending on what you intend to do, specially if you want to export AGGL rules to PNG files (numpy, ImageOps). In Debian-based GNU/Linux distributions these dependencies can be installed using the following commands (as root):

_Mandatory dependencies_: `apt-get install cmake ppython python-pyside python-pyparsing`

_Optional_: `apt-get install python-numpy python-imaging`

Once the dependencies have been installed you can safely install AGM and its associated appliactions:

`cmake .`

`make`

and, finally, as root:

`make install`


## What do I get with AGM?
The project is composed of four different elements:
* libAGM, the framework-agnostic library that is used to implement executives (*libagm*).
* The AGGL visual editor (*AGGLEditor*).
* An AGGL to PDDL compiler (*aggl2pddl*).
* A problem visualizer (*agm_xmlViewer*).
* An PDDL problem generator (*agm_xml2problem*).
* The implementation of an executive designed to work with the [RoboComp framework](http://robocomp.org) (*RoboCompAGMExecutive*).

###AGM library
The library that implements the core of AGM (_libagm_). The API of the library is available [here](http://here).

###AGGL Visual editor
The visual editor, AGGLEditor, eases the process of designing grammars. It's use is described in its own wiki page: [[AGGLEditor]].

###Problem visualizer
agm_xmlViewer initialWorld.xml goalPattern.xml

###AGGL to PDDL compiler
aggl2pddl -i grammar.aggl -p activeRules.pddl -f activeAndPassiveRules.pddl

###Problem viewer
agm_xmlViewer initialWorld.xml goal.xml

###PDDL problem generator
agm_xml2problem initialWorld.xml goal.xml problem.pddl [unknownMemorySize]
