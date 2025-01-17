import click

@click.command()
@click.option('-up', is_flag=True, help="Imprime los estrenos")
def cinepoliscli(up):  # Cambié 'upcoming' por 'up' para que coincida con el nombre de la opción
    if up:  # Aquí también usamos 'up' para verificar el flag
        click.echo("Hola Mundo")
    else:
        click.echo("No se han solicitado los estrenos")
