from league import League
import league

def main():
    game_select = input("What game?: ")

    game = League()
    league.main(game)
    


if __name__ == "__main__":
    main()