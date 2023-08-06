from arkdata.models import drop_all, create_all, seed_all


if __name__ == '__main__':
    drop_all()
    print("Dropped All Tables")
    create_all()
    print("Created All Tables")
    seed_all()
