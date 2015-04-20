__author__ = 'Austen'

class LaTeXTable(object):
    """
    Class for generating LaTeX 3-line table.
    Usage similar to prettytable
    """
    def __init__(self, headers):
        self._headers = [str(i) for i in headers]
        self._rows = []

    def _proc_index(self,content,index):
        if index == None:
            i = len(content)
        else:
            i = index
        return i

    def add_row(self, row, index=None):
        i = self._proc_index(self._rows,index)
        self._rows.insert(i,row)

    def add_column(self, header, column, index=None):
        i = self._proc_index(self._headers,index)
        self._headers.insert(i,header)
        for j, new_cell in enumerate(column):
            if len(self._rows) < j+1:
                self.add_row([])
            self._rows[j].insert(i,new_cell)

    def __str__(self):
        outs = ['\\begin{tabular}{%s}' % ('l'*len(self._headers)),
                '\hline',' & '.join(self._headers)+' \\\\','\hline']
        for row in self._rows:
            outs.append(' & '.join(row)+' \\\\')
        outs.extend(['\hline','\\end{tabular}'])
        return "\n".join(outs)