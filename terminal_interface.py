import click
from cine_scraper import print_terminal,get_new_releases , print_weather


@click.command()
@click.option('-up', is_flag=True, help="Imprime los estrenos")
def cinepoliscli(up):  # Cambié 'upcoming' por 'up' para que coincida con el nombre de la opción
    if up:  # Aquí también usamos 'up' para verificar el flag
        # print_terminal()
        print_terminal()