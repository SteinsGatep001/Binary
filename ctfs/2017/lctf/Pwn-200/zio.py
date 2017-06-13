class zio(object):
    #.....
    def w(self, s):
        self.write(s)
    def wl(self, s = ''):
        if isinstance(s, (int, long)):
            self.writeline(str(s))
        else:
            self.writeline(s)
    def wls(self ,sequence):
        self.writelines( [str(i) if isinstance(i, (int, long)) else i for i in sequence] )
    def r(self, size = None, timeout = 1):
        return self.read(size, timeout)
    def rl(self, size = 1):
        return self.read_line(size)
    def rtl(self, pattern_list, timeout = 1,
        searchwindowsize = None):
        return self.read_until(pattern_list, timeout, searchwindowsize)
    def w_af(self, pattern_list, s, timeout = 1,
        searchwindowsize = None):
        self.read_until(pattern_list, timeout, searchwindowsize)
        self.writeline(s)
    def wls_af(self, pattern_list, sequence, timeout = 1,
        searchwindowsize = None):
        self.read_until(pattern_list, timeout, searchwindowsize)
        self.writelines( [str(i) if isinstance(i, (int, long)) else i for i in sequence] )