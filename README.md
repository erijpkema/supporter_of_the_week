# Supporter of the week

## Usecase

Ops teams often drop all tasks at hand when there are incidents or requets for help.
This might not be the most efficient way to handle this. *supporter_of_the_week* creates a schedule with a team member on call to do first response.

## Installation

```bash
pipx install supporter_of_the_week
```

## Usage

```bash
usage: supporter_of_the_week [-h] [--start-date START_DATE ('%d-%m-%Y')] --supporters SUPPORTERS [--shuffle]
```

## Web version
I've experimented with [Pyodide](https://pyodide.org) to create a web assembly [web version](https://supporter.egonrijpkema.nl/).
It runs entirely in the browser.

## Limitations
For now the module only works for the Netherlands. So the schedule will not be accurate for other countries.
