
class HistoryWriter:
    activity_list = ('DEPOSIT', "DELETED",'ISSUE', 'REGISTER', 'ADD BOOK')
    def __init__(self, master, activity_type, database):
        self.master = master
        self.database  = database
        self.activity_type = activity_type
    
    def write(self, msg, activity_type=None):
        if activity_type is not None:
            self.activity_type = activity_type
        if self.activity_type not in self.activity_list:
            raise ValueError(f'activity type must be one of {self.activity_list}')
        self.database.execute('INSERT INTO history(activity_type, activity, account) VALUES(?,?,?)', (self.activity_type, msg, self.master.current_account))
    
    