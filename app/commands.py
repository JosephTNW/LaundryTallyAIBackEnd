from app import app, db
from app.models import User, Launderer, Laundry, Clothes, association_table
from sqlalchemy import text
from datetime import datetime

@app.cli.command('seed_db')
def seed_db():
    """Seed the database with some initial data."""
    user1 = User(
        name='Alice', 
        email='alice@example.com', 
        password='password',
    )
    user2 = User(
        name='John Wick', 
        email='johm@example.com', 
        password='password',
    )
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()  # Commit to get the ID

    launderers = [Launderer(
        name="Cottonmate Laundry", 
        address="Cikarang Utara - Depan Indomaret President Univ, Jl. Ki Hajar Dewantara No.3, Simpangan, Kabupaten Bekasi, Jawa Barat 17530", 
        phone_num="+62 856-4860-1730",
        desc="Cottonmate Laundry is a laundry service located in front of Indomaret President University.",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='launderer1.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="LaundryKlin Cilegon", 
        address="Cilegon - Jl. Temu Putih, Bekasi Regency, West Java, 17530", 
        phone_num="+62 877-7716-2688",
        desc="Jasa laundry satu ini terintegrasi dengan teknologi canggih sehingga proses cuci menjadi lebih mudah dan cepat.",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='LaundryKlin.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="Mr Klin", 
        address="Bekasi Jl. Kemang Anyelir 2, Blok AC No. 6, Kemang Pratama 2, RT.003/RW.035", 
        phone_num="+62 21-9855-5886",
        desc="MR KLIN LAUNDRY berdiri sejak 2009 dengan pengalaman selama lebih dari 15 tahun dan telah membimbing 270 mitra.",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='MrKlin.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="Bamboo Laundry", 
        address="Jagakarsa Jl. Raya Moch Kahfi 1 No. 8, RT.004/RW.002, Jakarta Selatan", 
        phone_num="+62 813-2386-0556",
        desc="Bamboo Laundry, yang kini telah dikelola secara profesional sebagai bagian dari 7 tahun berkelanjutan atas berkembangnya Clothes Laundry Indonesia.",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='BambooLaundry.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="Pam-Pam Laundry", 
        address="Jagakarsa Jl. Raya Moch Kahfi 1 No. 8, RT.004/RW.002, Jakarta Selatan", 
        phone_num="+62 821-1222-0209",
        desc="Great Price Great Service",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='PamPamLaundry.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="JOSS Laundry", 
        address="Pasirgombong Cikarang Utara, Bekasi Regency, West Java 17530", 
        phone_num="+62 821-2495-8201",
        desc="Joss Laundry the solution for every laundry",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='JossLaundry.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="Molandi Laundry", 
        address="Mekarmukti Jl. Kasuari raya No.22B, Cikarang, Kabupaten Bekasi, Jawa Barat 17530", 
        phone_num="+62 811-1797-066",
        desc="Great Small Laundry",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='MolandiLaundry.jpg',
        inputted_at=datetime.now()
    ), Launderer(
        name="Citra Fim Laundry", 
        address="Mekarmukti Jl. Singa Raya Jl. Cikarang Baru Raya No. 1, Kecamatan Cikarang Utara, Kabupaten Bekasi, Jawa Barat 17534", 
        phone_num="+62 898-8896-006",
        desc="Laundry Near the Boarding House, Cheap prices and Clean",
        has_whatsapp=True,
        has_delivery=True,
        l_pic='CitraFim.jpg',
        inputted_at=datetime.now()
    )]
    db.session.add_all(launderers)
    db.session.commit() 

    clothes = [
        Clothes(
        c_type='T-shirt', 
        color='Black', 
        owner=user1.id,
        cloth_pic='clothes1.jpg', 
        inputted_at=datetime.now(),
        desc='A black T-shirt got from Amazon'
    ),
    Clothes(
        c_type='T-shirt', 
        color='Green', 
        owner=user1.id,
        cloth_pic='clothes2.jpg', 
        inputted_at=datetime.now(),
        desc='Don\'t use this to the beach'
    ),
    Clothes(
        c_type='Shirt', 
        color='Blue', 
        owner=user1.id,
        cloth_pic='clothes3.jpg', 
        inputted_at=datetime.now(),
        desc='A Blue T-shirt from my dad'
    ),
    Clothes(
        c_type='Shirt', 
        color='White', 
        owner=user1.id,
        cloth_pic='clothes4.jpg', 
        inputted_at=datetime.now(),
        desc='A White T-shirt from my mom'
    ),
    Clothes(
        c_type='Shirt', 
        color='Green', 
        owner=user1.id,
        cloth_pic='clothes5.jpg', 
        inputted_at=datetime.now(),
        desc='A Green Shirt for my party'
    ),
    Clothes(
        c_type='T-Shirt', 
        color='Brown', 
        owner=user1.id,
        cloth_pic='clothes6.jpg', 
        inputted_at=datetime.now(),
        desc='Brown Shirt from Uniqlo'
    ),
    Clothes(
        c_type='T-Shirt', 
        color='Black', 
        owner=user1.id,
        cloth_pic='clothes7.jpg', 
        inputted_at=datetime.now(),
        desc='Black Shirt from Matahari'
    ),
    Clothes(
        c_type='T-Shirt', 
        color='Blue', 
        owner=user1.id,
        cloth_pic='clothes8.jpg', 
        inputted_at=datetime.now(),
        desc='Blue Shirt from The Executive'
    ),
    Clothes(
        c_type='T-Shirt', 
        color='White', 
        owner=user1.id,
        cloth_pic='clothes9.jpg', 
        inputted_at=datetime.now(),
        desc='White Polo Shirt'
    ),
    # Clothes(
    #     c_type='Shirt', 
    #     color='Blue', 
    #     owner=user1.id,
    #     cloth_pic='clothes10.jpg', 
    #     inputted_at=datetime.now(),
    #     desc='Blue Formal Shirt'
    # ),
    ]

    db.session.add_all(clothes)
    db.session.commit() 

    laundry1 = Laundry(
        launderer=launderers[0].id, 
        bill_pic='bill1.jpg',
        laundered_at=datetime.now(),
        laundry_days=3,
        status='pending',
        owner=user1.id
    )
    db.session.add(laundry1)
    db.session.commit()

    try:
        stmt = association_table.insert().values(laundry_id=laundry1.id, clothes_id=clothes[1].id, returned=False)
        stmt2 = association_table.insert().values(laundry_id=laundry1.id, clothes_id=clothes[2].id, returned=False)
        stmt3 = association_table.insert().values(laundry_id=laundry1.id, clothes_id=clothes[3].id, returned=False)
        stmt4 = association_table.insert().values(laundry_id=laundry1.id, clothes_id=clothes[4].id, returned=False)
        db.session.execute(stmt)
        db.session.execute(stmt2)
        db.session.execute(stmt3)
        db.session.execute(stmt4)
        db.session.commit()
    except Exception as e:
        print(f"Error inserting into association table: {e}")
        db.session.rollback()

    print('Database seeded!')
    
