import main
import os

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = str(150) + "," + str(40)
    main = main.Main()
    main.main()