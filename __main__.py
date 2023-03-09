import click
from pipelines.read import ReadData
from pipelines.classify import ClassifyData
from pipelines.analyze import analyze_data


@click.group()
def cli() -> None:
    pass


@cli.command(name="budgeting_application")
@click.option('--read', is_flag=True, show_default=True, default=False)
@click.option('--classify', is_flag=True, show_default=True, default=False)
@click.option('--analyze', is_flag=True, show_default=True, default=False)
def run(read: bool, classify: bool, analyze: bool) -> None:
    """
    Runs whole pipeline if a section isn't specified
    """
    if any([read, classify, analyze]):
        if read:
            ReadData().make_calculations()
        elif classify:
            ClassifyData().make_calculations()
        elif analyze:
            analyze_data()
    else:
        ReadData().make_calculations()
        ClassifyData().make_calculations()
        analyze_data()


if __name__ == '__main__':
    cli()