def reset_auto_inc(dbsession, sequence_name, table_name):
    """Reset the auto increment of a table to 1."""
    dbsession.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;"))
    dbsession.execute(text(f"ALTER TABLE \"{table_name}\" ALTER COLUMN id SET DEFAULT nextval('{sequence_name}');")) 
    
@app.cli.command('truncate_db')
def trunc_db():
    """Truncate all tables in the database."""
    db.session.query(association_table).delete()
    db.session.query(Laundry).delete()
    db.session.query(User).delete()
    db.session.query(Launderer).delete()    
    db.session.query(Clothes).delete()    
    reset_auto_inc(db.session, 'user_id_seq', 'user')
    reset_auto_inc(db.session, 'launderer_id_seq', 'launderer')
    reset_auto_inc(db.session, 'clothes_id_seq', 'clothes')
    reset_auto_inc(db.session, 'laundry_id_seq', 'laundry')
    
    db.session.commit()
    print('Database truncated!')

@app.cli.command('drop_db')
def drop_db():
    db.drop_all(bind_key=None)
    print('Database dropped!')

@app.cli.command('create_db')
def create_db():
    db.create_all()
    print('Database created!')


@app.cli.command('reset_assoc')
def reset_assoc():
    db.session.query(association_table).delete()
    db.session.commit()