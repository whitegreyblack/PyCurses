from examples.calendargrid import MonthGrid, DateNode

def main():
    m = MonthGrid(10, 2018)
    m.build()
    print(m)

if __name__ == "__main__":
    main()