from database import Database

def test_selection_db():
    db=Database()
    start=2
    stop=15
    value=start
    list_out = [''] * (stop-start+1)  # спиоск собирающийся на вывод
    for k in range(stop-start+1):
        list_out[k] = [''] * 2
    for i in range(0,stop-start+1):
        list_out[i][0]=value
        value+=1
    print(list_out)
    assert(db.print_in_giu(list_out))==[]
