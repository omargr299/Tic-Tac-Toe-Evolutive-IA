num = 2
    boards = []
    for i in range(num):
        boards.append(Board(wnd))
        wnd.blit(boards[i].surface,((w//3)*i,0))
        boards[i].DrawnBoard()

    print(boards)