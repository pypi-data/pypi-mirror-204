class Table:
    def __init__(self, name, col_headers, row_headers, rows):
        self.col_headers = col_headers
        self.row_headers = rows
        self.table = []
        self.name = name
        x = [str(name)]
        for i in col_headers:
            x.append(str(i))
        self.table.append(x)
        for i in range(len(row_headers)):
            x = [str(row_headers[i])]
            for ii in rows[i]:
                x.append(str(ii))
            self.table.append(x)

    def draw(self):
        maxlen = 0
        for i in self.table:
            for ii in i:
                if maxlen < len(ii):
                    maxlen = len(ii)
        maxlen += 1
        width = ((maxlen + 1) * len(self.table[0])) - 1

        def draw_split():
            print('+', end='')
            for i in range(len(self.table[0])):
                print('-' * maxlen, end='+')
            print()

        for row in self.table:
            draw_split()
            for i in row:
                print('|' + i.rjust(maxlen//2+1, ' ').ljust(maxlen, ' '), end='')
            print('|')
        draw_split()
