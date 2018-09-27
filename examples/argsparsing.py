import click

@click.command()
@click.option("-i", "inputfolders", multiple=True, 
              help="Folder(s) containing yaml data files")
@click.option("-o", "outputfolder", default="export", required=False,
              help="Folder to hold any exported files from application.")
@click.option("--rb", "--rebuild", "rebuild", is_flag=True, required=False, nargs=1,
              help="Option allows rebuilding of tables for a clean start.")
def main(inputfolders, outputfolder, rebuild):
    print(f"inputfolders: {inputfolders}")
    print(f"outputfolder: {outputfolder}")
    print(f"rebuild option: {rebuild}")

if __name__ == "__main__":
    main()