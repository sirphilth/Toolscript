=========================================================================================
=======================================[ Credits ]=======================================
=========================================================================================

Script made by:         SirPhilthyOwl (An Owl)
Twitch:                 http://www.twitch.tv/SirPhilthyOwl

=========================================================================================
=======================================[ Script Changes ]================================
=========================================================================================

1.0.0 - Script made.

=========================================================================================
==================================[ Future implementations ]=============================
=========================================================================================

None yet

=========================================================================================
=======================================[ workings ]======================================
=========================================================================================

Script that allows viewers to buy tools for use with certain commands that require tools to activate.

In order to make a command that requires a tool to operate put this in the response:

$tool("other command")

Now there are 2 kind of command parameters, script parameters and chatbot parameters.

Chatbot parameters can be added as normally.. example:

$tool("$math[1*1]")

Script parameters however you will have to change the $ to ~.. example:

$tool("~SLOBSsourceT("laughguy.mp4", "onoff", "4")")

Make sure to always add the command between quotes --> " "

Everything else should be self explanatory. Make sure to read the tooltips on the UI.



-------------ToolsFile.txt-----------

To add extra equipment to the script, open up the ToolsFile.txt with the UI button "open toolsfile".

Then add tools in this way:

Tooltype, durability, cost

Example:

Iron, 5, 1000
Ruby, 8, 2000
Diamond, 10, 3000

These will automatically be added to the store.