from database import Database
from user_interface import UserInterface

def test_selection_db():
    db=Database()
    start=2
    stop=15
    value=start
    list_out = [''] * (stop-start+1)  # спиоск собирающийся на вывод Moked
    for k in range(stop-start+1):
        list_out[k] = [''] * 2
    for i in range(0,stop-start+1):
        list_out[i][0]=value
        value+=1
    print(list_out)
    assert(db.print_in_giu(list_out,0))==[]

def test_data_revision():
    ui=UserInterface()
    assert (ui.data_revision('12.08.2023') == True)
    assert (ui.data_revision('30.08.2023') == None)
