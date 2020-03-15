import random
import time
import json
import click
from click.exceptions import UsageError

from colorama.ansi import Fore, Back, Style, clear_line, Cursor, clear_screen, set_title
from gutenhaiko import models, download

magenta = Style.BRIGHT + Fore.MAGENTA
yellow = Style.BRIGHT + Fore.YELLOW
green = Style.BRIGHT + Fore.GREEN
red = Style.BRIGHT + Fore.RED


def format_haiku_json(
    author, title, date, haiku, page=None, left_padding=10, **kwargs_dump
):
    return (
        green
        + "author: ".rjust(left_padding)
        + f"{yellow}{author}\n"
        + green
        + "title: ".rjust(left_padding)
        + f"{yellow}{title}\n"
        + green
        + "date: ".rjust(left_padding)
        + f"{yellow}{date}\n"
        + green
        + ("page: ".rjust(left_padding) + f"{yellow}{page}\n" if page else "")
        + green
        + "haiku: ".rjust(left_padding)
        + f"{magenta}{haiku[0]}\n"
        + (" " * left_padding)
        + f"{magenta}{haiku[1]}\n"
        + (" " * left_padding)
        + f"{magenta}{haiku[2]}\n"
        + Style.RESET_ALL
        + green
    )


nice_things_to_say = [
    "what a nice book!",
    "I remember reading that one when i was little, great book!",
    "WAT! where did you find that one!",
    "Oh yeah, one of the best!",
    "Great choice!",
]

LOGO = (
    Style.BRIGHT
    + green
    + "\n"
    + "                               .|                          \n"
    "                              | |                          \n"
    "                              |'|            ._____        \n"
    "                      ___    |  |            |.   |' .----|\n"
    "              _    .-'   '-. |  |     .--'|  ||   | _|    |\n"
    "           .-'|  _.|  |    ||   '-__  |   |  |    ||      |\n"
    "           |' | |.    |    ||       | |   |  |    ||      |\n"
    "           |  '-'     '    "
    "       '-'   '-.'    '`      |\n"
    "          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    "\n" + yellow + "             ██████╗ ██╗   ██╗████████╗███████╗███╗   ██╗\n"
    "            ██╔════╝ ██║   ██║╚══██╔══╝██╔════╝████╗  ██║\n"
    "            ██║  ███╗██║   ██║   ██║   █████╗  ██╔██╗ ██║\n"
    "            ██║   ██║██║   ██║   ██║   ██╔══╝  ██║╚██╗██║\n"
    "            ╚██████╔╝╚██████╔╝   ██║   ███████╗██║ ╚████║\n"
    "             ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═══╝\n"
    "\n" + magenta + "                 ██╗  ██╗ █████╗ ██╗██╗  ██╗██╗   ██╗\n"
    "                 ██║  ██║██╔══██╗██║██║ ██╔╝██║   ██║\n"
    "                 ███████║███████║██║█████╔╝ ██║   ██║\n"
    "                 ██╔══██║██╔══██║██║██╔═██╗ ██║   ██║\n"
    "                 ██║  ██║██║  ██║██║██║  ██╗╚██████╔╝\n"
    "                 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ \n"
    f"\n                                         {green}by {magenta}Sloev" + "\n"*5
)

USAGE = (
    "\n"
    + green
    + "Wat?".ljust(17)
    + magenta
    + f"Guten Haiko {yellow}lets you extract haiku poems from text"
    "\n"
    + green
    + "Usage: ".ljust(17)
    + yellow
    + f"{magenta}gutenhaiko{yellow} \\\n"
    + "                 -f frankenstein.txt \\\n"
    + "                 -a 'Mary Wollstonecraft Shelley' \\\n"
    + "                 -t 'frankenstein' \\\n"
    + "                 -d '1818-01-01'"
    + "\n"
    + green
    + f"Optional params: {magenta}--commandfile "
    + f"{yellow}[-cf] a file with comma seperated \n"
    + "                                     values for f,a,t,d params\n"
    + f"                 {magenta}--outputfile  "
    + f"{yellow} [-o] the output file path [default haiku.json\n"
    + f"                 {magenta}--eighties    "
    + f"{yellow} [-e] eighties mode [default 1]"
    + green
    + "\n\n"
    + f"Advanced usage:  {magenta}gutenhaiko{yellow} \\\n"
    + "                 -f frankenstein.txt \\\n"
    + "                 -a 'Mary Wollstonecraft Shelley' \\\n"
    + "                 -t 'frankenstein' \\\n"
    + "                 -d '1818-01-01' \\\n"
    + "                 -f dracula.txt \\\n"
    + "                 -a 'Bram Stoker' \\\n"
    + "                 -t 'dracula' \\\n"
    + "                 -d '1897-05-26'\n"
    + green
)


