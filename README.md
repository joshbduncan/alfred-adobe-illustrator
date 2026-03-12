# Alfred Adobe Illustrator Command Palette

Quickly access Adobe Illustrator menu commands, tools, and more directly from Alfred.

## Features

- Menu Commands
- Tool Commands
- User Actions
- Recent Files
- Update Commands

## Usage

Type `ai` in Alfred to launch the Adobe Illustrator Command Palette (the keyword is configurable in the workflow settings).

Pick one of the available options:

- **Menu Commands** — Execute any Illustrator menu command (e.g. `Object > Expand`, `Type > Create Outlines`).
- **Tool Commands** — Switch to any Illustrator tool by name.
- **User Actions** — Run a saved Action from your Illustrator Actions panel.
- **Recent Files** — Open a recently used Illustrator file.
- **Update Commands** — Download the latest menu and tool command lists from the [AiCommandPalette](https://github.com/joshbduncan/AiCommandPalette) repository.

### Updating Commands

Select **Update Commands** from the `ai` menu at any time to fetch the latest menu and tool command definitions. A notification will confirm once the update is complete.

## Notes

This project is a close sibling to my full-featured, cross-platform [AiCommandPalette](https://github.com/joshbduncan/AiCommandPalette) project.

> [!WARNING]
> Using Alfred Adobe Illustrator Command Palette requires some basic knowledge of Illustrator. The workflow doesn't know which commands can or can't be run at the time of execution so tread carefully.

> [!IMPORTANT]
> There are some known issues with executing actions via a script. There are no known solutions to this so if you encounter errors with a particular Action, it just may not be suitable to execute via a script.

> [!TIP]
> Most every action this workflow executes can be undone by choosing Edit > Undo (from the Edit menu at the top of your screen), or by pressing Command-Z.

## Credits

### Testing
- [Kurt Gold](https://community.adobe.com/t5/user/viewprofilepage/user-id/8354168)
- [Sergey Osokin](https://github.com/creold)

### Built-In Menu Commands and Tools
- [krasnovpro](https://community.adobe.com/t5/user/viewprofilepage/user-id/9425584)
- [Shalako Lee](https://github.com/shalakolee)
- [sttk3](https://judicious-night-bca.notion.site/app-executeMenuCommand-43b5a4b7a99d4ba2befd1798ba357b1a)
