from database import Database

def test_selection_db():
    db=Database()

    print(db.print_in_giu([(3,),(5,)]))
