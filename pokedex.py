import requests
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def obtener_pokemon(nombre_o_id):
    # Convertimos a minúsculas para evitar errores si el usuario escribe "Pikachu" o "PIKACHU"
    busqueda = str(nombre_o_id).strip().lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{busqueda}"
    
    try:
        response = requests.get(url)
        
        # Si la API devuelve 404 significa que el Pokémon no existe
        if response.status_code == 404:
            console.print(f"[bold red]❌ El Pokémon '{busqueda}' no existe. Verifica el nombre o ID.[/bold red]")
            return
        
        response.raise_for_status() # Lanza excepción para otros códigos HTTP de error
        data = response.json()
        
        # Datos básicos
        nombre = data["name"].capitalize()
        pokedex_id = data["id"]
        tipos = [t["type"]["name"].upper() for t in data["types"]]
        string_tipos = " / ".join(tipos)
        
        # Construimos la tabla de estadísticas
        table = Table(title=f"Estadísticas Base de {nombre}", show_header=True, header_style="bold magenta")
        table.add_column("Stat", style="cyan")
        table.add_column("Valor Base", justify="right", style="green")
        table.add_column("Barra", style="yellow")

        for stat in data["stats"]:
            nombre_stat = stat["stat"]["name"].upper()
            val = stat["base_stat"]
            # Creamos una barra visual proporcional al stat (máximo ~255)
            barra = "█" * (val // 10)
            table.add_row(nombre_stat, str(val), barra)

        # Imprimimos todo bien estructurado
        console.print(Panel(f"[bold yellow]#{pokedex_id} {nombre}[/bold yellow]\n[bold white]Tipo(s): {string_tipos}[/bold white]", title="Pokédex CLI"))
        console.print(table)

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error de conexión:[/bold red] {e}")

# Bucle principal de la app
if __name__ == "__main__":
    while True:
        busqueda = input("\nIngresa el nombre o ID de un Pokémon (o 'salir' para terminar): ")
        if busqueda.lower() == 'salir':
            print("¡Hasta luego, entrenador!")
            break
        if busqueda:
            obtener_pokemon(busqueda)