def loading_sequence(*items):
    click.echo(clear_screen())

    for label, splash in items:
        click.echo(green)

        if label is not None:
            with click.progressbar(label=label, length=10) as bar:
                for i in range(10):
                    bar.update(i)
                    time.sleep(1.0 - (i * 0.1))
            click.echo(clear_screen())
        for line in splash.splitlines():
            click.echo(line)
            time.sleep(0.05)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--eighties", "-e", type=bool, default=True)
@click.option("--commandfile", "-cf", type=click.File("rb"), default=None)
@click.option("--outputfile", "-o", type=click.File("a"), default="haiku.json")
@click.option("--file", "-f", type=click.File("r"), multiple=True)
@click.option("--author", "-a", type=str, multiple=True)
@click.option("--title", "-t", type=str, multiple=True)
@click.option("--date", "-d", type=click.DateTime(), multiple=True)
def cli(ctx, eighties, commandfile, outputfile, file, author, title, date):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(set_title('Guten Haiko'), nl=False)
    if ctx.invoked_subcommand is None:
        if not (commandfile or file):
            if eighties:
                loading_sequence(("Loading Guten Haiko", LOGO), (None, USAGE))
            else:
                click.echo(USAGE)
            exit(0)
        if not models.MODELS_ARE_DOWNLOADED:
            click.echo(f"{red}models are not downloaded, run {magenta}gutenhaiku setup")
            exit(1)
        if not (len(file) == len(author) == len(title) == len(date)):
            click.echo(f"{red}bad args: -f, -a, -t, -d needs to be same amount")
            exit(1)
        if eighties:
            loading_sequence(("Loading Guten Haiko", LOGO))

            click.echo(
                magenta
                + f"\n  Now processing {len(file)} {'books' if len(file)>1 else 'book'}\n"
                f"  Starting with {yellow}{title[0]} {magenta}by {yellow}{author[0]}{magenta}\n"
                f"  {random.choice(nice_things_to_say)}\n"
                f"{green}  We start by doing some loading of {magenta}fancy AI models{green}",
                nl=False,
            )
            for i in range(1, 9, 4):
                time.sleep(i / 4.0)
                click.echo(".", nl=False)

        from gutenhaiku import pipeline

        if eighties:
            click.echo(".", nl=False)
            time.sleep(0.2)

            click.echo(f"\n{green}  Now we are ready to scan through the book, enjoy!\n")

        for f, a, t, d in zip(file, author, title, date):
            for data in pipeline.process_generator(
                f.read(), progress_bar=click.progressbar
            ):
                data["author"] = a
                data["title"] = t
                data["date"] = d.isoformat()
                if eighties:
                    click.echo(clear_line())
                    click.echo(format_haiku_json(**data))
                outputfile.write(json.dumps(data)+"\n")

        click.echo(clear_line())
        if eighties:
            click.echo(f"\n{green}  All done, have a great day!\n")

def show_help(*args, **kwargs):
    click.echo(LOGO)
    click.echo(USAGE)
    try:
        self = args[0]
        click.echo(red + f'Error: {self.format_message()}')
    except:
        pass

UsageError.show = show_help
cli.get_help = show_help

@cli.command()
def help():
    show_help()

@cli.command()
@click.option("--eighties", "-e", type=bool, default=True)
def setup(eighties):
    if eighties:
        loading_sequence(("Loading Guten Haiko", LOGO))
    if models.MODELS_ARE_DOWNLOADED:
        click.echo(green + "Models are already downloaded, exiting")
        exit(0)

    click.echo(green + "Downloading models")
    download.download_models(click.progressbar)
    click.echo(clear_line())
    click.echo(green + "Done")


if __name__ == "__main__":
    cli()
