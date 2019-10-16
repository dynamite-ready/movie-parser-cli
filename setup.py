from cx_Freeze import setup, Executable
setup( name = "evaluate-images",
        version = "0.1",
        description = "Evaluates images",
        executables = [Executable("evaluate-images.py")],
        options = {
            'build_exe': {
                'packages': ['tensorflow', 'keras']
            }
        }
    )