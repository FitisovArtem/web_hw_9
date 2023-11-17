from parser import main as parser_main
from seed import main as seed_main
import models as models_main


if __name__ == '__main__':
    try:
        parser_main()
    except Exception as e:
        print(e)

    try:
        models_main
    except Exception as e:
        print(e)

    try:
        seed_main()
    except Exception as e:
        print(e)
